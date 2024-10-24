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

# Parse the command-line arguments
INPUT_FILE=""
COLOR_COLUMN=""
SHOW_SVGS_FLAG=""
CATEGORICAL_FLAG=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --input) INPUT_FILE="$2"; shift ;;
        --color_column) COLOR_COLUMN="$2"; shift ;;
        --show_svgs) SHOW_SVGS_FLAG="--show_svgs" ;;
        --categorical) CATEGORICAL_FLAG="--categorical" ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Check if the input file is provided
if [ -z "$INPUT_FILE" ]; then
  echo "Error: You must specify an input file using --input."
  exit 1
fi

# Get the full path of the input file
FULL_INPUT_PATH=$(realpath "$INPUT_FILE")

# Get the directory containing the input file
HOST_DIR=$(dirname "$FULL_INPUT_PATH")

# Run the Docker container, mounting the directory containing the input file
docker run -v "$HOST_DIR":/app/data -p 8050:8050 embeddings-app \
    --input /app/data/$(basename "$FULL_INPUT_PATH") \
    --color_column "$COLOR_COLUMN" \
    $SHOW_SVGS_FLAG \
    $CATEGORICAL_FLAG

if [ $? -ne 0 ]; then
  echo "Error: Failed to run Docker container."
  exit 1
fi
