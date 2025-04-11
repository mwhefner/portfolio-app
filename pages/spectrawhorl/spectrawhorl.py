"""

spectrawhorl.py

This script builds the spectrawhorl app's main page.

M W Hefner, 2025
MIT License

"""

from dash import register_page, html, dcc, clientside_callback, Input, Output, State, ClientsideFunction
import dash_bootstrap_components as dbc

register_page(
    __name__, 
    path="/spectrawhorl", 
    name="tonetornado", 
    title="tonetornado", 
    description="tonetornado is a free and interactive web tool that circularly visualizes (and makes) sound (and useful overlays) for learning (and fun!)", 
    image="/assets/webp/thumbnails/SpectraWhorl.webp"
)

layout = html.Div(
    
    children = [

        # A location object tracks the address bar url
        dcc.Location(id='spectrawhorl_url'),
        
        dcc.Store(id = "spectrawhorl_refresh_dummy_target"),
        
        # Help menu button
        dbc.Stack([
            dbc.Button(
                dbc.Col(html.I(className="fa-solid fa-question fs-2"), align="center"),
                id="spectrawhorl-help-button",
                color="primary",
                style={"borderRadius": "50%", "aspectRatio": "1 / 1"}
            )
        ], className="position-fixed bottom-0 start-0 m-3"),
        
        # help popover
        dbc.Popover(
            dbc.PopoverBody(html.Em("expand info modal")),
            target="spectrawhorl-help-button",
            trigger="hover",
            placement="right"
        ),
        
        # Help/information/welcome Modal
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Welcome")),
                dbc.ModalBody(
                    [
                        
                    dcc.Markdown("**SpectraWhorl**",
                        style={
                            "textAlign": "center", 
                            "fontSize": "3em",
                        }
                    ),
                    
                dbc.Carousel(
                    items=[
                        {"key": "6", "src": "/assets/webp/images/tonetornado_still.webp", "caption" : "The Harmonic Series at C3"},
                    ],
                    controls=True,
                    indicators=False,
                    className="carousel-fade",
                    interval=3000,
                ),
                    
                    ]
                ),
                dbc.ModalFooter(

                    dbc.Row([
                        dbc.Button(
                            "Close Info Modal",
                            id="close-spectrawhorl-help-modal",
                            className="ms-auto",
                            n_clicks=0,
                        )
                    ], justify="center", style={"textAlign": "center"}, className = "gap-3")

                ),
            ],
            id="spectrawhorl-help-modal",
            centered=True,
            size="lg"
        ),
        
        # Viewer
        html.Div(
            
            children=[
                
                # Fullscreen toggle
                html.Button([html.I(className="fa-solid fa-up-right-and-down-left-from-center"),], id = "fullscreenToggle", className = "B_TRANS",
                title = "Toggle fullscreen viewer"),
                
            ],
            
            id = "spectrawhorl_viewer"
        ),
    ]
)

# This callback creates, refreshes, or kills (when exiting) the sketch
clientside_callback(
    """
    function (path) {
        let sw = window.spectrawhorl_namespace;
        
        if (typeof spectrawhorl_sketch !== "undefined") {
            // This properly disposes of the old instance
            spectrawhorl_sketch.remove();
        }
        
        if (path === "/spectrawhorl") {
            // Create a fresh sketch
            spectrawhorl_sketch = new p5(sw.build_sketch);   
        }
        
        if (typeof spectrawhorl_sketch !== "undefined" && path !== "/spectrawhorl") {
            // Get rid of the instance if you leave the page
            spectrawhorl_sketch.remove();
        }
        
        return "";
    
    }    
    """,
    Output("spectrawhorl_refresh_dummy_target", "data"),
    Input("spectrawhorl_url", "pathname")
)

## Help modal open/close
clientside_callback(
    """
    function(n_clicks, n_2, is_open) {
        return !is_open;
    }
    """,
    Output("spectrawhorl-help-modal", "is_open"),
    [Input("spectrawhorl-help-button", "n_clicks"), Input("close-spectrawhorl-help-modal", "n_clicks")],
    State("spectrawhorl-help-modal", "is_open"),
    prevent_initial_call=True,
)
