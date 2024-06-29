# Screenshooter

Screenshooter is a simple tool for capturing screenshots on Linux. It allows users to quickly take rectagle selection screenshots and copy them to the clipboard.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)

## Features

- Capture screenshots with a single command.
- Save screenshots to a specified directory.
- Lightweight and fast.

## Installation

To install Screenshooter, follow these steps:

### Clone the repository
```bash
git clone https://github.com/CausticCatastrophe/screenshooter.git
cd screenshooter
```

### Build the application

Run the build.sh script to create the executable:
```bash
./build.sh
```

### Set up the application

Run the setup.sh script to install the application and create the desktop entry:
```bash
./setup.sh
```

# Usage

After installation, you can launch Screenshooter from your application menu or using the configured hotkey.
Configuration

To configure a hotkey for launching Screenshooter, follow these steps:

    Go to System Settings -> Shortcuts -> Custom Shortcuts.
    Create a new Command/URL shortcut.
    Set the command to the path of the Screenshooter executable (the path will be shown after running the setup script).

# License

Screenshooter is licensed under the MIT License. See the LICENSE file for more information.
