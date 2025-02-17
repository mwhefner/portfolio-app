import dash
from dash import html

"""dash.register_page(
    __name__, 
    path="/differential_geometry", 
    name="Differential Geometry Web Engine V2", 
    title="Differential Geometry Web Engine V2", 
    description="Extrensically and intrinsically visualize darboux-frames of embeded curves within abstract differentiable surfaces.", 
    image="/assets/as_webp/differential_geometry.webp"
)"""

layout = html.Div([
    html.H1("surf")
])