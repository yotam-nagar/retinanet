#!/usr/bin/env python3
"""
YOLO to RetinaNet CSV Converter

This script converts YOLO-style annotations to RetinaNet CSV format.
It processes images and labels from the data folder and creates:
- annotations_train.csv, annotations_val.csv, annotations_test.csv
- classes.csv

Expected directory structure:
data/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/

Usage:
    python data_tools/yolo_to_retinanet_csv.py
"""

import os
import glob
import cv2
import csv
import argparse
from collections import defaultdict

def load_class_names(class_names_file=None):
    """
    Load class names from file or use default mapping.
    
    Args:
        class_names_file (str): Path to file containing class names (one per line)
        
    Returns:
        dict: Mapping from class_id to class_name
    """
    if class_names_file and os.path.exists(class_names_file):
        class_map = {}
        with open(class_names_file, 'r') as f:
            for idx, line in enumerate(f):
                class_name = line.strip()
                if class_name:
                    class_map[str(idx)] = class_name
        return class_map
    else:
        # Default class mapping - modify this for your dataset
        return {
            "0": "dead",
            "1": "alive"
        }

def discover_classes_from_labels(labels_dirs):
    """
    Automatically discover class IDs from YOLO label files.
    
    Args:
        labels_dirs (list): List of label directories to scan
        
    Returns:
        set: Set of unique class IDs found
    """
    class_ids = set()
    
    for labels_dir in labels_dirs:
        if not os.path.exists(labels_dir):
            continue
            
        label_files = glob.glob(os.path.join(labels_dir, "*.txt"))
        for label_file in label_files:
            try:
                with open(label_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 5:  # class_id, x, y, w, h
                            class_ids.add(parts[0])
            except Exception as e:
                print(f"Warning: Could not read {label_file}: {e}")
    
    return class_ids

def create_classes_csv(class_map, output_path):
    """
    Create classes.csv file for RetinaNet.
    
    Args:
        class_map (dict): Mapping from class_id to class_name
        output_path (str): Path to save classes.csv
    """
    # Sort classes by ID for consistent ordering
    sorted_classes = sorted(class_map.items(), key=lambda x: int(x[0]))
    
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for class_id, class_name in sorted_classes:
            writer.writerow([class_name, class_id])
    
    print(f"Created classes.csv with {len(sorted_classes)} classes: {output_path}")
    for class_id, class_name in sorted_classes:
        print(f"  {class_id}: {class_name}")

def convert_yolo_to_retinanet(data_root="./data", class_names_file=None, splits=None):
    """
    Convert YOLO annotations to RetinaNet CSV format.
    
    Args:
        data_root (str): Root directory containing data
        class_names_file (str): Optional file containing class names
        splits (list): List of data splits to process
    """
    if splits is None:
        splits = ["train", "val", "test"]
    
    # Load or discover class mapping
    class_map = load_class_names(class_names_file)
    
    # Discover classes from labels if no class file provided
    if not class_names_file:
        labels_dirs = [os.path.join(data_root, "labels", split) for split in splits]
        discovered_classes = discover_classes_from_labels(labels_dirs)
        
        # Update class map with discovered classes
        for class_id in discovered_classes:
            if class_id not in class_map:
                class_map[class_id] = f"class_{class_id}"
    
    # Create classes.csv
    classes_csv_path = os.path.join(data_root, "classes.csv")
    create_classes_csv(class_map, classes_csv_path)
    
    # Process each split
    total_annotations = 0
    split_stats = {}
    
    for split in splits:
        images_dir = os.path.join(data_root, "images", split)
        labels_dir = os.path.join(data_root, "labels", split)
        output_csv = os.path.join(data_root, f"annotations_{split}.csv")
        
        if not os.path.exists(images_dir):
            print(f"Warning: Images directory not found: {images_dir}")
            continue
            
        if not os.path.exists(labels_dir):
            print(f"Warning: Labels directory not found: {labels_dir}")
            continue
        
        print(f"\nProcessing {split} split...")
        rows = []
        processed_images = 0
        skipped_images = 0
        
        # Find all image files
        image_files = []
        for ext in ["jpg", "jpeg", "png", "bmp", "tiff"]:
            image_files.extend(glob.glob(os.path.join(images_dir, f"*.{ext}")))
            image_files.extend(glob.glob(os.path.join(images_dir, f"*.{ext.upper()}")))
        
        for image_path in image_files:
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            label_path = os.path.join(labels_dir, image_name + ".txt")
            
            if not os.path.exists(label_path):
                skipped_images += 1
                continue  # Skip images with no label file
            
            # Load image to get dimensions
            img = cv2.imread(image_path)
            if img is None:
                print(f"Warning: Could not load image: {image_path}")
                skipped_images += 1
                continue
            
            img_h, img_w = img.shape[:2]
            processed_images += 1
            image_annotations = 0
            
            # Process YOLO annotations
            try:
                with open(label_path, "r") as f:
                    for line_num, line in enumerate(f, 1):
                        parts = line.strip().split()
                        if len(parts) != 5:
                            print(f"Warning: Invalid annotation format in {label_path}:{line_num}")
                            continue
                        
                        class_id, x_center, y_center, width, height = parts
                        
                        # Get class name
                        class_name = class_map.get(class_id, None)
                        if class_name is None:
                            print(f"Warning: Unknown class ID '{class_id}' in {label_path}:{line_num}")
                            continue
                        
                        # Convert YOLO format to absolute coordinates
                        try:
                            x_center = float(x_center) * img_w
                            y_center = float(y_center) * img_h
                            width = float(width) * img_w
                            height = float(height) * img_h
                            
                            # Convert to bounding box coordinates
                            x1 = int(x_center - width / 2)
                            y1 = int(y_center - height / 2)
                            x2 = int(x_center + width / 2)
                            y2 = int(y_center + height / 2)
                            
                            # Clamp to image bounds
                            x1 = max(0, x1)
                            y1 = max(0, y1)
                            x2 = min(img_w - 1, x2)
                            y2 = min(img_h - 1, y2)
                            
                            # Validate bounding box
                            if x2 <= x1 or y2 <= y1:
                                print(f"Warning: Invalid bounding box in {label_path}:{line_num}")
                                continue
                            
                            # Add to annotations (use absolute path for image)
                            rows.append([os.path.abspath(image_path), x1, y1, x2, y2, class_name])
                            image_annotations += 1
                            
                        except ValueError as e:
                            print(f"Warning: Invalid coordinate values in {label_path}:{line_num}: {e}")
                            continue
            
            except Exception as e:
                print(f"Error processing {label_path}: {e}")
                continue
        
        # Write CSV file
        with open(output_csv, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for row in rows:
                writer.writerow(row)
        
        # Statistics
        split_stats[split] = {
            'annotations': len(rows),
            'images_processed': processed_images,
            'images_skipped': skipped_images
        }
        total_annotations += len(rows)
        
        print(f"  Processed: {processed_images} images")
        print(f"  Skipped: {skipped_images} images")
        print(f"  Annotations: {len(rows)}")
        print(f"  Output: {output_csv}")
    
    # Summary
    print(f"\n{'='*50}")
    print("CONVERSION SUMMARY")
    print(f"{'='*50}")
    print(f"Total annotations: {total_annotations}")
    print(f"Classes: {len(class_map)}")
    print(f"Output files:")
    print(f"  - {classes_csv_path}")
    for split in splits:
        if split in split_stats:
            annotations_file = os.path.join(data_root, f"annotations_{split}.csv")
            print(f"  - {annotations_file} ({split_stats[split]['annotations']} annotations)")

def main():
    parser = argparse.ArgumentParser(description="Convert YOLO annotations to RetinaNet CSV format")
    parser.add_argument("--data-root", default="./data", 
                       help="Root directory containing images and labels folders (default: ./data)")
    parser.add_argument("--class-names", 
                       help="File containing class names (one per line)")
    parser.add_argument("--splits", nargs="+", default=["train", "val", "test"],
                       help="Data splits to process (default: train val test)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.data_root):
        print(f"Error: Data root directory not found: {args.data_root}")
        return
    
    print(f"Converting YOLO annotations to RetinaNet CSV format...")
    print(f"Data root: {args.data_root}")
    print(f"Splits: {args.splits}")
    
    convert_yolo_to_retinanet(
        data_root=args.data_root,
        class_names_file=args.class_names,
        splits=args.splits
    )

if __name__ == "__main__":
    main() 