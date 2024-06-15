#!/bin/bash

# Check for Python 3 and pip3 installation
if ! command -v python3 &> /dev/null; then
    echo "Python 3 could not be found. Please install Python 3."
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "pip3 could not be found. Please install pip3."
    exit 1
fi

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required dependencies
pip install -r requirements.txt

echo "Setup complete. To run the application, use 'source venv/bin/activate' and then 'python game.py'."
