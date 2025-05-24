import os
import csv

csv_files = [
    'data/annotations_train.csv',
    'data/annotations_val.csv',
    'data/annotations_test.csv'
]

valid_classes = {'dead', 'alive'}

def validate_csv(csv_path):
    total = 0
    valid = 0
    errors = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row_num, row in enumerate(reader, 1):
            total += 1
            if len(row) != 6:
                errors.append(f"Row {row_num}: Incorrect number of columns: {row}")
                continue
            image_path, x1, y1, x2, y2, class_name = row
            if not os.path.exists(image_path):
                errors.append(f"Row {row_num}: Image file does not exist: {image_path}")
                continue
            try:
                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)
            except ValueError:
                errors.append(f"Row {row_num}: Invalid coordinates: {row}")
                continue
            if not (x1 < x2 and y1 < y2 and x1 >= 0 and y1 >= 0 and x2 >= 0 and y2 >= 0):
                errors.append(f"Row {row_num}: Invalid bounding box: {row}")
                continue
            if class_name not in valid_classes:
                errors.append(f"Row {row_num}: Invalid class name: {class_name}")
                continue
            valid += 1
    print(f"\nValidation results for {csv_path}:")
    print(f"  Total rows: {total}")
    print(f"  Valid rows: {valid}")
    print(f"  Errors: {len(errors)}")
    if errors:
        print("  Example errors:")
        for err in errors[:10]:
            print(f"    - {err}")
    if len(errors) > 10:
        print(f"    ...and {len(errors)-10} more errors.")

if __name__ == '__main__':
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            validate_csv(csv_file)
        else:
            print(f"File not found: {csv_file}") 