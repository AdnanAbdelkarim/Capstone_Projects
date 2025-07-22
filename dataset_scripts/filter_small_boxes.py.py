import os

labels_dir = r'C:\Users\student\Desktop\train\labels'
min_area = 0.01  # Anything below this will be removed

for filename in os.listdir(labels_dir):
    if filename.endswith('.txt'):
        file_path = os.path.join(labels_dir, filename)

        with open(file_path, 'r') as f:
            lines = f.readlines()

        filtered_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue  # Skip invalid lines

            _, _, _, w, h = map(float, parts)
            area = w * h
            if area >= min_area:
                filtered_lines.append(line)

        # Overwrite file with filtered detections
        with open(file_path, 'w') as f:
            f.writelines(filtered_lines)

print("Small detections removed.")
