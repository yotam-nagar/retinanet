import os
import glob
import cv2
import csv

# Class mapping
yolo_class_map = {"0": "dead", "1": "alive"}

splits = ["train", "val", "test"]
data_root = "./data"

for split in splits:
    images_dir = os.path.join(data_root, "images", split)
    labels_dir = os.path.join(data_root, "labels", split)
    output_csv = os.path.join(data_root, f"annotations_{split}.csv")
    rows = []
    image_files = []
    for ext in ["jpg", "jpeg", "png"]:
        image_files.extend(glob.glob(os.path.join(images_dir, f"*.{ext}")))
        image_files.extend(glob.glob(os.path.join(images_dir, f"*.{ext.upper()}")))
    for image_path in image_files:
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        label_path = os.path.join(labels_dir, image_name + ".txt")
        if not os.path.exists(label_path):
            continue  # skip images with no label file
        img = cv2.imread(image_path)
        if img is None:
            continue
        img_h, img_w = img.shape[:2]
        with open(label_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
                class_id, x_center, y_center, width, height = parts
                class_name = yolo_class_map.get(class_id, None)
                if class_name is None:
                    continue
                x_center = float(x_center) * img_w
                y_center = float(y_center) * img_h
                width = float(width) * img_w
                height = float(height) * img_h
                x1 = int(x_center - width / 2)
                y1 = int(y_center - height / 2)
                x2 = int(x_center + width / 2)
                y2 = int(y_center + height / 2)
                # Clamp to image bounds
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(img_w - 1, x2)
                y2 = min(img_h - 1, y2)
                rows.append([os.path.abspath(image_path), x1, y1, x2, y2, class_name])
    # Write CSV
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow(row)
    print(f"Wrote {len(rows)} rows to {output_csv}") 