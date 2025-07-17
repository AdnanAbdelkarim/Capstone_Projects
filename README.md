# 🚗 License Plate Recognition for Qatari Plates (YOLOv8)

This project focuses on developing a robust License Plate Recognition (LPR) system using the YOLOv8 object detection model. It is trained to detect **Qatari license plates** from vehicle images and perform inference on unseen images with high accuracy.

---

## 📂 Project Structure

```
Capstone_LPR/
│
├── dataset/                # Train/valid/test sets with Roboflow format
├── lpr_training/           # Training outputs (plots, metrics, weights)
├── testing_images/         # Input/output images for testing the model
├── yolov8n.pt              # Trained YOLOv8n weights
├── testing_script.py       # Script for inference on new images
├── LPR_QATAR_PLATES.ipynb  # Notebook used for training the model
├── requirements.txt        # Python dependencies
└── README.md               # Project overview and usage
```

---

## 📸 Inference: Before and After

The `testing_images/` folder contains visual examples of the model’s inference performance:

| Input Image                    | Output Image                               | Description                            |
|-------------------------------|--------------------------------------------|----------------------------------------|
| `big_plate_vehicle.png`       | `big_plate_detected.png`                   | Vehicle image before and after plate detection |
| `small_plate_vehicle.png`     | `small_plate_detected_and_cropped.png`     | Vehicle with a smaller plate size, before and after detection |

These image pairs show the model's ability to locate license plates across various vehicle and plate sizes.

---

## 📊 Dataset

This project uses the publicly available **Qatari license plate dataset** from Roboflow.

- 📎 Source: [Roboflow - Qatar Number Plate](https://universe.roboflow.com/rao-waqas/qatar-number-plate/dataset/5)
- Dataset includes images annotated with bounding boxes for number plates.
- Split into `train/`, `valid/`, and `test/` sets.


---

## 🛠️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/AdnanAbdelkarim/Capstone_Projects.git
   cd Capstone_Projects
```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   # On Mac/Linux use: source venv/bin/activate  # On Windows use: `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the trained YOLOv8 model**
   - Place your `yolov8n.pt` weights in the root directory.
   - If retraining, follow the instructions in the notebook below.

---

## 🧪 Inference

Run the detection on a test image:

```bash
python testing_script.py
```

The script will:
- Load your trained YOLOv8 model
- Run OCR on the specified image
- Display the prediction and save the output to the `testing_images/` folder

---

### ⚠️ Before running, update the following paths in `testing_script.py`:

```python
# ✅ Load the trained YOLO model
model = YOLO("C:/Users/student/Desktop/LPR/lpr_training/weights/best.pt")  # ← update this path

# ✅ Path to the test image
img_path = "C:/Users/student/Desktop/LPR/testing_images/1.png"             # ← update this path
```

✅ Example update:
```python
model = YOLO("lpr_training/weights/best.pt")
img_path = "testing_images/car1.png"
```

- The script will read images from the `testing_images/` folder and save outputs with predicted bounding boxes to the same folder.

---

## 📚 Model Training

The model was trained using the `LPR_QATAR_PLATES.ipynb` notebook:

- Training was conducted with the YOLOv8n architecture using the Ultralytics library.
- The notebook includes preprocessing, training and validation.

The training outputs (in `lpr_training/`) include:
- `confusion_matrix.png` and normalized version
- PR/ROC/F1 curves
- Training batch previews
- YAML config files (`args.yaml`)
- Result metrics in `.csv` and `.png`

---

## 🚧 Notes

- Ensure you adjust the `paths` in the notebook or scripts if you use a different directory structure.

---

## 📜 License & Attribution

- Dataset: © [Rao Waqas on Roboflow](https://universe.roboflow.com/rao-waqas/qatar-number-plate)
- Model: YOLOv8 by [Ultralytics](https://github.com/ultralytics/ultralytics)

---

## 🙌 Acknowledgements

This project was developed as part of a capstone project to apply computer vision techniques to a real-world problem — detecting and localizing Qatari license plates on vehicles using deep learning.  It showcases how object detection models like YOLOv8 can be leveraged for intelligent transportation systems and smart city applications.

---