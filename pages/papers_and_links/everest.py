import dash
from dash import html

dash.register_page(
    __name__, 
    path="/everest", 
    name="The Real-Time Everest Weather Portal", 
    title="The Real-Time Everest Weather Portal", 
    description="Mountaineers use this low-bandwidth application on Mount Everest to gather real-time weather conditions at different camps on the mountain.", 
    image=""
)

layout = html.Div()