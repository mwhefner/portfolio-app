import dash_bootstrap_components as dbc
from dash import html, Output, Input, dcc,clientside_callback,State, ClientsideFunction

# SURFACE

layout = html.Div(
    [
        
        dcc.Markdown(
            
            r"""

            #### Theory of Surfaces  

            Consider as the subject of study a **surface** $S$ defined by the parametric representation  

            $$
            S = \big( X(u,v), Y(u,v), Z(u,v) \big)
            $$

            where the parameters $u$ and $v$ range over  

            $$
            u \in \left[ u_{\text{start}}, u_{\text{end}} \right], \quad 
            v \in \left[ v_{\text{start}}, v_{\text{end}} \right].
            $$


            ***

            #### Directions

            WebDG will create a mesh numerical approximation of your surface using $n_u$ equally spaced intervals of the total $u$ interval and $n_v$ equally spaced intervals of the total $v$ interval.

            - Use the forms below to define these functions and values. 

            - Use "Parse" to have WebDG process, understand, and validate an input. 

            - Once all inputs have valid parses, use "Render Subject" at the bottom to begin computing the mesh approximation of your surface from the parsed inputs.

            ***

            #### Presets

            Using a preset means overwriting the form inputs below with the definitions for the selected preset surface. **Selecting 'Use' will erase any information currently in these forms.** Preset inputs must be parsed like any other.

            """, id="s_define", mathjax=True),

        # presets
        dbc.InputGroup(
            [
                
                dbc.InputGroupText("Presets"),
                
                dbc.Select(
                    options=[
                        {"label": "Plane", "value": "Plane"},
                        {"label": "Torus", "value": "Torus"},
                        {"label": "Helical Strake", "value": "Helical Strake"},
                        {"label": "Cone", "value": "Cone"},
                        {"label": 'Möbius Strip', "value": "Mobius"},
                        {"label": 'Enneper Surface', "value": "Enneper"},
                        {"label": "Dini's Surface", "value": "Dini"},
                        {"label": "Helicatenoid", "value": "Helicatenoid"},
                        {"label": '"Figure 8" Immersion of a Klein Bottle', "value": "Klein Bottle"},
                    ],
                    persistence=True,
                    persistence_type = "memory",
                    value="Plane", 
                    id="s_preset_select"
                ),
                
                dbc.Button("Use", id="s_use_preset", color="warning")
                
            ],
            
            className="mb-3"
            
        ),
        
        dcc.Markdown("***"),
        
        dcc.Markdown(r"""
                     
                     ### Surface Definition
                     
                     Given $S = \left( X(u,v), Y(u,v), Z(u,v) \right)$,
                     
                     define $S$ by defining $X(u,v)$, $Y(u,v)$, and $Z(u,v)$.
                     
                     """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Store(id="s_x_validated"),
        
        dbc.InputGroup(
            [
                dbc.InputGroupText(
                    dcc.Markdown("$X (u,v)=$", mathjax=True),
                    className = "LaTeX-p"
                ), 
                
                dbc.Input(value = "u", id="s_xcomponent", persistence=True, persistence_type = "memory"), 
                
                dbc.Button("Parse", color="info", id="s_xcomponent_parse")
                
            ],
            
            className="mb-3"
            
        ),
        
        dcc.Markdown(r"""
                     
                     $X$ (the $x$-component of the surface $S$) has been parsed as: 
                     
                     """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(r"Please parse input for $X$", id="s_xcomponent_formtext", 
            mathjax=True, 
            className="mx-4 text-wrap w-90",
            style={
                "textAlign": "center", 
                "fontSize": "1.5em",
                "overflowWrap": "break-word",  # Forces breaking long words
                "wordBreak": "break-word",  # Ensures breaking inside words if needed
                "whiteSpace": "normal",  # Allows wrapping instead of inline behavior
                "display": "block",  # Ensures it behaves as a block for better wrapping
                "maxWidth": "100%",  # Prevents overflow beyond container width
                "overflowX": "auto"  # Adds horizontal scrolling if necessary
            }
        ),
        
        dcc.Store(id="s_y_validated"),
        
        dbc.InputGroup(
            [
                dbc.InputGroupText(
                    dcc.Markdown("$Y (u,v)=$", mathjax=True),
                    className = "LaTeX-p"
                ), 
                
                dbc.Input(value = "v", id="s_ycomponent", persistence=True, persistence_type = "memory",), 
                
                dbc.Button("Parse", color="info", id="s_ycomponent_parse")
                
            ],
            
            className="mb-3"
            
        ),
        
        dcc.Markdown(r"""
                     
                     $Y$ (the $y$-component of the surface $S$) has been parsed as: 
                     
                     """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(r"Please parse input for $Y$", id="s_ycomponent_formtext", 
            mathjax=True, 
            className="mx-4 text-wrap w-90",
            style={
                "textAlign": "center", 
                "fontSize": "1.5em",
                "overflowWrap": "break-word",  # Forces breaking long words
                "wordBreak": "break-word",  # Ensures breaking inside words if needed
                "whiteSpace": "normal",  # Allows wrapping instead of inline behavior
                "display": "block",  # Ensures it behaves as a block for better wrapping
                "maxWidth": "100%",  # Prevents overflow beyond container width
                "overflowX": "auto"  # Adds horizontal scrolling if necessary
            }
        ),
        
        dcc.Store(id="s_z_validated"),
        
        dbc.InputGroup(
            [
                dbc.InputGroupText(
                    dcc.Markdown("$Z (u,v)=$", mathjax=True),
                    className = "LaTeX-p"
                ), 
                
                dbc.Input(value = "0", id="s_zcomponent", persistence=True, persistence_type = "memory",), 
                
                dbc.Button("Parse", color="info", id="s_zcomponent_parse")
                
            ],
            
            className="mb-3"
            
        ),
        
        dcc.Markdown(r"""
                     
                     $Z$ (the $z$-component of the surface $S$) has been parsed as: 
                     
                     """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(r"Please parse input for $Z$", id="s_zcomponent_formtext", 
            mathjax=True, 
            className="mx-4 text-wrap w-90",
            style={
                "textAlign": "center", 
                "fontSize": "1.5em",
                "overflowWrap": "break-word",  # Forces breaking long words
                "wordBreak": "break-word",  # Ensures breaking inside words if needed
                "whiteSpace": "normal",  # Allows wrapping instead of inline behavior
                "display": "block",  # Ensures it behaves as a block for better wrapping
                "maxWidth": "100%",  # Prevents overflow beyond container width
                "overflowX": "auto"  # Adds horizontal scrolling if necessary
            }
        ),
        
        dcc.Markdown("***"),
        
        dcc.Store(id="s_ustart_validated"),
        dcc.Store(id="s_uend_validated"),
        dcc.Store(id="s_nu_validated"),
        
        dcc.Markdown(r"""
                     
                     #### Define $u$
                     
                     """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dbc.InputGroup(
            [
                dbc.InputGroupText(
                    dcc.Markdown(r"$u_{\text{start}}=$", mathjax=True),
                    className = "LaTeX-p"
                ), 
                
                dbc.Input(value="-1", id="s_ustart", persistence=True, persistence_type = "memory",), 
                
                dbc.InputGroupText(
                    dcc.Markdown(r"$u_{\text{end}}=$", mathjax=True),
                    className = "LaTeX-p"
                ), 
                
                dbc.Input(value="1", id="s_uend", persistence=True, persistence_type = "memory",), 
                
                dbc.InputGroupText(
                    dcc.Markdown(r"$n_{u}=$", mathjax=True),
                    className = "LaTeX-p"
                ), 
                
                dbc.Input(id="s_nu", type="number", value=10, min=1, step=1, persistence=True, persistence_type = "memory",), 
                
                dbc.Button("Parse", color="info", id="s_u_parse")
                
            ],
            
            className="mb-3"
            
        ),
        
        dcc.Markdown(r"""
                     
                    These parameters for numerical evaluation must each evaluate to a constant. 
                    
                    `pi` and `e` are allowed constants. 
                    
                    For example: "`4.28`" and "`3 + 8 * pi`" are valid, but "`4t`" and "`x * y`" are not valid.
                    
                    $n_u$ must be a positive whole number.
                    
                    The $u$ numerical parameters have been parsed as:
                     
                    """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(r"Please parse input for $u_{\text{start}}$", id="s_ustart_formtext", 
            mathjax=True, 
            className="mx-4 text-wrap w-90",
            style={
                "textAlign": "center", 
                "fontSize": "1.5em",
                "overflowWrap": "break-word",  # Forces breaking long words
                "wordBreak": "break-word",  # Ensures breaking inside words if needed
                "whiteSpace": "normal",  # Allows wrapping instead of inline behavior
                "display": "block",  # Ensures it behaves as a block for better wrapping
                "maxWidth": "100%",  # Prevents overflow beyond container width
                "overflowX": "auto"  # Adds horizontal scrolling if necessary
            }
        ),
        
        dcc.Markdown(r"Please parse input for $u_{\text{end}}$", id="s_uend_formtext", 
            mathjax=True, 
            className="mx-4 text-wrap w-90",
            style={
                "textAlign": "center", 
                "fontSize": "1.5em",
                "overflowWrap": "break-word",  # Forces breaking long words
                "wordBreak": "break-word",  # Ensures breaking inside words if needed
                "whiteSpace": "normal",  # Allows wrapping instead of inline behavior
                "display": "block",  # Ensures it behaves as a block for better wrapping
                "maxWidth": "100%",  # Prevents overflow beyond container width
                "overflowX": "auto"  # Adds horizontal scrolling if necessary
            }
        ),
        
        dcc.Markdown(r"Please parse input for $n_u$", id="s_nu_formtext", 
            mathjax=True, 
            className="mx-4 text-wrap w-90",
            style={
                "textAlign": "center", 
                "fontSize": "1.5em",
                "overflowWrap": "break-word",  # Forces breaking long words
                "wordBreak": "break-word",  # Ensures breaking inside words if needed
                "whiteSpace": "normal",  # Allows wrapping instead of inline behavior
                "display": "block",  # Ensures it behaves as a block for better wrapping
                "maxWidth": "100%",  # Prevents overflow beyond container width
                "overflowX": "auto"  # Adds horizontal scrolling if necessary
            }
        ),
        
        dcc.Markdown("***"),
        
		dcc.Store(id="s_vstart_validated"),
        dcc.Store(id="s_vend_validated"),
        dcc.Store(id="s_nv_validated"),
            
        dcc.Markdown(r"""
                     
                     #### Define $v$
                     
                     """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dbc.InputGroup(
            [
                dbc.InputGroupText(
                    dcc.Markdown(r"$v_{\text{start}}=$", mathjax=True),
                    className = "LaTeX-p"
                ), 
                
                dbc.Input(value="-1", id="s_vstart", persistence=True, persistence_type = "memory",), 
                
                dbc.InputGroupText(
                    dcc.Markdown(r"$v_{\text{end}}=$", mathjax=True),
                    className = "LaTeX-p"
                ), 
                
                dbc.Input(value="1", id="s_vend", persistence=True, persistence_type = "memory",), 
                
                dbc.InputGroupText(
                    dcc.Markdown(r"$n_{v}=$", mathjax=True),
                    className = "LaTeX-p"
                ), 
                
                dbc.Input(id="s_nv", type="number", value=10, min=1, step=1, persistence=True, persistence_type = "memory",), 
                
                dbc.Button("Parse", color="info", id="s_v_parse")
                
            ],
            
            className="mb-3"
            
        ),
        
        dcc.Markdown(r"""
                     
                    These parameters for numerical evaluation must each evaluate to a constant. 
                    
                    `pi` and `e` are allowed constants. 
                    
                    For example: "`4.28`" and "`3 + 8 * pi`" are valid, but "`4t`" and "`x * y`" are not valid.
                    
                    $n_v$ must be a positive whole number.
                    
                    The $v$ numerical parameters have been parsed as:
                     
                    """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(r"Please parse input for $v_{\text{start}}$", id="s_vstart_formtext", 
            mathjax=True, 
            className="mx-4 text-wrap w-90",
            style={
                "textAlign": "center", 
                "fontSize": "1.5em",
                "overflowWrap": "break-word",  # Forces breaking long words
                "wordBreak": "break-word",  # Ensures breaking inside words if needed
                "whiteSpace": "normal",  # Allows wrapping instead of inline behavior
                "display": "block",  # Ensures it behaves as a block for better wrapping
                "maxWidth": "100%",  # Prevents overflow beyond container width
                "overflowX": "auto"  # Adds horizontal scrolling if necessary
            }
        ),
        
        dcc.Markdown(r"Please parse input for $v_{\text{end}}$", id="s_vend_formtext", 
            mathjax=True, 
            className="mx-4 text-wrap w-90",
            style={
                "textAlign": "center", 
                "fontSize": "1.5em",
                "overflowWrap": "break-word",  # Forces breaking long words
                "wordBreak": "break-word",  # Ensures breaking inside words if needed
                "whiteSpace": "normal",  # Allows wrapping instead of inline behavior
                "display": "block",  # Ensures it behaves as a block for better wrapping
                "maxWidth": "100%",  # Prevents overflow beyond container width
                "overflowX": "auto"  # Adds horizontal scrolling if necessary
            }
        ),
        
        dcc.Markdown(r"Please parse input for $n_v$", id="s_nv_formtext", 
            mathjax=True, 
            className="mx-4 text-wrap w-90",
            style={
                "textAlign": "center", 
                "fontSize": "1.5em",
                "overflowWrap": "break-word",  # Forces breaking long words
                "wordBreak": "break-word",  # Ensures breaking inside words if needed
                "whiteSpace": "normal",  # Allows wrapping instead of inline behavior
                "display": "block",  # Ensures it behaves as a block for better wrapping
                "maxWidth": "100%",  # Prevents overflow beyond container width
                "overflowX": "auto"  # Adds horizontal scrolling if necessary
            }
        ),
        
        ##dcc.Markdown("***"),
            
        dbc.InputGroup(
            [
                dbc.InputGroupText("Color surface by"),
                dbc.Select(
                    options=[
                        {"label": "UV coordinates.", "value": "uv"},
                        {"label": "XYZ coordinates.", "value": "xyz"},
                        {"label": "scene lighting.", "value": "lighting"},
                        {"label": "surface normal.", "value": "normal"},
                        {"label": "Gaussian curvature.", "value": "gaussian"},
                        {"label": "mean curvature.", "value": "mean"},
                        {"label": "principal curvature (k1)", "value": "k1"},
                        {"label": "principal curvature (k2)", "value": "k2"},
                    ],
                    value="lighting",
                    id="s_colorby",
                    className="flex-grow-1",
                )
            ],
            className="mb-3"
        ),

        dcc.Markdown("***"),
        
        dcc.Markdown("""               
                     The subject can be rendered when all inputs have been parsed and validated.""", id="s_render_ready_message", className="mx-4", style={"textAlign" : "center"}),

            
        dbc.Row(
            dbc.Col(dbc.Button("Render Subject", id="render_surface", color="warning", disabled=True), width="auto"),
            justify="center", className="m-4"
        ),
            
        # sure? preset Modal
        dbc.Modal(
            [

                dbc.ModalHeader(dbc.ModalTitle("Are you sure?")),
                dbc.ModalBody(
                    dcc.Markdown(
                        """
                        This operation will overwrite the existing surface form field inputs with the definitions of the selected preset surface. 
                        
                        **Are you sure you want to continue?**
                        
                        """
                    )
                ),
                dbc.ModalFooter(
                    className="d-flex justify-content-between w-100",
                    children=[
                        dbc.Button(
                            "Cancel",
                            id="cancel-s-sure-modal",
                            n_clicks=0,
                            color="success"
                        ),
                        dbc.Button(
                            "Continue",
                            id="continue-s-sure-modal",
                            n_clicks=0,
                            color="warning"
                        )
                    ]
                ),
            ],
            id="s-sure-modal",
            centered=True,
            size="sm"
        ),
        
    ]
)

clientside_callback(
    """
    function(button_click, preset) {
        if (button_click) {
            // Define the preset values in a simple data structure
            const preset_values = {
                "Plane": {
                    "s_xcomponent": "u",
                    "s_ycomponent": "v",
                    "s_zcomponent": "0",
                    "s_ustart": "-1",
                    "s_uend": "1",
                    "s_nu": 2,
                    "s_vstart": "-1",
                    "s_vend": "1",
                    "s_nv": 2
                },
                "Torus": {
                    "s_xcomponent": "(2 + cos(v)) * cos(u)",
                    "s_ycomponent": "(2 + cos(v)) * sin(u)",
                    "s_zcomponent": "sin(v)",
                    "s_ustart": "0",
                    "s_uend": "2 * pi",
                    "s_nu": 50,
                    "s_vstart": "0",
                    "s_vend": "2 * pi",
                    "s_nv": 50
                },
                "Helical Strake": {
                    "s_xcomponent": "v * cos(u)",
                    "s_ycomponent": "v * sin(u)",
                    "s_zcomponent": "u",
                    "s_ustart": "-4 * pi",
                    "s_uend": "4 * pi",
                    "s_nu": 300,
                    "s_vstart": "1",
                    "s_vend": "3",
                    "s_nv": 30
                },
                "Enneper": {
                    "s_xcomponent": "(1/3) * u * (1 - (1/3) * u^2 + v^2)",
                    "s_ycomponent": "(1/3) * v * (1 - (1/3) * v^2 + u^2)",
                    "s_zcomponent": "(1/3) * (u^2 - v^2)",
                    "s_ustart": "-2.5",
                    "s_uend": "2.5",
                    "s_nu": 75,
                    "s_vstart": "-2.5",
                    "s_vend": "2.5",
                    "s_nv": 75
                },
                "Dini": {
                    "s_xcomponent": "cos(u) sin(v)",
                    "s_ycomponent": "cos(v) log(tan(v/2)) + 0.2 u",
                    "s_zcomponent": "sin(u) sin(v)",
                    "s_ustart": "-8 pi",
                    "s_uend": "8 pi",
                    "s_nu": 200,
                    "s_vstart": "0.1",
                    "s_vend": "1",
                    "s_nv": 100
                },
                "Helicatenoid": {
                    "s_xcomponent": "cos(pi / 4) * (3 cosh( u / 3) cos(v)) + sin(pi / 4) * (3 * sinh(u / 3) sin(v))",
                    "s_ycomponent": "-cos(pi / 4) * (3 cosh( u / 3) cos(v)) + sin(pi / 4) * (3 * sinh(u / 3) cos(v))",
                    "s_zcomponent": "cos(pi / 4) * u + sin(pi / 4) * 3 v",
                    "s_ustart": "-pi",
                    "s_uend": "pi",
                    "s_nu": 200,
                    "s_vstart": "-2 pi",
                    "s_vend": "pi",
                    "s_nv": 100
                },
                "Mobius": {
                    "s_xcomponent": "3 * (1 + (v / 2) * cos((u) / 2)) * cos(u)",
                    "s_ycomponent": "3 * (1 + (v / 2) * cos(u / 2)) * sin(u)",
                    "s_zcomponent": "3 * (v / 2) * sin(u / 2)",
                    "s_ustart": "0",
                    "s_uend": "2 * pi",
                    "s_nu": 50,
                    "s_vstart": "-1",
                    "s_vend": "1",
                    "s_nv": 50
                },
                "Klein Bottle": {
                    "s_xcomponent": "(3 + cos(u / 2) * sin(v) - sin(u / 2) * sin(2 * v)) * cos(u)",
                    "s_ycomponent": "(3 + cos(u / 2) * sin(v) - sin(u / 2) * sin(2 * v)) * sin(u)",
                    "s_zcomponent": "sin(u / 2) * sin(v) + cos(u / 2) * sin(2 * v)",
                    "s_ustart": "0",
                    "s_uend": "2 * pi",
                    "s_nu": 60,
                    "s_vstart": "0",
                    "s_vend": "2 * pi",
                    "s_nv": 60
                },
                "Cone": {
                    "s_xcomponent": "(1 - (1 / 3) * u) * cos(v)",
                    "s_zcomponent": "(1 - (1 / 3) * u) * sin(v)",
                    "s_ycomponent": "u",
                    "s_ustart": "-3",
                    "s_uend": "2.75",
                    "s_nu": 20,
                    "s_vstart": "0",
                    "s_vend": "2 * pi",
                    "s_nv": 50
                }
            };
    
            // Get the values for the selected preset
            const values = preset_values[preset] || {};

            // Return the updated values
            return [
                values["s_xcomponent"] || "",
                values["s_ycomponent"] || "",
                values["s_zcomponent"] || "",
                values["s_ustart"] || "",
                values["s_uend"] || "",
                values["s_nu"] || "",
                values["s_vstart"] || "",
                values["s_vend"] || "",
                values["s_nv"] || ""
            ];
        }
        return [ "", "", "", "", "", "", "", "", "" ];
    }
    """,
    [
        Output("s_xcomponent", "value"),
        Output("s_ycomponent", "value"),
        Output("s_zcomponent", "value"),
        Output("s_ustart", "value"),
        Output("s_uend", "value"),
        Output("s_nu", "value"),
        Output("s_vstart", "value"),
        Output("s_vend", "value"),
        Output("s_nv", "value")
    ],
    [
        Input("continue-s-sure-modal", "n_clicks")
    ],
    [
        State("s_preset_select", "value")
    ],
    prevent_initial_call = True
)

## s-sure preset modal
clientside_callback(
    """
    function(n_clicks, n_2, n_3, is_open) {
        return !is_open;
    }
    """,
    Output("s-sure-modal", "is_open"),
    [Input("continue-s-sure-modal", "n_clicks"), Input("cancel-s-sure-modal", "n_clicks"), Input("s_use_preset", "n_clicks")],
    State("s-sure-modal", "is_open"),
    prevent_initial_call=True,
)

# surface component input callbacks
clientside_callback(
    r"""
    function(n_clicks, value) {
        
        let dg = window.dash_clientside.differential_geometry;
        
        let result = dg.parse_math("X(u,v)=", value, ["u", "v"]);
        
        function isValid(value) {
            return typeof value === "string" && value.startsWith("$$");
        }
        
        let valid = isValid(result);
        
        return [result, valid, !valid, valid ? value : "1"];
        
    }
    """,
    [Output("s_xcomponent_formtext", "children"),
    Output("s_xcomponent", "valid"),
    Output("s_xcomponent", "invalid"),
    Output("s_x_validated", "data")],
    Input("s_xcomponent_parse", "n_clicks"),
    State("s_xcomponent", "value"),
    prevent_initial_call=True
)

clientside_callback(
    r"""
    function(n_clicks, value) {
        
        let dg = window.dash_clientside.differential_geometry;
        
        let result = dg.parse_math("Y(u,v)=", value, ["u", "v"]);
        
        function isValid(value) {
            return typeof value === "string" && value.startsWith("$$");
        }
        
        let valid = isValid(result);
        
        return [result, valid, !valid, valid ? value : "1"];
        
    }
    """,
    [Output("s_ycomponent_formtext", "children"),
    Output("s_ycomponent", "valid"),
    Output("s_ycomponent", "invalid"),
    Output("s_y_validated", "data")],
    Input("s_ycomponent_parse", "n_clicks"),
    State("s_ycomponent", "value"),
    prevent_initial_call=True
)

clientside_callback(
    r"""
    function(n_clicks, value) {
        
        let dg = window.dash_clientside.differential_geometry;
        
        let result = dg.parse_math("Z(u,v)=", value, ["u", "v"]);
        
        function isValid(value) {
            return typeof value === "string" && value.startsWith("$$");
        }
        
        let valid = isValid(result);
        
        return [result, valid, !valid, valid ? value : "1"];
 
    }
    """,
    [Output("s_zcomponent_formtext", "children"),
    Output("s_zcomponent", "valid"),
    Output("s_zcomponent", "invalid"),
    Output("s_z_validated", "data")],
    Input("s_zcomponent_parse", "n_clicks"),
    State("s_zcomponent", "value"),
    prevent_initial_call=True
)

# for u
clientside_callback(
    r"""
    function(n_clicks, ts_value, te_value, nt_value) {
        let dg = window.dash_clientside.differential_geometry;
        
        ts_value = ts_value.trim();
        te_value = te_value.trim();
        
        let results = {
            ts: dg.parse_constant("u_{\\text{start}}=", ts_value, ["t"])[0],
            te: dg.parse_constant("u_{\\text{end}}=", te_value, ["t"])[0],
            nt: dg.parse_constant("n_u=", nt_value, ["t"])[0],
            START: dg.parse_constant("", ts_value, ["t"])[1],
            END: dg.parse_constant("", te_value, ["t"])[1],
            
        };
        
        function isValid(value) {
            return typeof value === "string" && value.startsWith("$");
        }

        return [
            results.ts, results.te, results.nt,
            isValid(results.ts) && results.START < results.END,
            isValid(results.te) && results.START < results.END,
            isValid(results.nt),
            !isValid(results.ts) || results.START >= results.END,
            !isValid(results.te) || results.START >= results.END,
            !isValid(results.nt),
            isValid(results.ts) && results.START < results.END ? ts_value : "0",
            isValid(results.te) && results.START < results.END ? te_value : "1",
            isValid(results.nt) ? nt_value : "1"
        ];
    }
    """,
    [
        Output("s_ustart_formtext", "children"),
        Output("s_uend_formtext", "children"),
        Output("s_nu_formtext", "children"),
        Output("s_ustart", "valid"),
        Output("s_uend", "valid"),
        Output("s_nu", "valid"),
        Output("s_ustart", "invalid"),
        Output("s_uend", "invalid"),
        Output("s_nu", "invalid"),
        Output("s_ustart_validated", "data"),
        Output("s_uend_validated", "data"),
        Output("s_nu_validated", "data")
    ],
    [
        Input("s_u_parse", "n_clicks")
    ],
    [
        State("s_ustart", "value"),
        State("s_uend", "value"),
        State("s_nu", "value"),
    ],
    prevent_initial_call=True
)

# for v
clientside_callback(
    r"""
    function(n_clicks, ts_value, te_value, nt_value) {
        let dg = window.dash_clientside.differential_geometry;
        
        ts_value = ts_value.trim();
        te_value = te_value.trim();
        
        let results = {
            ts: dg.parse_constant("v_{\\text{start}}=", ts_value, ["t"])[0],
            te: dg.parse_constant("v_{\\text{end}}=", te_value, ["t"])[0],
            nt: dg.parse_constant("n_v=", nt_value, ["t"])[0],
            START: dg.parse_constant("", ts_value, ["t"])[1],
            END: dg.parse_constant("", te_value, ["t"])[1],
            
        };
        
        function isValid(value) {
            return typeof value === "string" && value.startsWith("$");
        }

        return [
            results.ts, results.te, results.nt,
            isValid(results.ts) && results.START < results.END,
            isValid(results.te) && results.START < results.END,
            isValid(results.nt),
            !isValid(results.ts) || results.START >= results.END,
            !isValid(results.te) || results.START >= results.END,
            !isValid(results.nt),
            isValid(results.ts) && results.START < results.END ? ts_value : "0",
            isValid(results.te) && results.START < results.END ? te_value : "1",
            isValid(results.nt) ? nt_value : "1"
        ];
    }
    """,
    [
        Output("s_vstart_formtext", "children"),
        Output("s_vend_formtext", "children"),
        Output("s_nv_formtext", "children"),
        Output("s_vstart", "valid"),
        Output("s_vend", "valid"),
        Output("s_nv", "valid"),
        Output("s_vstart", "invalid"),
        Output("s_vend", "invalid"),
        Output("s_nv", "invalid"),
        Output("s_vstart_validated", "data"),
        Output("s_vend_validated", "data"),
        Output("s_nv_validated", "data")
    ],
    [
        Input("s_v_parse", "n_clicks")
    ],
    [
        State("s_vstart", "value"),
        State("s_vend", "value"),
        State("s_nv", "value"),
    ],
    prevent_initial_call=True
)

# render readiness callback
clientside_callback(
    """
    function(valid1, invalid1, valid2, invalid2, valid3, invalid3, valid4, invalid4, valid5, invalid5, valid6, invalid6, valid7, invalid7, valid8, invalid8, valid9, invalid9) {
        let allValid = valid1 && !invalid1 &&
                       valid2 && !invalid2 &&
                       valid3 && !invalid3 &&
                       valid4 && !invalid4 &&
                       valid5 && !invalid5 &&
                       valid6 && !invalid6 &&
                       valid7 && !invalid7 &&
                       valid8 && !invalid8 &&
                       valid9 && !invalid9;
                       
        let buttonDisabled = !allValid;
        let messageHidden = allValid ? "" : "The subject can be rendered when all inputs have been parsed and validated.";

        return [buttonDisabled, allValid ? "success" : "warning", messageHidden];
    }
    """,
    [
        Output("render_surface", "disabled"),
        Output("render_surface", "color"),
        Output("s_render_ready_message", "children")
    ],
    [
        Input("s_xcomponent", "valid"), Input("s_xcomponent", "invalid"),
        Input("s_ycomponent", "valid"), Input("s_ycomponent", "invalid"),
        Input("s_zcomponent", "valid"), Input("s_zcomponent", "invalid"),
        Input("s_ustart", "valid"), Input("s_ustart", "invalid"),
        Input("s_uend", "valid"), Input("s_uend", "invalid"),
        Input("s_nu", "valid"), Input("s_nu", "invalid"),
        Input("s_vstart", "valid"), Input("s_vstart", "invalid"),
        Input("s_vend", "valid"), Input("s_vend", "invalid"),
        Input("s_nv", "valid"), Input("s_nv", "invalid"),
    ]
)
