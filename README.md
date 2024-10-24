# Embeddings Visualization App

This application visualizes RNA secondary structure embeddings in a 3D scatter plot using t-SNE dimensionality reduction. The plot is interactive, and secondary structure of each RNA point are displayed when hovering over them. The app is built using [Dash](https://plotly.com/dash/) and packaged with Docker for ease of deployment.


https://github.com/user-attachments/assets/ad5d9bbc-dc46-4089-b139-913e50a49ee1

---

## Prerequisites

- Ensure that [Docker](https://www.docker.com/products/docker-desktop) is installed on your machine. You can check by running the following command in your terminal:
  
  ```bash
  docker --version
  ```
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
  ./run_app.sh --input <path_to_input_file> --color_column <column_name> [options]
  ```
The script will check if the Docker image already exists. If not, it will build the image for the first time.
The app will start, and you should see a message like:

```
Dash is running on http://0.0.0.0:8050/
```

You can Ctrl+Left click on the link to open it in your browser
 

## Example Command

Here's an example of how to run the app:

  ```bash
  ./run_app.sh --input /home/user/data/embeddings.tsv --color_column Cluster --jitter --categorical
  ```

## Available Options


*   `--input`: Path to the input CSV or TSV file containing t-SNE data. (Required)
*   `--color_column`: Column name in the data file to use for coloring the points. (Required)
*   `--show_svgs`: Option to show SVGs of RNA secondary structures when hovering over points. If not provided, thumbnails are displayed.
*   `--categorical`: Forces the color column to be treated as categorical even if the column contains numeric values.
*   `--jitter`: Adds a small random perturbation to the points to prevent overlap if some points have identical coordinates in 3D space.


## Input File Format

The input file must be either a CSV or TSV file, and it should contain the following columns:

*   `tSNE_1`: First t-SNE dimension
*   `tSNE_2`: Second t-SNE dimension
*   `tSNE_3`: Third t-SNE dimension
*   `color_column`: The column you want to use for coloring the points

## Features

1.  **Interactive 3D Plot**: The RNA embeddings are visualized in a 3D scatter plot, allowing zoom, pan, and rotate actions for better exploration.
    
2.  **Hover Functionality**: When hovering over a data point, the RNA secondary structure is displayed either as a thumbnail or as an SVG based on the `--show_svgs` option.
    
3.  **Categorical vs Continuous Coloring**: By default, the app automatically determines whether the `color_column` should be treated as categorical or continuous. The `--categorical` option forces it to be treated as categorical, even for numeric columns.
    
4.  **Jittering to Prevent Overlap**: The `--jitter` option introduces a small random perturbation (1% of the range in each t-SNE dimension) to prevent points with identical coordinates from overlapping.
