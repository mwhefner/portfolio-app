import dash_bootstrap_components as dbc
from dash import html, callback, Output, Input, dcc, html, clientside_callback, State

layout = dbc.Card(
    [
        dbc.CardBody(
            html.Div(
                
                children = [
                    dcc.Store(id = "settings_target"),
                    
                    dcc.Markdown("### Background",className="my-4"),
                    
                    dbc.Switch(
                        id="show_solid_bg",
                        label="Solid Background Color",
                        value=True,
                        disabled=False,
                        style={'user-select': 'none',"fontSize": "1.5em",},
                        className="my-2"
                    ),
                    
                    dbc.Label(
                        "Background Color",
                        className="pb-0 mb-0",
                        style={'user-select': 'none',"fontSize": "1.5em",},
                    ),
                    
                    dbc.Input(
                        type="color",
                        id="bg_colorpicker",
                        value="#2e2e2e",
                        className="p-0 mb-4",
                        style={"width": "100%", "height": 100, 'user-select': 'none', "fontSize": "1.5em",}
                    ),
                    
                    dcc.Markdown("***\n### Movement",className="my-4"),
                    
                    dbc.Switch(
                        id="show_focal_point",
                        label="Show Focal Point",
                        value=True,
                        disabled=False,
                        style={'user-select': 'none', "fontSize": "1.5em",},
                        className="my-2"
                    ),
                    
                    dbc.Label(
                        "Speed",
                        className="pb-0 mb-0",
                        style={'user-select': 'none',"fontSize": "1.5em",},
                    ),
                    
                    dcc.Slider(
                        min=0.1, 
                        max=20, 
                        step=0.1, 
                        value=5, 
                        id='movement_speed',
                        marks=None,  # Removes labeled marks
                        tooltip={"always_visible": False},  # Optional: Hide tooltip
                        className="webdg_slider my-2"  # Add the class
                    ),
                    
                    dcc.Markdown("***\n### Space",className="my-4"),
                    
                    dbc.Switch(
                        id="show_axes",
                        label="Show Axes Indicator and Orienting (X-Z) Plane",
                        value=True,
                        disabled=False,
                        style={'user-select': 'none', "fontSize": "1.5em",},
                        className="my-2"
                    ),
                    
                    dbc.Label(
                        "Display Scale",
                        className="pb-0 mb-0",
                        style={'user-select': 'none',"fontSize": "1.5em",},
                    ),
                    
                    dcc.Slider(
                        min=1, 
                        max=300, 
                        step=1, 
                        value=100, 
                        id='displayScaleSlider',
                        marks=None,  # Removes labeled marks
                        tooltip={"always_visible": False},  # Optional: Hide tooltip
                        className="webdg_slider my-2"  # Add the class
                    ),
                    
                    dcc.Markdown(
                        "***\n### Curves",
                        className="my-4"
                    ),
                    
                    dbc.Label(
                        "Curve Width",
                        className="pb-0 mb-0",
                        style={'user-select': 'none',"fontSize": "1.5em",},
                    ),
                    
                    dcc.Slider(
                        min=0.1, 
                        max=40, 
                        step=0.1, 
                        value=4, 
                        id='curveWidthSlider',
                        marks=None,  # Removes labeled marks
                        tooltip={"always_visible": False},  # Optional: Hide tooltip
                        className="webdg_slider my-2"  # Add the class
                    ),
                    
                    # TNB SELECTION

                    dbc.InputGroup(
                        [
                            dbc.InputGroupText(
                                dcc.Markdown("Curves' Frenet-Serret frames are "),
                                className = "LaTeX-p"
                            ), 
                            
                            dbc.Select(
                                options=[
                                    {"label": "not shown.", "value": "hide"},
                                    {"label": "static.", "value": "anchor"},
                                    {"label": "animated.", "value": "animated"},
                                ],
                                value="hide",
                                id="tnb_select",
                                className="flex-grow-1",
                                # controlled with callback in analytics.py
                                disabled=True
                            ),
                            
                        ],
                        
                        className="mb-4"
                        
                    ),
                    
                    dcc.Markdown(
                        "Compute analytics for a curve to enable the Frenet-Serret Frame feature.",
                        style={
                            "textAlign": "center", 
                            "overflowWrap": "break-word",  # Forces breaking long words
                            "wordBreak": "break-word",  # Ensures breaking inside words if needed
                            "whiteSpace": "normal",  # Allows wrapping instead of inline behavior
                            "display": "block",  # Ensures it behaves as a block for better wrapping
                            "maxWidth": "100%",  # Prevents overflow beyond container width
                            "overflowX": "auto"  # Adds horizontal scrolling if necessary
                    }, id="tnb_info"),
                    
                    # anchor location
                    
                    dcc.Store(id="tnb_anchor_target"),
                    
                    html.Div(
                        [
                        dbc.Label(
                            dcc.Markdown("Anchor Frenet-Serret Frame at $t=$",mathjax=True),
                            className="pb-0 mb-0",
                            style={'user-select': 'none',"fontSize": "1.5em",},
                            id="tnb_anchor_label"
                        ),
                        
                        dcc.Slider(
                            
                            # updated with callback in analytics.py
                            min=0.1, 
                            max=40, 
                            step=0.1, 
                            value=10, 
                            
                            
                            id='TNB_t_slider',
                            marks=None,  # Removes labeled marks
                            tooltip={"always_visible": True},  # Optional: Hide tooltip
                            className="webdg_slider mb-2 mt-4"  # Add the class
                        ),
                        ],
                        id="tnb_anchor_wrapper",  # Wrapper div for this section
                    ),
            
                    # animation speed
                    html.Div(
                        [
                            dbc.Label(
                                dcc.Markdown("Frenet-Serret Frame Animation Speed"),
                                className="pb-0 mb-0",
                                style={'user-select': 'none',"fontSize": "1.5em",},
                                id="tnb_animation_label"
                            ),
                            
                            dcc.Slider(
                                min=1, 
                                max=10, 
                                step=1, 
                                value=10, 
                                id='TNB_speed_slider',
                                marks=None,  # Removes labeled marks
                                tooltip={"always_visible": False},  # Optional: Hide tooltip
                                className="webdg_slider my-2"  # Add the class
                            ),
                        ],
                        id="tnb_animation_wrapper",  # Wrapper div for this section
                    ),
                    
                    dcc.Markdown("***\n### Surfaces",className="my-4"),
                    
                    dbc.Label(
                        dcc.Markdown("Shine"),
                        className="pb-0 mb-0",
                        style={'user-select': 'none',"fontSize": "1.5em",}
                    ),
                            
                    dcc.Slider(
                        min=0, 
                        max=50, 
                        step=1, 
                        value=10, 
                        id='surfaceShine',
                        marks=None,  # Removes labeled marks
                        tooltip={"always_visible": False},  # Optional: Hide tooltip
                        className="webdg_slider my-2"  # Add the class
                    ),
                    
                    dcc.Markdown("***\n### Lighting",className="my-4"),
                    
                    dbc.Label(
                        "Ambient Light",
                        className="pb-0 mb-0",
                        style={'user-select': 'none',"fontSize": "1.5em",},
                    ),
                    
                    dbc.Input(
                        type="color",
                        id="ambient_light_colorpicker",
                        value="#646464",
                        className="p-0 mb-4",
                        style={"width": "100%", "height": 100, 'user-select': 'none', "fontSize": "1.5em",}
                    ),
                    
                    dbc.Label(
                        "Positive X-Axis Directional Light",
                        className="pb-0 mb-0",
                        style={'user-select': 'none',"fontSize": "1.5em",},
                    ),
                    
                    dbc.Input(
                        type="color",
                        id="x_light_colorpicker",
                        value="#FF0000",
                        className="p-0 mb-4",
                        style={"width": "100%", "height": 100, 'user-select': 'none', "fontSize": "1.5em",}
                    ),
                    
                    dbc.Label(
                        "Positive Y-Axis Directional Light",
                        className="pb-0 mb-0",
                        style={'user-select': 'none',"fontSize": "1.5em",},
                    ),
                    
                    dbc.Input(
                        type="color",
                        id="y_light_colorpicker",
                        value="#00FF00",
                        className="p-0 mb-4",
                        style={"width": "100%", "height": 100, 'user-select': 'none', "fontSize": "1.5em",}
                    ),
                    
                    dbc.Label(
                        "Positive Z-Axis Directional Light",
                        className="pb-0 mb-0",
                        style={'user-select': 'none',"fontSize": "1.5em",},
                    ),
                    
                    dbc.Input(
                        type="color",
                        id="z_light_colorpicker",
                        value="#0000FF",
                        className="p-0 mb-4",
                        style={"width": "100%", "height": 100, 'user-select': 'none', "fontSize": "1.5em",}
                    ),
                    
                    # end settings children
                    
                ],
                id="settings-content", 
                className="card-text"
            )
        ),
        
        
    ],
    
    className = "px-0"
    
)

clientside_callback(
    """
    function(TNB_anchor_slider, TNB_speed_slider) {
        let dg = window.dash_clientside.differential_geometry;
        
        dg.TNB_anchor_slider = TNB_anchor_slider;
        
        dg.TNB_speed_slider = TNB_speed_slider;
        
        return "";
    }
    """,
    Output("tnb_anchor_target", "data"),
    Input('TNB_t_slider', "value"),
    Input('TNB_speed_slider', "value"),
    
)

clientside_callback(
    """
    function(tnb_select_is_disabled, tnb_select_value, data){
        
        let dg = window.dash_clientside.differential_geometry;
        
        dg.TNB_select_disabled = tnb_select_is_disabled;
        
        dg.TNB_select = tnb_select_value;
        
        if (data) {
            dg.TNB_data = data;
            //console.log(data);
        }
        
        const hide = {'display': 'none'};
        const show = {'display': 'block'};
        
        if (tnb_select_is_disabled) {
            
            return [show, hide, hide];
            
        } else if(tnb_select_value == "hide") {
            
            return [hide, hide, hide];
            
        } else if(tnb_select_value == "anchor") {
            
            return [hide, show, hide];
            
        } else if(tnb_select_value == "animated") {
            
            return [hide, hide, show];
            
        }
        
        return [show, hide, hide]; // default
    }
    """,
    [
        Output("tnb_info", "style"),
        
        Output("tnb_anchor_wrapper", "style"),
        
        Output("tnb_animation_wrapper", "style"),
    ],
    
    Input("tnb_select", "disabled"),
    Input("tnb_select", "value"),
    Input("c_kappa_tau_plot_data", "data")
)

clientside_callback(
    """
    function(show_solid_bg, bg_colorpicker_value, show_axes, displayScaleSlider_value, curveWidthSlider_value, movement_speed, show_focal_point, surfaceShine, ambient_light_colorpicker, x_light_colorpicker, y_light_colorpicker, z_light_colorpicker){
        
        let dg = window.dash_clientside.differential_geometry;
        
        dg.movementSpeed = movement_speed;
        
        dg.showBackground = show_solid_bg;
        
        dg.backgroundColor = bg_colorpicker_value;
        
        dg.showAxis = show_axes;
        
        dg.scaler = displayScaleSlider_value;
        
        dg.strokeW = curveWidthSlider_value;
        
        dg.showFocalPoint = show_focal_point;
        
        dg.surfaceShine = surfaceShine;
        
        dg.ambient_light = dg.hexToRGB(ambient_light_colorpicker);
        dg.x_light = dg.hexToRGB(x_light_colorpicker);
        dg.y_light = dg.hexToRGB(y_light_colorpicker);
        dg.z_light = dg.hexToRGB(z_light_colorpicker);

        
        return ""; // empty return, no need to actually store anything
    }
    """,
    Output("settings_target", "data"),
    Input("show_solid_bg", "value"),
    Input("bg_colorpicker", "value"),
    Input("show_axes", "value"),
    Input("displayScaleSlider", "value"),
    Input("curveWidthSlider", "value"),
    Input("movement_speed", "value"),
    Input("show_focal_point", "value"),
    Input("surfaceShine", "value"),
    Input("ambient_light_colorpicker", "value"),
    Input("x_light_colorpicker", "value"),
    Input("y_light_colorpicker", "value"),
    Input("z_light_colorpicker", "value"),
)