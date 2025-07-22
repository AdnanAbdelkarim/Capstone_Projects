import os

# ✅ Your car class IDs (modify if needed)
CAR_CLASS_IDS = {2, 7}  # Set containing class ID 2 and class ID 7

# ✅ Path to your labels folder
LABELS_DIR = r'C:\Users\student\Desktop\train\labels'

# ✅ Counters
total_files = 0
files_modified = 0
total_detections_removed = 0

# ✅ Loop through label files
for label_file in os.listdir(LABELS_DIR):
    if not label_file.endswith('.txt'):
        continue

    total_files += 1
    file_path = os.path.join(LABELS_DIR, label_file)

    # Read all lines
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Filter car and class ID 7 detections
    filtered_lines = []
    removed_detections_in_file = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        class_id = int(line.split()[0])

        if class_id in CAR_CLASS_IDS:  # Check if class_id is 2 or 7
            filtered_lines.append(line + '\n')
        else:
            removed_detections_in_file += 1

    # ✅ If we removed any lines, overwrite the file
    if removed_detections_in_file > 0:
        with open(file_path, 'w') as f:
            f.writelines(filtered_lines)

        files_modified += 1
        total_detections_removed += removed_detections_in_file
        print(f"✅ Cleaned {removed_detections_in_file} non-car and non-class 7 detections from {label_file}")

# ✅ Summary
print("\n🚀 Cleaning Complete!")
print(f"📂 Total label files processed: {total_files}")
print(f"✅ Files modified (non-car and non-class 7 detections removed): {files_modified}")
print(f"❗ Total non-car and non-class 7 detections removed: {total_detections_removed}")
