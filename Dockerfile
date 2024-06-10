# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
        libgl1-mesa-glx \
        libegl1-mesa \
        libxkbcommon-x11-0 \
        libxcb-xinerama0 \
        libxcb-xinput0 \
        libxcb-randr0 \
        libxcb-xkb1 \
        libxcb-render0 \
        libxkbcommon0 \
        libx11-xcb1 \
        libfontconfig1 \
        libglib2.0-0 \
        libdbus-1-3 \
        libxcb-cursor0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the default command to run the application
CMD ["python", "game.py"]
