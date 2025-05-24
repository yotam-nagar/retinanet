import os
import json
import glob
from pathlib import Path
import cv2
import numpy as np

def validate_image(image_path):
    """Validate if an image can be read and has valid format."""
    try:
        img = cv2.imread(str(image_path))
        if img is None:
            return False, f"Could not read image: {image_path}"
        if len(img.shape) != 3 or img.shape[2] != 3:
            return False, f"Image must be RGB/BGR: {image_path}"
        return True, "Valid image"
    except Exception as e:
        return False, f"Error reading image {image_path}: {str(e)}"

def validate_annotation(annotation_path, image_path):
    """Validate if annotation file exists and has valid format."""
    try:
        if not os.path.exists(annotation_path):
            return False, f"Annotation file not found: {annotation_path}"
        with open(annotation_path, 'r') as f:
            annotation = json.load(f)
        if not os.path.exists(image_path):
            return False, f"Image file not found: {image_path}"
        img = cv2.imread(str(image_path))
        img_height, img_width = img.shape[:2]
        if 'shapes' not in annotation:
            return False, f"Annotation missing 'shapes' field: {annotation_path}"
        for shape in annotation['shapes']:
            if 'points' not in shape:
                return False, f"Shape missing 'points' field: {annotation_path}"
            if 'label' not in shape:
                return False, f"Shape missing 'label' field: {annotation_path}"
            points = np.array(shape['points'])
            if points.shape[0] != 2:
                return False, f"Invalid points format in {annotation_path}"
            x1, y1 = points[0]
            x2, y2 = points[1]
            if not (0 <= x1 < img_width and 0 <= x2 < img_width and 0 <= y1 < img_height and 0 <= y2 < img_height):
                return False, f"Bounding box outside image bounds in {annotation_path}"
            if x1 >= x2 or y1 >= y2:
                return False, f"Invalid bounding box coordinates in {annotation_path}"
        return True, "Valid annotation"
    except Exception as e:
        return False, f"Error validating annotation {annotation_path}: {str(e)}"

def check_data_structure(images_dir, labels_dir):
    print(f"\nChecking images: {images_dir}")
    print(f"Checking labels: {labels_dir}")
    if not os.path.exists(images_dir):
        print(f"Error: Images directory not found: {images_dir}")
        return False
    if not os.path.exists(labels_dir):
        print(f"Error: Labels directory not found: {labels_dir}")
        return False
    image_extensions = ['.jpg', '.jpeg', '.png']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(images_dir, f"*{ext}")))
        image_files.extend(glob.glob(os.path.join(images_dir, f"*{ext.upper()}")))
    if not image_files:
        print(f"Error: No image files found in {images_dir}")
        return False
    print(f"Found {len(image_files)} image files")
    valid_images = []
    valid_annotations = []
    class_names = set()
    errors = []
    for image_path in image_files:
        image_path = Path(image_path)
        label_path = Path(labels_dir) / image_path.with_suffix('.json').name
        img_valid, img_msg = validate_image(image_path)
        if not img_valid:
            errors.append(img_msg)
            continue
        ann_valid, ann_msg = validate_annotation(label_path, image_path)
        if not ann_valid:
            errors.append(ann_msg)
            continue
        valid_images.append(image_path)
        valid_annotations.append(label_path)
        with open(label_path, 'r') as f:
            annotation = json.load(f)
            for shape in annotation['shapes']:
                class_names.add(shape['label'])
    print("\nValidation Summary:")
    print(f"Total images found: {len(image_files)}")
    print(f"Valid images: {len(valid_images)}")
    print(f"Valid annotations: {len(valid_annotations)}")
    print(f"Classes found: {sorted(list(class_names))}")
    if errors:
        print("\nErrors found:")
        for error in errors:
            print(f"- {error}")
    return len(valid_images) > 0 and len(valid_annotations) > 0 and len(class_names) > 0

def main():
    data_root = "./data"
    splits = ['train', 'val', 'test']
    all_valid = True
    for split in splits:
        images_dir = os.path.join(data_root, 'images', split)
        labels_dir = os.path.join(data_root, 'labels', split)
        print(f"\n{'='*50}")
        print(f"Checking split: {split}")
        print(f"{'='*50}")
        if not check_data_structure(images_dir, labels_dir):
            all_valid = False
            print(f"\nData in split '{split}' does not meet requirements!")
        else:
            print(f"\nData in split '{split}' meets requirements!")
    if all_valid:
        print("\nAll splits meet the requirements for keras-retinanet training!")
    else:
        print("\nSome splits have issues that need to be fixed before training.")

if __name__ == '__main__':
    main() 