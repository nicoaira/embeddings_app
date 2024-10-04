import pandas as pd
from dash.dependencies import ClientsideFunction, Input, Output
import dash
from dash import dcc, html, Input, Output, callback, no_update
import base64
import pandas as pd
import plotly.express as px
import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


# Load your dataframe
df = pd.read_csv("structure_embeddings.csv")
df = df[df['rna_type'] != "tmRNA"]
df = df[df['rna_type'] != "ribozyme"]
unique_rna_types = df['rna_type'].unique()
num_categories = len(unique_rna_types)

def get_distinct_colors(n):
    colors = plt.get_cmap('tab20', n)
    return [mcolors.rgb2hex(colors(i)) for i in range(n)]

color_sequence = get_distinct_colors(num_categories)
color_discrete_map = dict(zip(unique_rna_types, color_sequence))

# Ensure 'rna_type' is of string type
df['rna_type'] = df['rna_type'].astype(str)
df['rna_type'] = df['rna_type'].astype(str).str.replace('_', ' ')

def capitalize_rnas(rna_type):
    if (rna_type == 'hammerhead ribozyme') |  (rna_type == 'ribozyme'):
        return rna_type.capitalize()
    elif (rna_type.startswith('RNase')) |  (rna_type.startswith('SRP')):
        return ' '.join(rna_type.split(' ')[:-1])
    else:
        return rna_type

df['rna_type'] = df['rna_type'].apply(capitalize_rnas)


df.rename(columns={'tSNE_1' : 'tSNE1', 'tSNE_2' : 'tSNE2', 'tSNE_3' : 'tSNE3'}, inplace=True)

# Create the 3D scatter plot using plotly.express with tSNE columns
fig = px.scatter_3d(
    df,
    x='tSNE1',
    y='tSNE2',
    z='tSNE3',
    color='rna_type',
    labels={'rna_type': 'RNA type'},  # Add this line
    custom_data=['rnacentral_id'],
    color_discrete_map=color_discrete_map,
)

# Adjust legend 
fig.update_layout(legend=dict(
    x=0.85,  # Adjust this value between 0 and 1; smaller values move the legend left
    y=0.9,   # Adjust this value between 0 and 1; smaller values move the legend down
    xanchor='left',
    font=dict(family="Courier", size=16, color="black"),  # Adjust the font size
    itemsizing='constant',  # Ensure consistent item sizing
    itemwidth=60,  # Increase this value to make the legend marker bigger
    )
)

fig.update_traces(
    hoverinfo='none',
    hovertemplate=None
    
)
fig.update_traces(marker=dict(size=3)) 

app = dash.Dash(__name__)

app.layout = html.Div(
    style={'width': '100vw', 'height': '100vh'},
    children=[
        dcc.Graph(
            id='3d-scatter',
            figure=fig,
            config={
                'toImageButtonOptions': {
                    'format': 'svg',  # Default export format to SVG
                    'filename': 'emmbeddings-plot',  
                    'height': 1200,  
                    'width': 1600,   
                    'scale': 1      
                }
            },
            style={'width': '100%', 'height': '100%'},
            clear_on_unhover=True
        ),
        dcc.Tooltip(id='graph-tooltip', direction='bottom'),
    ],
)

@app.callback(
    Output('graph-tooltip', 'show'),
    Output('graph-tooltip', 'bbox'),
    Output('graph-tooltip', 'children'),
    Input('3d-scatter', 'hoverData'),
)
def display_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update

    # Extract hover data
    hover_data = hoverData['points'][0]
    bbox = hover_data['bbox']  # Use bbox from hover data
    rnacentral_id = hover_data['customdata'][0]  # Get rnacentral_id from customdata

    # Construct the file path to the SVG image
    svg_file = f'./thumbnail_resize/{rnacentral_id}.thumbnail.svg'

    if not os.path.exists(svg_file):
        return False, no_update, no_update

    # Read and encode the SVG image
    with open(svg_file, 'rb') as f:
        svg_content = f.read()
    encoded_svg = base64.b64encode(svg_content).decode('utf-8')
    img_src = f'data:image/svg+xml;base64,{encoded_svg}'
    
    # Create the tooltip content
    children = [
        html.Div([
            html.Img(src=img_src),
            html.P(f"RNA Type: {rna_type}", style={'font-weight': 'bold'})
        ])  
    ]

    return True, bbox, children

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')

