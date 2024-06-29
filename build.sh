#!/bin/bash

# Set variables
APP_NAME="screenshooter"
ENV_NAME="screenshooter_env"
SRC_DIR="src"
PYTHON_SCRIPT="$SRC_DIR/$APP_NAME.py"
REQUIREMENTS_FILE="requirements.txt"

# Create a new conda environment
echo "Creating a new conda environment..."
conda create -n $ENV_NAME python=3.9 -y

# Activate the conda environment
echo "Activating the conda environment..."
source activate $ENV_NAME

# Install dependencies
echo "Installing dependencies..."
pip install -r $REQUIREMENTS_FILE

# Generate hidden imports from requirements.txt
HIDDEN_IMPORTS=$(grep -oP '^[^=]+' $REQUIREMENTS_FILE | sed 's/^/--hidden-import=/')
HIDDEN_IMPORTS="$HIDDEN_IMPORTS --hidden-import=PIL._tkinter_finder --hidden-import=tkinter"

# Build the executable with hidden imports
echo "Building the executable with hidden imports..."
pyinstaller --onefile $HIDDEN_IMPORTS $PYTHON_SCRIPT --name=$APP_NAME

# Deactivate the conda environment
echo "Deactivating the conda environment..."
conda deactivate

echo "Build complete. The executable is located in the dist/ directory."
