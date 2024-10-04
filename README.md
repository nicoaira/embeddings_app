# Embeddings Visualization App

This application visualizes RNA embeddings in a 3D scatter plot using t-SNE dimensionality reduction. The plot is interactive, and additional details about each point are displayed when hovering over them. The app is built using [Dash](https://plotly.com/dash/) and packaged with Docker for ease of deployment.

---

## Prerequisites

- Ensure that [Docker](https://www.docker.com/products/docker-desktop) is installed on your machine. You can check by running the following command in your terminal:
  
  ```bash
  docker --version
  
  ---

## Running the App

1. Clone the repository or download the app folder.

2. Open a terminal and navigate to the app directory:

  ```bash
  cd embeddings_app
  ```
  
 3. Make the run_app.sh executable:
  
  ```bash
  chmod +x run_app.sh
  ```
 
 4. Run the setup script: 
 
  ```bash
  ./run_app.sh
  ```
The script will check if the Docker image already exists. If not, it will build the image for the first time.
The app will start, and you should see a message like:

```
Dash is running on http://0.0.0.0:8050/
```

You can Ctrl+Left click on the link to open it in your browser
 

