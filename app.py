import pandas as pd
from dash import dcc, html, Input, Output, callback, no_update
import dash
import plotly.express as px
import argparse
import os
import base64
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Run the t-SNE Embeddings Visualization App.')
parser.add_argument('--input', required=True, help='Path to the input CSV/TSV file containing tSNE data.')
parser.add_argument('--color_column', required=True, help='Column name to use for coloring the points.')
parser.add_argument('--show_svgs', action='store_true', help='Whether to display SVGs or thumbnails on hover.')
args = parser.parse_args()

# Load the input dataframe
if args.input.endswith('.csv'):
    df = pd.read_csv(args.input)
elif args.input.endswith('.tsv'):
    df = pd.read_csv(args.input, sep='\t')
else:
    raise ValueError("Input file must be a CSV or TSV file.")

# Ensure required columns exist
required_columns = ['tSNE_1', 'tSNE_2', 'tSNE_3']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Input file must contain the column: {col}")

# Rename columns for consistency
df.rename(columns={'tSNE_1': 'tSNE1', 'tSNE_2': 'tSNE2', 'tSNE_3': 'tSNE3'}, inplace=True)

# Ensure color column exists
if args.color_column not in df.columns:
    raise ValueError(f"Color column '{args.color_column}' not found in input file.")

color_column = args.color_column

# Determine if the color column is categorical or continuous
if pd.api.types.is_numeric_dtype(df[color_column]):
    color_type = 'continuous'
else:
    color_type = 'categorical'

# Generate colors for categorical data if needed
if color_type == 'categorical':
    unique_categories = df[color_column].unique()
    num_categories = len(unique_categories)
    colors = plt.get_cmap('tab20', num_categories)
    color_sequence = [mcolors.rgb2hex(colors(i)) for i in range(num_categories)]
    color_discrete_map = dict(zip(unique_categories, color_sequence))
else:
    color_sequence = None
    color_discrete_map = None

# Create the 3D scatter plot using plotly.express with tSNE columns
fig = px.scatter_3d(
    df,
    x='tSNE1',
    y='tSNE2',
    z='tSNE3',
    color=color_column,
    labels={color_column: color_column},
    custom_data=['rnacentral_id'] if 'rnacentral_id' in df.columns else None,
    color_discrete_map=color_discrete_map if color_type == 'categorical' else None,
    color_continuous_scale='Viridis' if color_type == 'continuous' else None,
)

# Adjust legend if categorical
if color_type == 'categorical':
    fig.update_layout(legend=dict(
        x=0.85,
        y=0.9,
        xanchor='left',
        font=dict(family="Courier", size=16, color="black"),
        itemsizing='constant',
        itemwidth=60,
    ))

fig.update_traces(
    hoverinfo='none',
    hovertemplate=None,
    marker=dict(size=3)
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(
    style={'width': '100vw', 'height': '100vh'},
    children=[
        html.Div(
            style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'},
            children=[
                # Add the RadioItems for SVG/Thumbnails option if enabled
                html.Div(
                    style={'padding': '10px'},
                    children=[
                        dcc.RadioItems(
                            id='structure-type',
                            options=[
                                {'label': 'Thumbnails', 'value': 'thumbnails'},
                                {'label': 'Svg', 'value': 'svg'}
                            ],
                            value='thumbnails',
                            labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                        )
                    ]
                ) if args.show_svgs else None,
                # Add the 3D plot
                html.Div(
                    style={'width': '100%', 'height': '85vh'},
                    children=[
                        dcc.Graph(
                            id='3d-scatter',
                            figure=fig,
                            config={
                                'toImageButtonOptions': {
                                    'format': 'svg',
                                    'filename': 'embeddings-plot',
                                    'height': 1200,
                                    'width': 1600,
                                    'scale': 1
                                }
                            },
                            style={'width': '100%', 'height': '100%'},
                            clear_on_unhover=True
                        ),
                    ]
                ),
            ]
        ),
        # Tooltip component if SVGs/Thumbnails are enabled
        dcc.Tooltip(id='graph-tooltip', direction='bottom') if args.show_svgs else None,
    ],
)

# Define callback for hover behavior if SVG/Thumbnails are enabled
if args.show_svgs:
    @app.callback(
        Output('graph-tooltip', 'show'),
        Output('graph-tooltip', 'bbox'),
        Output('graph-tooltip', 'children'),
        Input('3d-scatter', 'hoverData'),
        Input('structure-type', 'value'),
    )
    def display_hover(hoverData, structure_type):
        if hoverData is None:
            return False, no_update, no_update

        hover_data = hoverData['points'][0]
        bbox = hover_data['bbox']
        rnacentral_id = hover_data['customdata'][0] if 'customdata' in hover_data else None

        if not rnacentral_id:
            return False, no_update, no_update

        svg_file = f'./thumbnail_resize/{rnacentral_id}.thumbnail.svg' if structure_type == 'thumbnails' else f'./svg_resize/{rnacentral_id}.colored.svg'

        if not os.path.exists(svg_file):
            return False, no_update, no_update

        with open(svg_file, 'rb') as f:
            svg_content = f.read()
        encoded_svg = base64.b64encode(svg_content).decode('utf-8')
        img_src = f'data:image/svg+xml;base64,{encoded_svg}'

        children = [
            html.Div([
                html.Img(src=img_src),
                html.P(f"RNA Type: {rnacentral_id}", style={'font-weight': 'bold'})
            ])
        ]

        return True, bbox, children

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')