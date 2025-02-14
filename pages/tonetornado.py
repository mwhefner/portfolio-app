import dash
from dash import html

dash.register_page(
    __name__, 
    path="/tonetornado", 
    name="tonetornado", 
    title="tonetornado", 
    description="tonetornado is a free and interactive web tool that circularly visualizes (and makes) sound (and useful overlays) for learning (and fun!)", 
    image="/assets/as_webp/tonetornado.webp"
)

layout = html.Div([

])