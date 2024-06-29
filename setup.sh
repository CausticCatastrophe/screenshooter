#!/bin/bash

# Set variables
APP_NAME="screenshooter"
DESKTOP_FILE="$APP_NAME.desktop"
SCRIPT_DIR=$(dirname "$(realpath "$0")")
EXECUTABLE_DIR="$SCRIPT_DIR/dist"
EXECUTABLE="$EXECUTABLE_DIR/$APP_NAME"
ICON_PATH="$SCRIPT_DIR/resources/icons/screenshooter.ico"
DESKTOP_FILE_PATH="$SCRIPT_DIR/$DESKTOP_FILE"

# Check if the executable exists
if [ ! -f "$EXECUTABLE" ]; then
    echo "Executable not found. Please run build.sh first."
    exit 1
fi

# Create the .desktop file
echo "Creating the .desktop file..."
cat > $DESKTOP_FILE_PATH <<EOL
[Desktop Entry]
Name=Screenshooter
Comment=Take a screenshot and copy to clipboard
Exec=$EXECUTABLE
Icon=$ICON_PATH
Terminal=false
Type=Application
Categories=Utility;
EOL

# Ensure the applications directory exists
mkdir -p ~/.local/share/applications/

# Copy the .desktop file to the applications directory
echo "Installing the .desktop file..."
cp $DESKTOP_FILE_PATH ~/.local/share/applications/

# Notify the user of successful installation
echo "Screenshooter has been installed successfully."
echo "You can launch it from your application menu or using the configured hotkey."

# Suggest setting up a hotkey
echo "To set up a hotkey, go to System Settings -> Shortcuts -> Custom Shortcuts, and create a new Command/URL shortcut with the command:"
echo "$EXECUTABLE"
