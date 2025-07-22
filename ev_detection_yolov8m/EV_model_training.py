from ultralytics import YOLO
import os

# Paths
dataset_yaml = os.path.join("dataset", "data.yaml")
output_dir = os.path.join("model_training")

# Load YOLOv8m model (pretrained)
model = YOLO("yolov8m.pt")

# Train the model
model.train(
    data=dataset_yaml,             # Path to data.yaml
    epochs=100,                    # Total epochs
    imgsz=960,                     # Input image size
    batch=32,                      # Batch size per GPU
    name="ev_detection_yolov8m",   # Output subdirectory name
    project=output_dir,            # Root training directory
    device=0,                      # Use GPU 0
    workers=4,                     # Data loading workers (adjustable)
    verbose=True,                  # Show training details
    exist_ok=True                  # Overwrite if folder exists
)
