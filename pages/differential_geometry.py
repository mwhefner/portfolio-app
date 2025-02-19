import dash
from dash import html, dcc, Input, Output, clientside_callback, register_page, ClientsideFunction
import dash_bootstrap_components as dbc

"""register_page(
    __name__, 
    path="/differential_geometry", 
    name="Differential Geometry Web Engine V2", 
    title="Differential Geometry Web Engine V2", 
    description="Extrensically and intrinsically visualize darboux-frames of embeded curves within abstract differentiable surfaces.", 
    image="/assets/as_webp/differential_geometry.webp"
)"""

clientside_callback(
    """
    function(n_clicks) {
        console.log("Button pressed.");
    }
    """,
    Output("DGWE_Store", "data"),
    Input("DGWE_start", "n_clicks"),
    prevent_initial_call=True 
)

layout = html.Div(
    [
        
        html.Div(id = "DGWE_Store", style={'display' : 'none'}),
        
        dcc.Store(id = "dummy"),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("(Re-) Start Engine", id="re_start_engine", color="primary", n_clicks=0, style={"width": "100%"}),
                    width=True, className="m-4"
                ),
                dbc.Col(
                    dbc.Button("Toggle Animation", id="toggle_animation", color="primary", n_clicks=0, style={"width": "100%"}),
                    width=True, className="m-4"
                ),
                dbc.Col(
                    dbc.Button("Lines & Surfaces", id="lines_and_surfaces", color="primary", n_clicks=0, style={"width": "100%"}),
                    width=True, className="m-4"
                ),
                dbc.Col(
                    dbc.Button("Fe-line Surf-er", id="kitty", color="primary", n_clicks=0, style={"width": "100%"}),
                    width=True, className="m-4"
                ),
            ],
            justify="space-between"
        ),

        # Scroll container (takes up remaining height)
        html.Div(
            [
                html.Div(id="DGWE_Canvas_Parent", style={'width':'100%', 'height' : '100%'}),
            ],
            id="no-scroll-container",
            className="p-0 m-0",
            style={
                "flex": "1",  # This makes it take up remaining space
                "width": "100%",
                "height": "100%",
                "minHeight" : 0
            }
        ),
        
    ],
    
    style={
        "display": "flex",
        "flexDirection": "column",
        "height": "100vh"  # Makes the whole app take up the full viewport height
    }
)

clientside_callback(
    ClientsideFunction(namespace="differential_geometry", function_name="create_sketch"),
    Output("dummy", "data"),
    Input("re_start_engine", "n_clicks"),
    prevent_initial_call=True  # This stops it from running on page load
)

