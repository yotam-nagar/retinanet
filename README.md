# RetinaNet Training Project

A comprehensive RetinaNet object detection training setup with automated environment configuration and data preparation tools.

## 🎯 Project Overview

This project provides a complete setup for training RetinaNet models using the [keras-retinanet](https://github.com/fizyr/keras-retinanet) framework. It includes automated environment setup scripts, data preparation tools, and comprehensive documentation for reproducible model training across different Linux systems.

## 📁 Project Structure

```
retinanet/
├── data_tools/                 # Data preparation and validation scripts
│   ├── yolo_to_retinanet_csv.py      # Convert YOLO annotations to RetinaNet CSV format
│   ├── validate_retinanet_csv.py     # Validate CSV annotation files
│   ├── data_validation.py            # Comprehensive data validation
│   └── prepare_data.py               # Data preparation utilities
├── data/                       # Training and validation data (excluded from git)
├── installtion/               # Installation and setup scripts
├── snapshots/                 # Model checkpoints (excluded from git)
├── tensorboard/              # TensorBoard logs (excluded from git)
├── keras-retinanet/          # Original keras-retinanet framework
└── .gitignore                # Git ignore rules
```

**Note**: The `data/` folder and all image/annotation files are excluded from Git to keep the repository lightweight. You'll need to add your training data separately.

## 🚀 Quick Start

### Prerequisites
- Linux system (Ubuntu/Debian, Fedora/CentOS/RHEL, or Arch)
- Python 3.8+
- Git

### Environment Setup

1. **Clone this repository:**
   ```bash
   git clone <your-repo-url>
   cd retinanet
   ```

2. **Run the automated setup script:**
   ```bash
   chmod +x installtion/setup_retinanet_environment_fixed.sh
   ./installtion/setup_retinanet_environment_fixed.sh
   ```

3. **Activate the environment:**
   ```bash
   source ~/My_Projects/venv/retinanet/bin/activate
   # Or use the convenience script:
   ./activate_retinanet.sh
   ```

## 📊 Data Preparation

### Data Management

Since the `data/` folder is excluded from Git, you need to set up your training data separately:

1. **Create the data directory:**
   ```bash
   mkdir -p data/train data/val
   ```

2. **Add your images and annotations:**
   ```bash
   # Copy your training images
   cp /path/to/your/images/* data/train/
   
   # Copy your validation images  
   cp /path/to/your/val_images/* data/val/
   ```

3. **Prepare annotation files:**
   - Place your CSV annotation files in the project root
   - Or use the conversion tools below

### Converting YOLO to RetinaNet Format

If you have YOLO-style annotations, use the conversion tool:

```bash
python data_tools/yolo_to_retinanet_csv.py
```

### Validating Your Data

Ensure your annotations are correctly formatted:

```bash
python data_tools/validate_retinanet_csv.py
python data_tools/data_validation.py
```

## 🏋️ Training

### Basic Training Command

```bash
python keras_retinanet/bin/train.py \
    --steps 1000 \
    --epochs 50 \
    --snapshot-path ./snapshots \
    --tensorboard-dir ./tensorboard \
    csv annotations.csv classes.csv
```

### Training Parameters

- `--steps`: Number of steps per epoch
- `--epochs`: Number of training epochs
- `--snapshot-path`: Directory to save model checkpoints
- `--tensorboard-dir`: Directory for TensorBoard logs
- `--batch-size`: Training batch size (default: 1)

## 📋 Environment Details

### Installed Packages

The setup script installs these specific versions for compatibility:

- **keras**: 2.12.0
- **tensorflow**: 2.12.0
- **keras-resnet**: 0.2.0
- **opencv-python**: 4.11.0.86
- **numpy**: 1.23.5
- **matplotlib**: 3.10.3
- **pillow**: 11.2.1
- **h5py**: 3.13.0
- **cython**: 3.1.1
- **pycocotools**: Latest (replaces problematic cocoapi)

### Virtual Environment

- **Location**: `~/My_Projects/venv/retinanet`
- **Activation**: `source ~/My_Projects/venv/retinanet/bin/activate`
- **Deactivation**: `deactivate`

## 🛠️ Development

### Adding New Data Tools

1. Create your script in the `data_tools/` directory
2. Follow the existing naming convention
3. Include proper documentation and error handling
4. Test with sample data before committing

### Environment Management

To recreate the environment on a new machine:

1. Use the setup script: `./installtion/setup_retinanet_environment_fixed.sh`
2. Or use pip with requirements: `pip install -r requirements_exact.txt`

## 🐛 Troubleshooting

### Common Issues

1. **Package Conflicts**: Use the exact versions specified in the setup script
2. **CUDA Issues**: Ensure compatible CUDA drivers for GPU training
3. **Import Errors**: Verify virtual environment is activated
4. **Memory Issues**: Reduce batch size or image resolution

### Getting Help

1. Check the environment setup notes in `installtion/`
2. Verify all packages are correctly installed: `pip list`
3. Test imports: `python -c "from keras_retinanet import models"`

## 📝 Notes

- Model checkpoints are saved in `snapshots/` (excluded from git)
- TensorBoard logs are in `tensorboard/` (excluded from git)
- Large data files should be stored separately or use Git LFS
- The setup script handles all dependency conflicts automatically

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project builds upon the keras-retinanet framework. Please refer to the original repository for licensing information.

## 🔗 References

- [keras-retinanet GitHub Repository](https://github.com/fizyr/keras-retinanet)
- [RetinaNet Paper](https://arxiv.org/abs/1708.02002)
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Keras Documentation](https://keras.io/) 