import dash
from dash import html

dash.register_page(
    __name__, 
    path="/ggea", 
    name="The Carbon Dioxide Information Analysis Center at AppState Dashboard", 
    title="The Carbon Dioxide Information Analysis Center at AppState Dashboard", 
    description="Interactively visualize sources of CO₂ emissions worldwide from fossil fuel and cement manufacture.", 
    image="/assets/ggea.png"
)

layout = html.Div()