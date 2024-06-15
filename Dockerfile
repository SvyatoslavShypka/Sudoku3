# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variable to non-interactive
ENV DEBIAN_FRONTEND=noninteractive

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libxkbcommon-x11-0 \
    x11-apps \
    libxcb-cursor-dev \
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
    libxcb-xinerama0 \
    libxkbcommon-x11-0 \
    libxcb-xinerama0 \

    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set display environment variable
ENV DISPLAY=:0

# Run the application
CMD ["python", "game.py"]
