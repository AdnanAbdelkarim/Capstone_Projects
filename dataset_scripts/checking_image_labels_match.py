import os

# Set your images and labels folders
IMAGES_DIR = r'C:\Users\student\Desktop\EV_MODEL\dataset\train\images'
LABELS_DIR = r'C:\Users\student\Desktop\EV_MODEL\dataset\train\labels'

# Collect base filenames (without extension)
image_files = {os.path.splitext(f)[0] for f in os.listdir(IMAGES_DIR) if f.endswith(('.jpg', '.png'))}
label_files = {os.path.splitext(f)[0] for f in os.listdir(LABELS_DIR) if f.endswith('.txt')}

# Find mismatches
images_without_labels = image_files - label_files
labels_without_images = label_files - image_files

# Report
print(f"✅ Total images found: {len(image_files)}")
print(f"✅ Total labels found: {len(label_files)}\n")

if images_without_labels:
    print(f"⚠️ Images without corresponding labels ({len(images_without_labels)}):")
    for img in images_without_labels:
        print(f" - {img}")
else:
    print("✅ All images have corresponding labels.")

if labels_without_images:
    print(f"\n⚠️ Labels without corresponding images ({len(labels_without_images)}):")
    for lbl in labels_without_images:
        print(f" - {lbl}")
else:
    print("✅ All labels have corresponding images.")
