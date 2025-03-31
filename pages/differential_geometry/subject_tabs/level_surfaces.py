import dash_bootstrap_components as dbc
from dash import html, Output, Input, dcc,clientside_callback,State, ClientsideFunction

# Minimal Surfaces

layout = html.Div([
    
    dcc.Markdown(
        r"""
        #### Level Surfaces (a.k.a. "Isosurfaces" or "Implicit Surfaces")

        Consider as the subject of study a **level surface** $S$ defined implicitly by the equation

        $$
        F(x,y,z)=0
        $$

        bounded in space by

        $$
        x \in \left[ x_{\text{start}}, x_{\text{end}} \right], \quad 
        y \in \left[ y_{\text{start}}, y_{\text{end}} \right], \quad 
        z \in \left[ z_{\text{start}}, z_{\text{end}} \right].
        $$
        
        ***

        #### Directions

        WebDG will create a mesh numerical approximation of your surface using a version of the [marching cubes algorithm](https://paulbourke.net/geometry/polygonise/) on an $n_x \times n_y \times n_z$ lattice.

        - Use the forms below to define the function $F$ and $n$-values for spacial resolution. 

        - When all inputs have been validated (✅), use "Render Subject" at the bottom to begin computing the approximation of your surface.

        ***

        #### Presets

        **Selecting 'Use' will erase any information currently in the forms below.**

        """, id="ls_define", mathjax=True
    ),

    dbc.InputGroup(
    [
        
        dbc.InputGroupText("Presets"),
        
        dbc.Select(
            options=[
                {"label": "Scherk's (first) surface", "value": "Scherk1"},
                {"label": "Scherk's (second) surface", "value": "Scherk2"},
                {"label": "Schwarz P-Surface", "value": "P-Surface"},
                {"label": "Schwarz D-Surface", "value": "D-Surface"},
                {"label": "Gyroid", "value": "Gyroid"},
            ],
            persistence=True,
            persistence_type = "memory",
            value="Scherk1", 
            id="ls_preset_select"
        ),
        
        dbc.Button("Use", id="ls_use_preset", color="warning"),
        
    ],
    className="mb-3"
    ),
    
    dcc.Markdown("***"),
    
    dcc.Markdown(r"""
                    
                    ### Surface Definition
                    
                    """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
    
    dcc.Store(id="ls_f_validated"),
    
    dbc.InputGroup(
        [
            dbc.InputGroupText(
                dcc.Markdown("$F(x,y,z)=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(value = "x+y+z", id="ls_fcomponent", persistence=True, persistence_type = "memory",), 
            
            dbc.InputGroupText(
                dcc.Markdown("$=0$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Button("Parse", color="info", id="ls_fcomponent_parse", n_clicks=0, style={'display' : 'none'})
            
        ],
        
        className="mb-3"
        
    ),
    
    dcc.Markdown(r"Please parse input for $F$", id="ls_fcomponent_formtext", 
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
    
    dcc.Markdown(r"""
                    
                ### Spacial Resultion
                
                Define the three axes' resolutions. High resultions may take a significant time to compute.
                    
                These parameters for numerical evaluation must each evaluate to a constant. 
                
                `pi` and `e` are allowed constants. 
                
                For example: "`4.28`" and "`3 + 8 * pi`" are valid, but "`4t`" and "`x * y`" are not valid.
                
                $n_x$, $n_y$, and $n_z$ must be a positive whole numbers.
                    
                """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
    
    dcc.Markdown("***"),
    
    # X
    
    dcc.Store(id="ls_xstart_validated"),
    dcc.Store(id="ls_xend_validated"),
    dcc.Store(id="ls_nx_validated"),
    
    dcc.Markdown(r"""
                    
                    #### $x$ resolution
                    
                    """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
    
    dbc.InputGroup(
        [
            dbc.InputGroupText(
                dcc.Markdown(r"$x_{\text{start}}=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(value="-1", id="ls_xstart", persistence=True, persistence_type = "memory",), 
            
            dbc.InputGroupText(
                dcc.Markdown(r"$x_{\text{end}}=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(value="1", id="ls_xend", persistence=True, persistence_type = "memory",), 
            
            dbc.InputGroupText(
                dcc.Markdown(r"$n_{x}=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(id="ls_nx", type="number", value=10, min=1, step=1, persistence=True, persistence_type = "memory",), 
            
            dbc.Button("Parse", color="info", id="ls_x_parse", n_clicks=0, style={'display' : 'none'})
            
        ],
        
        className="mb-3"
        
    ),
    
    dcc.Markdown(r"Please parse input for $x_{\text{start}}$", id="ls_xstart_formtext", 
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
    
    dcc.Markdown(r"Please parse input for $x_{\text{end}}$", id="ls_xend_formtext", 
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
    
    dcc.Markdown(r"Please parse input for $n_x$", id="ls_nx_formtext", 
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
    
    # Y
    
    dcc.Store(id="ls_ystart_validated"),
    dcc.Store(id="ls_yend_validated"),
    dcc.Store(id="ls_ny_validated"),
        
    dcc.Markdown(r"""
                    
                    #### $y$ resolution
                    
                    """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
    
    dbc.InputGroup(
        [
            dbc.InputGroupText(
                dcc.Markdown(r"$y_{\text{start}}=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(value="-1", id="ls_ystart", persistence=True, persistence_type = "memory",), 
            
            dbc.InputGroupText(
                dcc.Markdown(r"$y_{\text{end}}=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(value="1", id="ls_yend", persistence=True, persistence_type = "memory",), 
            
            dbc.InputGroupText(
                dcc.Markdown(r"$n_{y}=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(id="ls_ny", type="number", value=10, min=1, step=1, persistence=True, persistence_type = "memory",), 
            
            dbc.Button("Parse", color="info", id="ls_y_parse", n_clicks=0, style={'display' : 'none'})
            
        ],
        
        className="mb-3"
        
    ),
    
    dcc.Markdown(r"Please parse input for $y_{\text{start}}$", id="ls_ystart_formtext", 
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
    
    dcc.Markdown(r"Please parse input for $y_{\text{end}}$", id="ls_yend_formtext", 
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
    
    dcc.Markdown(r"Please parse input for $n_y$", id="ls_ny_formtext", 
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
    
    # Z
    
    dcc.Store(id="ls_zstart_validated"),
    dcc.Store(id="ls_zend_validated"),
    dcc.Store(id="ls_nz_validated"),
        
    dcc.Markdown(r"""
                    
                    #### $z$ resolution
                    
                    """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
    
    dbc.InputGroup(
        [
            dbc.InputGroupText(
                dcc.Markdown(r"$z_{\text{start}}=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(value="-1", id="ls_zstart", persistence=True, persistence_type = "memory",), 
            
            dbc.InputGroupText(
                dcc.Markdown(r"$z_{\text{end}}=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(value="1", id="ls_zend", persistence=True, persistence_type = "memory",), 
            
            dbc.InputGroupText(
                dcc.Markdown(r"$n_{z}=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(id="ls_nz", type="number", value=10, min=1, step=1, persistence=True, persistence_type = "memory",), 
            
            dbc.Button("Parse", color="info", id="ls_z_parse", n_clicks=0, style={'display' : 'none'})
            
        ],
        
        className="mb-3"
        
    ),
    
    dcc.Markdown(r"Please parse input for $z_{\text{start}}$", id="ls_zstart_formtext", 
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
    
    dcc.Markdown(r"Please parse input for $z_{\text{end}}$", id="ls_zend_formtext", 
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
    
    dcc.Markdown(r"Please parse input for $n_z$", id="ls_nz_formtext", 
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

    # color by
    dbc.InputGroup(
        [
            dbc.InputGroupText("Color surface by"),
            dbc.Select(
                options=[
                    # requires a texture mapping
                    #{"label": "XYZ coordinates.", "value": "xyz"},
                    {"label": "scene lighting.", "value": "lighting"},
                    {"label": "surface normal.", "value": "normal"},
                ],
                value="lighting",
                id="ls_colorby",
                className="flex-grow-1",
            )
        ],
        className="mb-3"
    ),

    dcc.Markdown("***"),
    
    dcc.Markdown("""               
                    The subject can be rendered when all inputs have been parsed and validated.""", id="ls_render_ready_message", className="mx-4", style={"textAlign" : "center"}),

    # render button
    dbc.Row(
        dbc.Col(dbc.Button("Render Subject", id="render_level_surface", color="warning", disabled=True), width="auto"),
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
                        id="cancel-ls-sure-modal",
                        n_clicks=0,
                        color="success"
                    ),
                    dbc.Button(
                        "Continue",
                        id="continue-ls-sure-modal",
                        n_clicks=0,
                        color="warning"
                    )
                ]
            ),
        ],
        id="ls-sure-modal",
        centered=True,
        size="sm"
    ),

])

# preset callback
clientside_callback(
    """
    function(button_click, preset) {
        if (button_click) {
            // Define the preset values in a simple data structure
            const preset_values = {
                "Scherk1": {
                    "ls_fcomponent": "e^z * cos(y) - cos(x)",
                    
                    "ls_xstart" : "-4 pi",
                    "ls_xend" : "4 pi",
                    "ls_nx" : 100,
                    
                    "ls_ystart" : "-6 pi",
                    "ls_yend" : "6 pi",
                    "ls_ny" : 100,
                    
                    "ls_zstart" : "-4 pi",
                    "ls_zend" : "4 pi",
                    "ls_nz" : 100
                    
                },
                "Scherk2": {
                    "ls_fcomponent": "sin(y)-sinh(x)*sinh(z)",
                    
                    "ls_xstart" : "-3 pi",
                    "ls_xend" : "3 pi",
                    "ls_nx" : 100,
                    
                    "ls_ystart" : "-7 pi",
                    "ls_yend" : "7 pi",
                    "ls_ny" : 100,
                    
                    "ls_zstart" : "-3pi",
                    "ls_zend" : "3pi",
                    "ls_nz" : 100
                    
                },
                "P-Surface": {
                    "ls_fcomponent": "cos(x)+cos(y)+cos(z)",
                    
                    "ls_xstart" : "-6 pi",
                    "ls_xend" : "6 pi",
                    "ls_nx" : 100,
                    
                    "ls_ystart" : "-6 pi",
                    "ls_yend" : "6 pi",
                    "ls_ny" : 100,
                    
                    "ls_zstart" : "-6 pi",
                    "ls_zend" : "6 pi",
                    "ls_nz" : 100
                },
                "D-Surface": {
                    "ls_fcomponent": "cos(z) * sin(x+y) + sin(z) * cos(x-y)",
                    
                    "ls_xstart" : "-6 pi",
                    "ls_xend" : "6 pi",
                    "ls_nx" : 100,
                    
                    "ls_ystart" : "-6 pi",
                    "ls_yend" : "6 pi",
                    "ls_ny" : 100,
                    
                    "ls_zstart" : "-6 pi",
                    "ls_zend" : "6 pi",
                    "ls_nz" : 100
                    
                },
                "Gyroid": {
                    "ls_fcomponent": "sin(x) * cos(y) + sin(y) * cos(z) + cos(x) * sin(z)",
                    
                    "ls_xstart" : "-6 pi",
                    "ls_xend" : "6 pi",
                    "ls_nx" : 100,
                    
                    "ls_ystart" : "-6 pi",
                    "ls_yend" : "6 pi",
                    "ls_ny" : 100,
                    
                    "ls_zstart" : "-6 pi",
                    "ls_zend" : "6 pi",
                    "ls_nz" : 100
                    
                }
            };
    
            // Get the values for the selected preset
            const values = preset_values[preset] || {};

            // Return the updated values
            return [
                values["ls_fcomponent"] || "",
                
                values["ls_xstart"] || "",
                values["ls_xend"] || "",
                values["ls_nx"] || "",
                
                values["ls_ystart"] || "",
                values["ls_yend"] || "",
                values["ls_ny"] || "",
                
                values["ls_zstart"] || "",
                values["ls_zend"] || "",
                values["ls_nz"] || ""
                
            ];
        }
        return [ "", "","","", "","","", "","","" ];
    }
    """,
    [
        Output("ls_fcomponent", "value"),
        
        Output("ls_xstart", "value"),
        Output("ls_xend", "value"),
        Output("ls_nx", "value"),
        
        Output("ls_ystart", "value"),
        Output("ls_yend", "value"),
        Output("ls_ny", "value"),
        
        Output("ls_zstart", "value"),
        Output("ls_zend", "value"),
        Output("ls_nz", "value"),
    ],
    [
        Input("continue-ls-sure-modal", "n_clicks")
    ],
    [
        State("ls_preset_select", "value")
    ],
    prevent_initial_call = True
)

## ls-sure preset modal
clientside_callback(
    """
    function(n_clicks, n_2, n_3, is_open) {
        return !is_open;
    }
    """,
    Output("ls-sure-modal", "is_open"),
    [Input("continue-ls-sure-modal", "n_clicks"), Input("cancel-ls-sure-modal", "n_clicks"), Input("ls_use_preset", "n_clicks")],
    State("ls-sure-modal", "is_open"),
    prevent_initial_call=True,
)

# equation (F) callback
clientside_callback(
    r"""
    function(n_clicks, value) {
        
        let dg = window.dash_clientside.differential_geometry;
        
        let result = dg.parse_math("F(x,y,z)=", value, ["x", "y", "z"]);
        
        function isValid(value) {
            return typeof value === "string" && value.startsWith("$$");
        }
        
        let valid = isValid(result);
        
        return [valid ? result + "$=0$": result, valid, !valid, valid ? value : "1"];
        
    }
    """,
    [Output("ls_fcomponent_formtext", "children"),
    Output("ls_fcomponent", "valid"),
    Output("ls_fcomponent", "invalid"),
    Output("ls_f_validated", "data")],
    Input("ls_fcomponent_parse", "n_clicks"),
    State("ls_fcomponent", "value"),
    prevent_initial_call=True
)

clientside_callback(
    r"""
    function(value, n_1, active_tab, inv, validated, parse_times) {
        
        if ((active_tab !== "minimal surfaces") || (value === validated && !inv)) {
            return window.dash_clientside.no_update;
        }
        
        return parse_times + 1; // this should trigger a parse
        
    }
    """,
    
    Output("ls_fcomponent_parse", "n_clicks"),
    
    Input("ls_fcomponent", "value"), 
    Input("subject", "n_clicks"), 
    Input("subject-tabs", "active_tab"),
    
    State("ls_fcomponent", "invalid"),
    State("ls_f_validated", "data"),
    State("ls_fcomponent_parse", "n_clicks")
)

# for x
clientside_callback(
    r"""
    function(n_clicks, ts_value, te_value, nt_value) {
        let dg = window.dash_clientside.differential_geometry;
        
        ts_value = ts_value.trim();
        te_value = te_value.trim();
        
        let results = {
            ts: dg.parse_constant("x_{\\text{start}}=", ts_value, ["t"])[0],
            te: dg.parse_constant("x_{\\text{end}}=", te_value, ["t"])[0],
            nt: dg.parse_constant("n_x=", nt_value, ["t"])[0],
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
        Output("ls_xstart_formtext", "children"),
        Output("ls_xend_formtext", "children"),
        Output("ls_nx_formtext", "children"),
        Output("ls_xstart", "valid"),
        Output("ls_xend", "valid"),
        Output("ls_nx", "valid"),
        Output("ls_xstart", "invalid"),
        Output("ls_xend", "invalid"),
        Output("ls_nx", "invalid"),
        Output("ls_xstart_validated", "data"),
        Output("ls_xend_validated", "data"),
        Output("ls_nx_validated", "data")
    ],
    [
        Input("ls_x_parse", "n_clicks")
    ],
    [
        State("ls_xstart", "value"),
        State("ls_xend", "value"),
        State("ls_nx", "value"),
    ],
    prevent_initial_call=True
)

clientside_callback(
    r"""
    function(s_value, e_value, n_value, n_1, active_tab, s_inv, s_validated, e_inv, e_validated, n_inv, n_validated, parse_times) {
        
        if ((active_tab !== "minimal surfaces")) {
            return window.dash_clientside.no_update;
        }
        
        if (s_value === s_validated && !s_inv) {
            return window.dash_clientside.no_update;
        }
        
        if (e_value === e_validated && !e_inv) {
            return window.dash_clientside.no_update;
        }
        
        if (n_value === n_validated && !n_inv) {
            return window.dash_clientside.no_update;
        }
        
        return parse_times + 1; // this should trigger a parse
        
    }
    """,
    
    Output("ls_x_parse", "n_clicks"),
    
    Input("ls_xstart", "value"),
    Input("ls_xend", "value"),
    Input("ls_nx", "value"),
    
    Input("subject", "n_clicks"), 
    Input("subject-tabs", "active_tab"),
    
    State("ls_xstart_validated", "data"),
    State("ls_xstart", "invalid"),
    
    State("ls_xend_validated", "data"),
    State("ls_xend", "invalid"),

    State("ls_nx_validated", "data"),
    State("ls_nx", "invalid"),    
    
    State("ls_x_parse", "n_clicks"),
)

# for y
clientside_callback(
    r"""
    function(n_clicks, ts_value, te_value, nt_value) {
        let dg = window.dash_clientside.differential_geometry;
        
        ts_value = ts_value.trim();
        te_value = te_value.trim();
        
        let results = {
            ts: dg.parse_constant("y_{\\text{start}}=", ts_value, ["t"])[0],
            te: dg.parse_constant("y_{\\text{end}}=", te_value, ["t"])[0],
            nt: dg.parse_constant("n_y=", nt_value, ["t"])[0],
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
        Output("ls_ystart_formtext", "children"),
        Output("ls_yend_formtext", "children"),
        Output("ls_ny_formtext", "children"),
        Output("ls_ystart", "valid"),
        Output("ls_yend", "valid"),
        Output("ls_ny", "valid"),
        Output("ls_ystart", "invalid"),
        Output("ls_yend", "invalid"),
        Output("ls_ny", "invalid"),
        Output("ls_ystart_validated", "data"),
        Output("ls_yend_validated", "data"),
        Output("ls_ny_validated", "data")
    ],
    [
        Input("ls_y_parse", "n_clicks")
    ],
    [
        State("ls_ystart", "value"),
        State("ls_yend", "value"),
        State("ls_ny", "value"),
    ],
    prevent_initial_call=True
)

clientside_callback(
    r"""
    function(s_value, e_value, n_value, n_1, active_tab, s_inv, s_validated, e_inv, e_validated, n_inv, n_validated, parse_times) {
        
        if ((active_tab !== "minimal surfaces")) {
            return window.dash_clientside.no_update;
        }
        
        if (s_value === s_validated && !s_inv) {
            return window.dash_clientside.no_update;
        }
        
        if (e_value === e_validated && !e_inv) {
            return window.dash_clientside.no_update;
        }
        
        if (n_value === n_validated && !n_inv) {
            return window.dash_clientside.no_update;
        }
        
        return parse_times + 1; // this should trigger a parse
        
    }
    """,
    
    Output("ls_y_parse", "n_clicks"),
    
    Input("ls_ystart", "value"),
    Input("ls_yend", "value"),
    Input("ls_ny", "value"),
    
    Input("subject", "n_clicks"), 
    Input("subject-tabs", "active_tab"),
    
    State("ls_ystart_validated", "data"),
    State("ls_ystart", "invalid"),
    
    State("ls_yend_validated", "data"),
    State("ls_yend", "invalid"),

    State("ls_ny_validated", "data"),
    State("ls_ny", "invalid"),    
    
    State("ls_y_parse", "n_clicks"),
)

# for z
clientside_callback(
    r"""
    function(n_clicks, ts_value, te_value, nt_value) {
        let dg = window.dash_clientside.differential_geometry;
        
        ts_value = ts_value.trim();
        te_value = te_value.trim();
        
        let results = {
            ts: dg.parse_constant("z_{\\text{start}}=", ts_value, ["t"])[0],
            te: dg.parse_constant("z_{\\text{end}}=", te_value, ["t"])[0],
            nt: dg.parse_constant("n_z=", nt_value, ["t"])[0],
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
        Output("ls_zstart_formtext", "children"),
        Output("ls_zend_formtext", "children"),
        Output("ls_nz_formtext", "children"),
        Output("ls_zstart", "valid"),
        Output("ls_zend", "valid"),
        Output("ls_nz", "valid"),
        Output("ls_zstart", "invalid"),
        Output("ls_zend", "invalid"),
        Output("ls_nz", "invalid"),
        Output("ls_zstart_validated", "data"),
        Output("ls_zend_validated", "data"),
        Output("ls_nz_validated", "data")
    ],
    [
        Input("ls_z_parse", "n_clicks")
    ],
    [
        State("ls_zstart", "value"),
        State("ls_zend", "value"),
        State("ls_nz", "value"),
    ],
    prevent_initial_call=True
)

clientside_callback(
    r"""
    function(s_value, e_value, n_value, n_1, active_tab, s_inv, s_validated, e_inv, e_validated, n_inv, n_validated, parse_times) {
        
        if ((active_tab !== "minimal surfaces")) {
            return window.dash_clientside.no_update;
        }
        
        if (s_value === s_validated && !s_inv) {
            return window.dash_clientside.no_update;
        }
        
        if (e_value === e_validated && !e_inv) {
            return window.dash_clientside.no_update;
        }
        
        if (n_value === n_validated && !n_inv) {
            return window.dash_clientside.no_update;
        }
        
        return parse_times + 1; // this should trigger a parse
        
    }
    """,
    
    Output("ls_z_parse", "n_clicks"),
    
    Input("ls_zstart", "value"),
    Input("ls_zend", "value"),
    Input("ls_nz", "value"),
    
    Input("subject", "n_clicks"), 
    Input("subject-tabs", "active_tab"),
    
    State("ls_zstart_validated", "data"),
    State("ls_zstart", "invalid"),
    
    State("ls_zend_validated", "data"),
    State("ls_zend", "invalid"),

    State("ls_nz_validated", "data"),
    State("ls_nz", "invalid"),    
    
    State("ls_z_parse", "n_clicks"),
)

# render readiness callback
clientside_callback(
    """
    function(valid1, invalid1, valid2, invalid2, valid3, invalid3, valid4, invalid4, valid5, invalid5, valid6, invalid6, valid7, invalid7, valid8, invalid8, valid9, invalid9, valid10, invalid10) {
        let allValid = valid1 && !invalid1 &&
                       valid2 && !invalid2 &&
                       valid3 && !invalid3 &&
                       valid4 && !invalid4 &&
                       valid5 && !invalid5 &&
                       valid6 && !invalid6 &&
                       valid7 && !invalid7 &&
                       valid8 && !invalid8 &&
                       valid9 && !invalid9 &&
                       valid10 && !invalid10;
                       
        let buttonDisabled = !allValid;
        let messageHidden = allValid ? "" : "The subject can be rendered when all inputs have been parsed and validated.";

        return [buttonDisabled, allValid ? "success" : "warning", messageHidden];
    }
    """,
    [
        Output("render_level_surface", "disabled"),
        Output("render_level_surface", "color"),
        Output("ls_render_ready_message", "children")
    ],
    [
        Input("ls_fcomponent", "valid"), Input("ls_fcomponent", "invalid"),

        Input("ls_xstart", "valid"), Input("ls_xstart", "invalid"),
        Input("ls_xend", "valid"), Input("ls_xend", "invalid"),
        Input("ls_nx", "valid"), Input("ls_nx", "invalid"),
        
        Input("ls_ystart", "valid"), Input("ls_ystart", "invalid"),
        Input("ls_yend", "valid"), Input("ls_yend", "invalid"),
        Input("ls_ny", "valid"), Input("ls_ny", "invalid"),
        
        Input("ls_zstart", "valid"), Input("ls_zstart", "invalid"),
        Input("ls_zend", "valid"), Input("ls_zend", "invalid"),
        Input("ls_nz", "valid"), Input("ls_nz", "invalid"),
    ]
)


