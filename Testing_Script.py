import cv2
import os
import numpy as np
from ultralytics import YOLO
from paddleocr import PaddleOCR
from sort import Sort

# -----------------------------
# Load Models
# -----------------------------
vehicle_detector = YOLO("yolov8n.pt")
ev_classifier = YOLO(r"C:/Users/student/Desktop/EV_MODEL/runs/ev_detection_yolov8m/weights/best.pt")
lpr_detector = YOLO(r"C:/Users/student/Desktop/LPR/lpr_training/weights/best.pt")

ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False)

# -----------------------------
# Output Paths
# -----------------------------
output_video_path = r"C:/Users/student/Desktop/EV_MODEL/output_results_EV_LPR/live_feed_output.mp4"

snapshot_folder = r"C:/Users/student/Desktop/EV_MODEL/output_results_EV_LPR/images"
lp_folder = r"C:/Users/student/Desktop/EV_MODEL/output_results_EV_LPR/LP_images"

os.makedirs(snapshot_folder, exist_ok=True)
os.makedirs(lp_folder, exist_ok=True)

# -----------------------------
# SORT Tracker Setup
# -----------------------------
tracker = Sort(max_age=5, min_hits=2, iou_threshold=0.3)

# -----------------------------
# Processing Parameters
# -----------------------------
vehicle_class_ids = [2, 7]
MIN_RELATIVE_AREA_THRESHOLD = 0.05
EV_CONFIDENCE_THRESHOLD = 0.7
LPR_CLASS_ID = 10

MIN_VOTES_REQUIRED = 10
CONFIDENCE_RATIO = 0.8

track_classifications = {}

# -----------------------------
# Live Feed Setup
# -----------------------------
cap = cv2.VideoCapture(0)  # Change to IP stream if needed: cv2.VideoCapture("rtsp://...")
if not cap.isOpened():
    print(f"Error: Could not open live feed.")
    exit()

# Get frame size and FPS from camera (or set default)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

frame_count = 0
plate_digits_log = {}

print("✅ Live feed started. Press 'q' to stop.")

# -----------------------------
# Process Frames
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Frame capture failed.")
        break

    frame_count += 1
    image_height, image_width = frame.shape[:2]
    image_area = image_width * image_height

    # Step 1: Detect vehicles
    vehicle_results = vehicle_detector(frame, conf=0.65)

    detections = []
    for vehicle_box in vehicle_results[0].boxes:
        class_id = int(vehicle_box.cls)

        if class_id not in vehicle_class_ids:
            continue

        x1, y1, x2, y2 = map(float, vehicle_box.xyxy[0])
        width = x2 - x1
        height = y2 - y1
        area = width * height
        relative_area = area / image_area

        if relative_area < MIN_RELATIVE_AREA_THRESHOLD:
            continue

        confidence = vehicle_box.conf.item()
        detections.append([x1, y1, x2, y2, confidence])

    detections_np = np.array(detections) if len(detections) > 0 else np.empty((0, 5))

    # Step 2: SORT tracking
    tracks = tracker.update(detections_np)

    for track in tracks:
        x1, y1, x2, y2, track_id = track
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        track_id = int(track_id)

        # Initialize new track
        if track_id not in track_classifications:
            track_classifications[track_id] = {
                'label': 'UNKNOWN',
                'ev_votes': 0,
                'non_ev_votes': 0,
                'total_votes': 0,
                'locked': False,
                'snapshot_saved': False,
                'lpr_processed': False,
                'lp_bbox': None
            }

        track_state = track_classifications[track_id]

        # Snapshot when label is locked and snapshot not saved
        if track_state['locked'] and not track_state['snapshot_saved']:
            vehicle_crop = frame[y1:y2, x1:x2]
            if vehicle_crop.size == 0:
                continue

            color = (0, 255, 0) if track_state['label'] == 'EV' else (0, 0, 255)
            cv2.rectangle(vehicle_crop, (0, 0), (vehicle_crop.shape[1] - 1, vehicle_crop.shape[0] - 1), color, 2)
            label_text = f"{track_state['label']} ID {track_id}"
            cv2.putText(vehicle_crop, label_text, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            snapshot_filename = f"{track_state['label']}_Track{track_id}_Frame{frame_count}.jpg"
            snapshot_path = os.path.join(snapshot_folder, snapshot_filename)
            cv2.imwrite(snapshot_path, vehicle_crop)
            track_state['snapshot_saved'] = True
            print(f"✅ Snapshot saved for Track {track_id} as {snapshot_filename}")

        # If label locked skip classification
        if not track_state['locked']:
            vehicle_crop = frame[y1:y2, x1:x2]
            if vehicle_crop.size == 0:
                continue

            ev_results = ev_classifier(vehicle_crop, conf=0.5)

            if len(ev_results[0].boxes) > 0:
                ev_confidence = ev_results[0].boxes[0].conf.item()
                if ev_confidence >= EV_CONFIDENCE_THRESHOLD:
                    track_state['ev_votes'] += 1
                else:
                    track_state['non_ev_votes'] += 1
            else:
                track_state['non_ev_votes'] += 1

            track_state['total_votes'] = track_state['ev_votes'] + track_state['non_ev_votes']

            if track_state['total_votes'] >= MIN_VOTES_REQUIRED:
                ev_ratio = track_state['ev_votes'] / track_state['total_votes']
                non_ev_ratio = track_state['non_ev_votes'] / track_state['total_votes']

                if ev_ratio >= CONFIDENCE_RATIO:
                    track_state['label'] = 'EV'
                    track_state['locked'] = True
                elif non_ev_ratio >= CONFIDENCE_RATIO:
                    track_state['label'] = 'NON-EV'
                    track_state['locked'] = True

        # Run LPR ONCE per vehicle when label is locked
        if track_state['locked'] and not track_state['lpr_processed']:
            vehicle_crop = frame[y1:y2, x1:x2]
            if vehicle_crop.size == 0:
                continue

            lpr_results = lpr_detector(vehicle_crop, conf=0.3)

            for lpr_box in lpr_results[0].boxes:
                if int(lpr_box.cls) == LPR_CLASS_ID:
                    px1, py1, px2, py2 = map(int, lpr_box.xyxy[0])
                    plate_crop = vehicle_crop[py1:py2, px1:px2]

                    if plate_crop.size == 0:
                        continue

                    ocr_results = ocr.ocr(plate_crop, cls=True)

                    print(f"\n🔢 License Plate Detected: {ocr_results}")

                    plate_text = ""

                    if ocr_results and isinstance(ocr_results[0], list) and len(ocr_results[0]) > 0:
                        for line in ocr_results[0]:
                            text = line[1][0]
                            confidence = line[1][1]
                            print(f"Detected text: '{text}' with confidence: {confidence:.2f}")
                            plate_text += text + " "
                    else:
                        print("⚠️ No text found by OCR!")

                    plate_text_clean = plate_text.strip().replace(" ", "").replace("/", "")

                    if not plate_text_clean:
                        plate_text_clean = f"Unknown_Track{track_id}"

                    if track_id not in plate_digits_log:
                        lp_img_filename = f"{plate_text_clean}_Track{track_id}.jpg"
                        lp_img_path = os.path.join(lp_folder, lp_img_filename)
                        cv2.imwrite(lp_img_path, plate_crop)
                        plate_digits_log[track_id] = plate_text_clean
                        print(f"✅ Saved license plate image: {lp_img_filename}")
                        print(f"✅ License Plate Digits: {plate_text_clean}")

                    # Store the license plate box for persistent drawing
                    track_state['lp_bbox'] = (x1 + px1, y1 + py1, x1 + px2, y1 + py2)

                    track_state['lpr_processed'] = True

        # Draw vehicle bounding box and label
        label_display = track_state['label'] if track_state['locked'] else "CLASSIFYING"
        color = (0, 255, 0) if label_display == 'EV' else (0, 0, 255)
        label_text = f"{label_display} ID {track_id}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label_text, (x1 + 5, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Draw license plate box if known
        if track_state['lp_bbox'] is not None:
            lp_x1, lp_y1, lp_x2, lp_y2 = track_state['lp_bbox']
            cv2.rectangle(frame, (lp_x1, lp_y1), (lp_x2, lp_y2), (255, 0, 0), 2)
            cv2.putText(frame, "License Plate", (lp_x1, lp_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Show live feed with bounding boxes
    cv2.imshow('EV + LPR Live Feed', frame)

    # Write to output video
    out.write(frame)

    # Exit condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("❗ Quit command received.")
        break

# Cleanup
cap.release()
out.release()
cv2.destroyAllWindows()

# Final log
print("\n✅ Live feed processing complete.")
print(f"✅ Output video saved to: {output_video_path}")
print(f"✅ Vehicle snapshots saved in: {snapshot_folder}")
print(f"✅ License Plate images saved in: {lp_folder}")

print("\n📄 Final Recognized License Plates:")
for track_id, digits in plate_digits_log.items():
    print(f"Track {track_id}: {digits}")
