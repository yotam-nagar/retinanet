#!/bin/bash

# ========================================================================
# Transfer Script to Remote Computer
# ========================================================================
# This script transfers the RetinaNet setup script to the remote computer
# and provides instructions for running it.
#
# Usage: ./transfer_to_remote.sh
# ========================================================================

REMOTE_USER="zoe"
REMOTE_HOST="172.31.100.94"
REMOTE_PATH="/home/zoe/"
SETUP_SCRIPT="setup_retinanet_environment.sh"

echo "========================================================================="
echo "Transferring RetinaNet Setup Script to Remote Computer"
echo "========================================================================="
echo ""
echo "Remote computer: $REMOTE_USER@$REMOTE_HOST"
echo "Target path: $REMOTE_PATH"
echo ""

# Check if setup script exists
if [ ! -f "$SETUP_SCRIPT" ]; then
    echo "Error: $SETUP_SCRIPT not found in current directory"
    exit 1
fi

# Transfer the script
echo "Transferring $SETUP_SCRIPT..."
scp "$SETUP_SCRIPT" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH"

if [ $? -eq 0 ]; then
    echo "✓ Script transferred successfully!"
    echo ""
    echo "========================================================================="
    echo "Next Steps:"
    echo "========================================================================="
    echo ""
    echo "1. SSH to the remote computer:"
    echo "   ssh $REMOTE_USER@$REMOTE_HOST"
    echo ""
    echo "2. Make the script executable:"
    echo "   chmod +x $SETUP_SCRIPT"
    echo ""
    echo "3. Run the setup script:"
    echo "   ./$SETUP_SCRIPT"
    echo ""
    echo "The script will:"
    echo "  - Install system dependencies (may require sudo password)"
    echo "  - Create virtual environment in: /home/zoe/My_Projects/venv/retinanet"
    echo "  - Set up RetinaNet project in: /home/zoe/My_Projects/test_cursor/retinanet"
    echo "  - Install all required packages with correct versions"
    echo "  - Verify the installation"
    echo ""
    echo "========================================================================="
else
    echo "✗ Transfer failed. Please check your SSH connection and try again."
    exit 1
fi 