#!/bin/bash

# Check if Docker is installed
if ! [ -x "$(command -v docker)" ]; then
  echo 'Error: Docker is not installed.' >&2
  exit 1
fi

# Check if the Docker image already exists
IMAGE_EXISTS=$(docker images -q embeddings-app)

if [ -n "$IMAGE_EXISTS" ]; then
    read -p "Docker image 'embeddings-app' already exists. Do you want to rebuild it? (y/n): " REBUILD_CHOICE
    if [ "$REBUILD_CHOICE" = "y" ]; then
        echo "Rebuilding the Docker image..."
        docker build -t embeddings-app .
        if [ $? -ne 0 ]; then
          echo "Error: Docker build failed."
          exit 1
        fi
    else
        echo "Using the existing Docker image."
    fi
else
    echo "Building the Docker image for the first time..."
    docker build -t embeddings-app .
    if [ $? -ne 0 ]; then
      echo "Error: Docker build failed."
      exit 1
    fi
fi

# Run the Docker container
docker run -p 8050:8050 embeddings-app
if [ $? -ne 0 ]; then
  echo "Error: Failed to run Docker container."
  exit 1
fi
