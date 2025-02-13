import dash
from dash import html

dash.register_page(
    __name__, 
    path="/differential_geometry", 
    name="Differential Geometry Engine V2", 
    title="Differential Geometry Engine V2", 
    description="Animate darboux-frames of embeded curves within abstract differentiable surfaces.", 
    image="/static/images/archive.png"
)

layout = html.Div([
    html.H1('This is our Archive page'),
    html.Div('This is our Archive page content.'),
])