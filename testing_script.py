from ultralytics import YOLO
import cv2
from paddleocr import PaddleOCR

# ✅ Load the trained YOLO model
model = YOLO("C:/Users/student/Desktop/LPR/lpr_training/weights/best.pt")

# ✅ Load OCR model (CPU mode)
ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False)

# ✅ Path to the test image
img_path = "C:/Users/student/Desktop/LPR/testing_images/1.png"

# ✅ Read the image
img = cv2.imread(img_path)
if img is None:
    raise FileNotFoundError(f"❌ Image not found: {img_path}")

# ✅ Perform inference (with confidence threshold)
results = model(img, conf=0.6)

# ✅ Loop through detections and extract text
for result in results:
    for box in result.boxes.data.tolist():
        x1, y1, x2, y2, conf, class_id = box

        if int(class_id) == 10:  # License plate class
            plate_crop = img[int(y1):int(y2), int(x1):int(x2)]

            if plate_crop.size == 0:
                continue

            # Resize if too small
            h, w = plate_crop.shape[:2]
            if w < 100:
                scale = 320 / w
                new_w = 320
                new_h = int(h * scale)
                plate_crop = cv2.resize(plate_crop, (new_w, new_h))

            # Convert BGR to RGB
            plate_crop_rgb = cv2.cvtColor(plate_crop, cv2.COLOR_BGR2RGB)

            # OCR - get only the text
            result_text = ocr.ocr(plate_crop_rgb, cls=True)

            if result_text and result_text[0]:
                extracted_text = result_text[0][0][1][0]
                print(extracted_text)  # ✅ Only print the text (e.g., 111811)
            else:
                print("No text detected.")
