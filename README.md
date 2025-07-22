# ⚡ Electric Vehicle Detection using YOLOv8

This project focuses on building an Electric Vehicle (EV) Detection system using the YOLOv8 object detection model. It was designed to classify whether a vehicle is electric based on custom-trained labels of EV models. If a vehicle is detected by the model, it is considered electric; otherwise, it is non-EV.

The model was trained on over **19,000 images** representing **203 different EV makes and models**.

---

## 📂 Project Structure

```
Capstone_EV_Detection/
│
├── dataset/                     # Train/val dataset and config
│   ├── train/
│   ├── val/
│   └── data.yaml
│
├── ev_training/                 # Training scripts and results
│   ├── EV_model_training.py     # Model training script
│   └── ev_detection_yolov8m/    # YOLOv8 training outputs (metrics, weights, curves)
│
├── testing_videos/              # Sample videos for model testing
│   ├── EV_detected_1.mp4
│   └── EV_detected_2.mp4
│
├── yolov8m.pt                   # Trained model weights (optional to push)
├── Testing_Script.py            # Script for video-based inference
├── dataset_scripts/             # Dataset creation and cleaning scripts
│   ├── scrape_ev_images.py              # Scrape EV images from the internet
│   ├── replace_class_ids.py             # Replace YOLO class IDs with EV-specific class IDs
│   ├── generate_labels_command.txt      # Label images using YOLO commands
│   ├── generate_data_yaml.py            # Automatically create data.yaml
│   ├── filter_non_vehicle_labels.py     # Remove irrelevant labels (e.g., person, animal)
│   └── filter_small_boxes.py            # Remove detections with small bounding boxes
│
├── requirements.txt             # Project dependencies
└── README.md                    # Project overview and usage
```

---

## 🎥 Inference: Before and After

The `testing_videos/` folder contains sample outputs that demonstrate the model’s inference capability on real-world video feeds:

| Input Video         | Output Video         | Description                          |
|---------------------|----------------------|--------------------------------------|
| `EV_not_detected_1`    | `EV_detected_1.mp4`  | Real-time detection of EV charging from **front** |
| `EV_not_detected_2`     | `EV_detected_2.mp4`  | Real-time detection of EV charging from **back** |

The model classifies a vehicle as EV if it matches any of the 203 EV make/model classes.

---

## 📊 Dataset & Preprocessing

The dataset contains **over 19,000 EV-only images**, scraped and preprocessed through several stages. The data was split into:

- **90% training** (~17,100 images)
- **10% validation** (~1,900 images)

> The validation set was used to monitor performance during training and generate evaluation metrics.

Key preprocessing steps included:

- 🔍 **Image Scraping**: `Downloading_images_from_internet.py`
- 🧾 **Label Generation**: `Generate_labels.txt` was used to batch-generate YOLO-style labels.
- 🔄 **Class ID Replacement**: `Changing_class_ids.py` replaces YOLO default IDs with real EV model names.
- 🧼 **Label Cleaning**:
  - `Removing_noncar_detections.py` deletes irrelevant detections like people, trees, etc.
  - `Removing_small_detections.py` removes vehicles with minimal bounding box area.
- 📄 **`data.yaml` Generation**: Automated using `Generating_datayaml_file.py`

> All 203 classes in `data.yaml` represent different EV makes/models. If YOLO detects any of them, the object is considered an EV.


---

## 🛠️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/AdnanAbdelkarim/Capstone_Projects.git
   cd Capstone_Projects/Capstone_EV_Detection
   ```

2. **(Optional) Create a virtual environment**
   ```bash
   python -m venv venv
   # Mac/Linux: source venv/bin/activate
   # Windows:   venv\Scripts\activate
   ```

3. **Install the required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download or place the trained YOLOv8 weights**
   - Place `yolov8m.pt` in the root directory or update `Testing_Script.py` accordingly.

---

## 🧪 Inference

Run the detection on a video stream or clip:

```bash
python Testing_Script.py
```

This script will:
- Load the trained YOLOv8 model
- Read and analyze a video feed
- Save the output with bounding boxes to `testing_videos/`

---

### ⚠️ Before running, update the following in `Testing_Script.py`:

```python
# ✅ Path to YOLO model weights
model = YOLO("model_training/weights/best.pt")  # ← update this path

# ✅ Path to input video
video_path = "testing_videos/input_clip.mp4"    # ← update this path
```

✅ You can also connect the output to an OCR or LPR model if running in parallel branches.

---

## 📚 Model Training

The model was trained using the YOLOv8m architecture from Ultralytics, using the `train_ev_yolov8.py` script:

```bash
cd ev_detection_yolov8m
python train_ev_yolov8.py
```

Training outputs (saved in `model_training/`) include:
- Confusion matrix & normalized confusion matrix
- Precision/Recall/F1-score curves
- Sample batch previews
- YOLO weights in `/weights/`

---

## 🚧 Notes

- This project assumes that only EVs are labeled. If a vehicle is not detected, it is considered **non-EV**.
- This branch includes EV detection only — the **LPR component** is maintained in a separate GitHub branch.

---

## 📜 License & Attribution

- Dataset: Custom-built EV dataset (web scraped and cleaned manually)
- Model: YOLOv8 by [Ultralytics](https://github.com/ultralytics/ultralytics)

---

## 🙌 Acknowledgements

This project was developed as part of a university capstone project to explore how computer vision can support sustainability through the automatic identification of electric vehicles, contributing to the development of EV charging station infrastructure in Qatar.

The pipeline was designed and implemented by **Adnan Abdelkarim**, a Data Science & AI undergraduate at the University of Doha for Science & Technology, as part of a team project.  
The EV Detection task was my individual responsibility and contribution.

---

