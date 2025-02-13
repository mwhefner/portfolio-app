import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

dash.register_page(
    __name__, 
    path="/nyt_best_sellers", 
    name="New York Times Best Sellers: Fiction", 
    title="New York Times Best Sellers: Fiction", 
    description="Explore the history of New York Times' Best-Selling Fiction.", 
    image=""
)

# Read the CSV and treat ISBN as a string to prevent conversion errors
df = pd.read_csv("bestsellers.csv", dtype={'ISBN': 'str'})

# Convert ISBN to integer, ignoring errors and converting invalid values to NaN
df['ISBN'] = pd.to_numeric(df['ISBN'], errors='coerce')

# If you want to drop rows with NaN ISBN (optional):
df = df.dropna(subset=['ISBN'])

# Convert ISBN to int after handling invalid values (if any)
df['ISBN'] = df['ISBN'].astype('int64')

# Get the unique week numbers
unique_weeks = df['Week'].unique()

# Sort the weeks in descending order
sorted_weeks = sorted(unique_weeks, reverse=True)

# Select the last 52 weeks
last_52_weeks = sorted_weeks[:52]

df = df[df['Week'].isin(last_52_weeks)]

# Define your figure
fig = go.Figure(data=go.Scatter(
    x=df['x'],
    y=df['y'],
    mode='markers'
))

# Update layout to remove background, grid, axes, etc.
fig.update_layout(
    width=72600,
    dragmode=False,  # Disable dragging (zooming, panning)
    xaxis=dict(
        showgrid=False,  # Hide grid lines
        zeroline=False,  # Hide the zero line
        showticklabels=False,  # Hide tick labels
        visible=False  # Hide x-axis
    ),
    yaxis=dict(
        showgrid=False,  # Hide grid lines
        zeroline=False,  # Hide the zero line
        showticklabels=False,  # Hide tick labels
        visible=False  # Hide y-axis
    ),
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot area background
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent surrounding area
    # hovermode=False,  # Disable hover interactions
    height=2100,
    margin=dict(
        l=50,  # Left padding
        r=50,  # Right padding
        t=50,  # Top padding
        b=50   # Bottom padding
    ),
)

image_url = "https://covers.openlibrary.org/b/isbn/"  # Replace with your actual image URL
images = []

# Iterate through each row of the dataframe
for i, row in df.iterrows():
    
    x = row['x']  # Get x from the record
    y = row['y']  # Get y from the record
    isbn = row['ISBN']  # Get isbn from the record

    images.append(
        dict(
            source=image_url + str(isbn) + "-M.jpg",
            x=x,
            y=y,
            xref="x",
            yref="y",
            sizex=20,  # Set the image size
            sizey=20,
            opacity=1,
            layer="above"
        )
    )

fig.update_layout(images=images)

layout = html.Div([
    html.Div(
        dcc.Graph(figure=fig, id="sankey"),
        style={"width": "1200px", 'height' : '100vh'}  # Make the graph wider
    )
], style={"width": "100%", "overflowX": "auto", "border": "1px solid black", "white-space": "nowrap", "overflow-y": "hidden"})

