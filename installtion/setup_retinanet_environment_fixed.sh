#!/bin/bash

# ========================================================================
# RetinaNet Environment Setup Script (FIXED VERSION)
# ========================================================================
# This script automates the complete setup of a RetinaNet training environment
# on a Linux system, incorporating all the lessons learned and corrections
# from the original manual setup process.
#
# Usage: ./setup_retinanet_environment_fixed.sh
# ========================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration - Updated for remote computer zoe@172.31.100.94
PROJECT_DIR="/home/zoe/My_Projects/test_cursor"
VENV_DIR="/home/zoe/My_Projects/venv/retinanet"
REPO_URL="https://github.com/fizyr/keras-retinanet.git"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect Linux distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo $ID
    elif [ -f /etc/redhat-release ]; then
        echo "rhel"
    elif [ -f /etc/debian_version ]; then
        echo "debian"
    else
        echo "unknown"
    fi
}

# Function to install system dependencies
install_system_deps() {
    print_status "Installing system dependencies..."
    
    DISTRO=$(detect_distro)
    
    case $DISTRO in
        ubuntu|debian)
            print_status "Detected Ubuntu/Debian system"
            sudo apt update
            sudo apt install -y build-essential python3-dev python3-pip python3-venv git
            ;;
        fedora|centos|rhel)
            print_status "Detected RedHat-based system"
            sudo dnf install -y gcc gcc-c++ python3-devel python3-pip git
            ;;
        arch|manjaro)
            print_status "Detected Arch-based system"
            sudo pacman -S --noconfirm python base-devel git
            ;;
        *)
            print_warning "Unknown distribution. Please install manually:"
            print_warning "- build tools (gcc, make)"
            print_warning "- python3-dev/python3-devel"
            print_warning "- python3-pip"
            print_warning "- git"
            read -p "Press Enter to continue after installing dependencies..."
            ;;
    esac
    
    print_success "System dependencies installed"
}

# Function to create project structure
create_project_structure() {
    print_status "Creating project directory structure..."
    
    # Create main project directory
    mkdir -p "$PROJECT_DIR"
    cd "$PROJECT_DIR"
    
    # Remove existing retinanet directory if it exists
    if [ -d "retinanet" ]; then
        print_warning "Existing retinanet directory found, removing..."
        rm -rf retinanet
    fi
    
    # Clone repository
    print_status "Cloning keras-retinanet repository..."
    git clone "$REPO_URL" retinanet
    
    cd retinanet
    print_success "Project structure created and repository cloned"
}

# Function to create virtual environment
create_virtual_environment() {
    print_status "Creating virtual environment..."
    
    # Create venv directory
    mkdir -p "$(dirname "$VENV_DIR")"
    
    # Remove existing environment if it exists
    if [ -d "$VENV_DIR" ]; then
        print_warning "Existing virtual environment found, removing..."
        rm -rf "$VENV_DIR"
    fi
    
    # Create new virtual environment
    python3 -m venv "$VENV_DIR"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Verify activation
    if [ "$VIRTUAL_ENV" = "$VENV_DIR" ]; then
        print_success "Virtual environment created and activated"
    else
        print_error "Failed to activate virtual environment"
        exit 1
    fi
}

# Function to upgrade pip
upgrade_pip() {
    print_status "Upgrading pip..."
    pip install --upgrade pip
    print_success "Pip upgraded to version $(pip --version)"
}

# Function to install core dependencies
install_core_dependencies() {
    print_status "Installing core dependencies..."
    
    # Install numpy first (required for many other packages)
    print_status "Installing numpy..."
    pip install numpy==1.23.5
    
    # Install core ML framework dependencies in specific order
    print_status "Installing keras and tensorflow..."
    pip install keras==2.12.0
    pip install tensorflow==2.12.0
    
    print_success "Core dependencies installed"
}

# Function to install keras-retinanet dependencies
install_retinanet_dependencies() {
    print_status "Installing keras-retinanet dependencies..."
    
    # Install keras-resnet (depends on keras being installed first)
    print_status "Installing keras-resnet..."
    pip install keras-resnet==0.2.0
    
    # Install computer vision and utility packages
    print_status "Installing OpenCV and other packages..."
    pip install opencv-python==4.11.0.86
    pip install progressbar2==4.5.0
    
    # Install additional required packages
    print_status "Installing additional packages..."
    pip install matplotlib==3.10.3
    pip install pillow==11.2.1
    pip install h5py==3.13.0
    pip install cython==3.1.1
    
    # Install COCO API (use pre-built version to avoid compilation issues)
    print_status "Installing pycocotools..."
    pip install pycocotools
    
    print_success "All dependencies installed"
}

# Function to install keras-retinanet package
install_keras_retinanet() {
    print_status "Installing keras-retinanet package..."
    
    # Make sure we're in the correct retinanet directory (the cloned repo)
    cd "$PROJECT_DIR/retinanet"
    
    # Verify we have setup.py
    if [ ! -f "setup.py" ]; then
        print_error "setup.py not found in $(pwd)"
        print_error "This suggests the repository was not cloned correctly"
        exit 1
    fi
    
    # Install keras-retinanet in development mode
    pip install -e .
    
    print_success "keras-retinanet package installed"
}

# Function to create data tools directory
create_data_tools() {
    print_status "Creating data tools directory..."
    
    cd "$PROJECT_DIR/retinanet"
    mkdir -p data_tools
    
    print_success "Data tools directory created"
}

# Function to create activation script
create_activation_script() {
    print_status "Creating environment activation script..."
    
    cd "$PROJECT_DIR/retinanet"
    
    cat > activate_retinanet.sh << 'EOF'
#!/bin/bash
echo "Activating RetinaNet environment..."
source /home/zoe/My_Projects/venv/retinanet/bin/activate
cd /home/zoe/My_Projects/test_cursor/retinanet
echo "Environment activated. Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Virtual environment: $VIRTUAL_ENV"
echo ""
echo "To deactivate, run: deactivate"
EOF
    
    chmod +x activate_retinanet.sh
    
    print_success "Activation script created: $PROJECT_DIR/retinanet/activate_retinanet.sh"
}

# Function to verify installation
verify_installation() {
    print_status "Verifying installation..."
    
    # Test import of key modules
    python -c "
import sys
try:
    import keras
    import tensorflow as tf
    import cv2
    import numpy as np
    from keras_retinanet import models
    
    print('✓ All core packages imported successfully')
    print(f'✓ TensorFlow version: {tf.__version__}')
    print(f'✓ Keras version: {keras.__version__}')
    print(f'✓ OpenCV version: {cv2.__version__}')
    print(f'✓ NumPy version: {np.__version__}')
    print('✓ Environment setup complete!')
    
except ImportError as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        print_success "All packages verified successfully!"
    else
        print_error "Package verification failed"
        exit 1
    fi
}

# Function to create requirements file
create_requirements_file() {
    print_status "Creating requirements file..."
    
    cd "$PROJECT_DIR/retinanet"
    pip freeze > requirements_exact.txt
    
    print_success "Requirements file created: requirements_exact.txt"
}

# Function to display final instructions
display_final_instructions() {
    echo ""
    echo "========================================================================="
    print_success "RetinaNet Environment Setup Complete!"
    echo "========================================================================="
    echo ""
    echo "To activate the environment in the future, run:"
    echo "  source $VENV_DIR/bin/activate"
    echo "  cd $PROJECT_DIR/retinanet"
    echo ""
    echo "Or use the convenience script:"
    echo "  $PROJECT_DIR/retinanet/activate_retinanet.sh"
    echo ""
    echo "Project structure:"
    echo "  - Main directory: $PROJECT_DIR/retinanet"
    echo "  - Virtual environment: $VENV_DIR"
    echo "  - Data tools: $PROJECT_DIR/retinanet/data_tools"
    echo "  - Requirements: $PROJECT_DIR/retinanet/requirements_exact.txt"
    echo ""
    echo "Next steps:"
    echo "  1. Prepare your training data"
    echo "  2. Configure model parameters"
    echo "  3. Start training with: python keras_retinanet/bin/train.py"
    echo ""
    echo "========================================================================="
}

# Main execution
main() {
    echo "========================================================================="
    echo "RetinaNet Environment Setup Script (FIXED VERSION)"
    echo "========================================================================="
    echo ""
    
    # Check if running as root
    if [ "$EUID" -eq 0 ]; then
        print_error "Please do not run this script as root"
        exit 1
    fi
    
    # Check for Python 3
    if ! command_exists python3; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    print_status "Starting RetinaNet environment setup..."
    print_status "Python version: $(python3 --version)"
    print_status "Target directory: $PROJECT_DIR"
    print_status "Virtual environment: $VENV_DIR"
    echo ""
    
    # Ask for confirmation
    read -p "Do you want to proceed with the installation? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Installation cancelled"
        exit 0
    fi
    
    # Execute setup steps
    install_system_deps
    create_project_structure
    create_virtual_environment
    upgrade_pip
    install_core_dependencies
    install_retinanet_dependencies
    install_keras_retinanet
    create_data_tools
    create_activation_script
    verify_installation
    create_requirements_file
    display_final_instructions
    
    print_success "Setup completed successfully!"
}

# Run main function
main "$@" 