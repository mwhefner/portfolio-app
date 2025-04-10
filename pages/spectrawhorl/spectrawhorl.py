import dash
from dash import html

# Tonetornado to be refactored here as spectrawhorl

dash.register_page(
    __name__, 
    path="/spectrawhorl", 
    name="tonetornado", 
    title="tonetornado", 
    description="tonetornado is a free and interactive web tool that circularly visualizes (and makes) sound (and useful overlays) for learning (and fun!)", 
    image="/assets/webp/thumbnails/tonetornado.webp"
)

layout = html.Div()