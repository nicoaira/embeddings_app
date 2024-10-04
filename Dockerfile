# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the app code to the container
COPY app.py /app/
COPY data/structure_embeddings.csv /app/
COPY data/thumbnail_resize /app/thumbnail_resize/

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install required Python libraries
RUN pip install --no-cache-dir dash plotly pandas matplotlib

# Expose the port the app runs on
EXPOSE 8050

# Run the app when the container launches
CMD ["python", "app.py"]
