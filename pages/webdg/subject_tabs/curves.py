"""

curves.py

This defines the layout and callback functionality of the curves subject tab.

M W Hefner, 2025
MIT License

"""

import dash_bootstrap_components as dbc
from dash import html, Output, Input, dcc,clientside_callback,State

layout = html.Div(
    [
        
        dcc.Markdown(
            
            r"""

            #### Theory of Curves  

            Consider as the subject of study a **curve** $\alpha$ defined by the parametric representation  

            $$
            \alpha = \big( X(t), Y(t), Z(t) \big)
            $$

            where the parameter $t$ ranges over  

            $$
            t \in \left[ t_{\text{start}}, t_{\text{end}} \right].
            $$


            ***

            #### Directions

            WebDG will create a numerical approximation of your curve using $n_t$ equally spaced intervals of the total $t$ interval.

            - Use the forms below to define these functions and values. 

            - When all inputs have been validated (✅), use "Render Subject" at the bottom to begin computing the approximation of your curve.

            *Tip: Frenet-Serret (TNB) frame visibility can be toggled in the Settings menu.*

            ***

            #### Presets

            **Selecting 'Use' will erase any information currently in the forms below.**

            """, id="c_define", mathjax=True),

        # presets
        dbc.InputGroup(
            [
                
                dbc.InputGroupText("Presets"),
                
                dbc.Select(
                    options=[
                        {"label": "Line", "value": "Line"},
                        {"label": "Circle", "value": "Planar Curve"}, # make a circle
                        {"label": 'Catenary', "value": "Catenary"},
                        {"label": 'Cycloid', "value": "Cycloid"},
                        {"label": 'Archimedean Spiral', "value": "Archimedean Spiral"},
                        {"label": "Helix", "value": "Helix"},
                        {"label": "Trefoil Knot", "value": "Trefoil Knot"},
                        {"label": "Torus Knot", "value": "Torus Knot"},
                    ],
                    persistence=True,
                    persistence_type = "memory",
                    value="Planar Curve", 
                    id="c_preset_select"
                ),
                
                dbc.Button("Use", id="c_use_preset", color="warning")
                
            ],
            
            className="mb-3"
            
        ),
        
        dcc.Markdown("***"),
        
        dcc.Markdown(r"""
                     
                     ### Curve Definition
                     
                     Given $\alpha = \left( X(t), Y(t), Z(t) \right)$,
                     
                     define $\alpha$ by defining $X(t)$, $Y(t)$, and $Z(t)$.
                     
                     """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        # CX
        
        dcc.Store(id="c_x_validated"),
        
        dbc.InputGroup(
            [
                dbc.InputGroupText(
                    dcc.Markdown("$X (t)=$", mathjax=True),
                    className = "LaTeX-p"
                ), 
                
                dbc.Input(value = "cos(t)", id="c_xcomponent", persistence=True, persistence_type = "memory"), 
                
                dbc.Button("Parse", color="info", id="c_xcomponent_parse", n_clicks=0, style={'display' : 'none'})
                
            ],
            
            className="mb-3"
            
        ),
        
        dcc.Markdown(r"Please parse input for $X$", id="c_xcomponent_formtext", 
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
        
        # CY
        
        dcc.Store(id="c_y_validated"),
        
        dbc.InputGroup(
            [
                dbc.InputGroupText(
                    dcc.Markdown("$Y (t)=$", mathjax=True),
                    className = "LaTeX-p"
                ), 
                
                dbc.Input(value = "sin(t)", id="c_ycomponent", persistence=True, persistence_type = "memory",), 
                
                dbc.Button("Parse", color="info", id="c_ycomponent_parse", n_clicks=0, style={'display' : 'none'})
                
            ],
            
            className="mb-3"
            
        ),
        
        dcc.Markdown(r"Please parse input for $Y$", id="c_ycomponent_formtext", 
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
        
        # CZ
        
        dcc.Store(id="c_z_validated"),
        
        dbc.InputGroup(
            [
                dbc.InputGroupText(
                    dcc.Markdown("$Z (t)=$", mathjax=True),
                    className = "LaTeX-p"
                ), 
                
                dbc.Input(value = "0", id="c_zcomponent", persistence=True, persistence_type = "memory",), 
                
                dbc.Button("Parse", color="info", id="c_zcomponent_parse", n_clicks=0, style={'display' : 'none'})
                
            ],
            
            className="mb-3"
            
        ),
        
        dcc.Markdown(
            r"Please parse input for $Z$", 
            id="c_zcomponent_formtext", 
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
        
        # CT
        
        dcc.Store(id="c_tstart_validated"),
        dcc.Store(id="c_tend_validated"),
        dcc.Store(id="c_nt_validated"),
        
        dcc.Markdown(r"""
                     
                     #### Define $t$
                     
                     """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dbc.InputGroup(
            [
                dbc.InputGroupText(
                    dcc.Markdown(r"$t_{\text{start}}=$", mathjax=True),
                    className = "LaTeX-p"
                ), 
                
                dbc.Input(value="0", id="c_tstart", persistence=True, persistence_type = "memory",), 
                
                dbc.InputGroupText(
                    dcc.Markdown(r"$t_{\text{end}}=$", mathjax=True),
                    className = "LaTeX-p"
                ), 
                
                dbc.Input(value="2 * pi", id="c_tend", persistence=True, persistence_type = "memory",), 
                
                dbc.InputGroupText(
                    dcc.Markdown(r"$n_{t}=$", mathjax=True),
                    className = "LaTeX-p"
                ), 
                
                dbc.Input(id="c_nt", type="number", value=100, min=1, step=1, persistence=True, persistence_type = "memory",), 
                
                dbc.Button("Parse", color="info", id="c_t_parse", n_clicks=0, style={'display' : 'none'})
                
            ],
            
            className="mb-3"
            
        ),
        
        dcc.Markdown(r"""
                     
                    These parameters for numerical evaluation must each evaluate to a constant. 
                    
                    `pi` and `e` are allowed constants. 
                    
                    For example: "`4.28`" and "`3 + 8 * pi`" are valid, but "`4t`" and "`x * y`" are not valid.
                    
                    $n_t$ must be a positive whole number.
                    
                    The $t$ numerical parameters have been parsed as:
                     
                    """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(r"Please parse input for $t_{\text{start}}$", id="c_tstart_formtext", 
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
        
        dcc.Markdown(r"Please parse input for $t_{\text{end}}$", id="c_tend_formtext", 
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
        
        dcc.Markdown(r"Please parse input for $n_t$", id="c_nt_formtext", 
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
            
        dbc.InputGroup(
            [
                dbc.InputGroupText("Color curve by"),
                dbc.Select(
                    options=[
                        {"label": "its speed.", "value": "Speed"},
                        {"label": "its curvature.", "value": "Curvature"},
                        {"label": "its torsion.", "value": "Torsion"},
                        {"label": "its t coordinates.", "value": "t"},
                        {"label": "its (X,Y,Z) coordinates.", "value": "xyz"},
                        {"label": "this solid color:", "value": "Solid Color"},
                    ],
                    value="Solid Color",
                    id="c_colorby",
                    className="flex-grow-1",
                ),
                dbc.Input(
                    type="color",
                    id="c_colorpicker",
                    value="#FFFFFF",
                    className="p-0 border-0",
                    style={"width": "10%", "height": "2.5rem"}  # Adjust height for visibility
                ),
            ],
            className="mb-3"
        ),

        dcc.Markdown("***"),
        
        dcc.Markdown("""               
                     The subject can be rendered when all inputs have been parsed and validated.""", id="c_render_ready_message", className="mx-4", style={"textAlign" : "center"}),

            
        dbc.Row(
            dbc.Col(dbc.Button("Render Subject", id="render_curve", color="warning", disabled=True), width="auto"),
            justify="center", className="m-4"
        ),
            
        # sure? preset Modal
        dbc.Modal(
            [

                dbc.ModalHeader(dbc.ModalTitle("Are you sure?")),
                dbc.ModalBody(
                    dcc.Markdown(
                        """
                        This operation will overwrite the existing curve form field inputs with the definitions of the selected preset curve. 
                        
                        **Are you sure you want to continue?**
                        
                        """
                    )
                ),
                dbc.ModalFooter(
                    className="d-flex justify-content-between w-100",
                    children=[
                        dbc.Button(
                            "Cancel",
                            id="cancel-c-sure-modal",
                            n_clicks=0,
                            color="success"
                        ),
                        dbc.Button(
                            "Continue",
                            id="continue-c-sure-modal",
                            n_clicks=0,
                            color="warning"
                        )
                    ]
                ),
            ],
            id="c-sure-modal",
            centered=True,
            size="sm"
        ),
        
    ]
)

# Curve callbacks

# preset callback
clientside_callback(
    """
    function(button_click, preset) {
        if (button_click) {
            // Define the preset values in a simple data structure
            const preset_values = {
                "Planar Curve": {
                    "c_xcomponent": "cos(t)",
                    "c_ycomponent": "sin(t)",
                    "c_zcomponent": "0",
                    "c_tstart": "0",
                    "c_tend": "2 * pi",
                    "c_nt": 100
                },
                "Line": {
                    "c_xcomponent": "2 * t",
                    "c_ycomponent": "3 * t",
                    "c_zcomponent": "1/2 * t",
                    "c_tstart": "-10",
                    "c_tend": "10",
                    "c_nt": 1
                },
                "Helix": {
                    "c_xcomponent": "cos(t)",
                    "c_ycomponent": "sin(t)",
                    "c_zcomponent": "t",
                    "c_tstart": "-10",
                    "c_tend": "10",
                    "c_nt": 200
                },
                "Trefoil Knot": {
                    "c_xcomponent": "sin(t) + 2 * sin(2 * t)",
                    "c_ycomponent": "cos(t) - 2 * cos(2 * t)",
                    "c_zcomponent": "sin(3 * t)",
                    "c_tstart": "0",
                    "c_tend": "2 * pi",
                    "c_nt": 100
                },
                "Torus Knot": {
                    "c_xcomponent": "sin(3 * t) * (1 + 0.3 * cos(4 * t))",
                    "c_ycomponent": "cos(3 * t) * (1 + 0.3 * cos(4 * t))",
                    "c_zcomponent": "0.3 * sin(4 * t)",
                    "c_tstart": "0",
                    "c_tend": "2 * pi",
                    "c_nt": 200
                },
                "Archimedean Spiral": {
                    "c_xcomponent": "t * cos(t)",
                    "c_ycomponent": "t * sin(t)",
                    "c_zcomponent": "0",
                    "c_tstart": "0",
                    "c_tend": "2 * pi",
                    "c_nt": 200
                },
                "Catenary": {
                    "c_xcomponent": "t",
                    "c_ycomponent": "cosh(t)",
                    "c_zcomponent": "0",
                    "c_tstart": "-pi",
                    "c_tend": "pi",
                    "c_nt": 100
                },
                "Cycloid": {
                    "c_xcomponent": "t - sin(t)",
                    "c_ycomponent": "1 - cos(t)",
                    "c_zcomponent": "0",
                    "c_tstart": "0.01",
                    "c_tend": "1.99 * pi",
                    "c_nt": 100
                }

            };
            
            // Get the values for the selected preset
            const values = preset_values[preset];

            // Return the updated values and reset 'valid' and 'invalid' properties
            return [
                values["c_xcomponent"],
                values["c_ycomponent"],
                values["c_zcomponent"],
                values["c_tstart"],
                values["c_tend"],
                values["c_nt"]
            ];
        }
        return [];
    }
    """,
    # Output for the 6 input values and their valid/invalid properties
    Output("c_xcomponent", "value"),
    Output("c_ycomponent", "value"),
    Output("c_zcomponent", "value"),
    Output("c_tstart", "value"),
    Output("c_tend", "value"),
    Output("c_nt", "value"),
    Input("continue-c-sure-modal", "n_clicks"),
    State("c_preset_select", "value"),
)

## c-sure preset modal
clientside_callback(
    """
    function(n_clicks, n_2, n_3, is_open) {
        return !is_open;
    }
    """,
    Output("c-sure-modal", "is_open"),
    [Input("continue-c-sure-modal", "n_clicks"), Input("cancel-c-sure-modal", "n_clicks"), Input("c_use_preset", "n_clicks")],
    State("c-sure-modal", "is_open"),
    prevent_initial_call=True,
)

# curve component input callbacks
clientside_callback(
    r"""
    function(n_clicks, value) {
        
        let dg = window.dash_clientside.differential_geometry;
        
        let result = dg.parse_math("X(t)=", value, ["t"]);
        
        function isValid(x) {
            return typeof x === "string" && x.startsWith("$$");
        }
        
        let valid = isValid(result);
        
        return [result, valid, !valid, valid ? value : "1"];
        
    }
    """,
    [Output("c_xcomponent_formtext", "children"),
    Output("c_xcomponent", "valid"),
    Output("c_xcomponent", "invalid"),
    Output("c_x_validated", "data")],
    Input("c_xcomponent_parse", "n_clicks"),
    State("c_xcomponent", "value"),
    prevent_initial_call=True
)

clientside_callback(
    r"""
    function(value, n_1, active_tab, inv, validated, parse_times) {
        
        if ((active_tab !== "curves") || (value === validated && !inv)) {
            return window.dash_clientside.no_update;
        }
        
        return parse_times + 1; // this should trigger a parse
        
    }
    """,
    
    Output("c_xcomponent_parse", "n_clicks"),
    
    Input("c_xcomponent", "value"), 
    Input("subject", "n_clicks"), 
    Input("subject-tabs", "active_tab"),
    
    State("c_xcomponent", "invalid"),
    State("c_x_validated", "data"),
    State("c_xcomponent_parse", "n_clicks")
)

clientside_callback(
    r"""
    function(n_clicks, value) {
        
        let dg = window.dash_clientside.differential_geometry;
        
        let result = dg.parse_math("Y(t)=", value, ["t"]);
        
        function isValid(value) {
            return typeof value === "string" && value.startsWith("$$");
        }
        
        let valid = isValid(result);
        
        return [result, valid, !valid, valid ? value : "1"];
        
    }
    """,
    [Output("c_ycomponent_formtext", "children"),
    Output("c_ycomponent", "valid"),
    Output("c_ycomponent", "invalid"),
    Output("c_y_validated", "data")],
    Input("c_ycomponent_parse", "n_clicks"),
    State("c_ycomponent", "value"),
    prevent_initial_call=True
)

clientside_callback(
    r"""
    function(value, n_1, active_tab, inv, validated, parse_times) {
        
        if ((active_tab !== "curves") || (value === validated && !inv)) {
            return window.dash_clientside.no_update;
        }
        
        return parse_times + 1; // this should trigger a parse
        
    }
    """,
    
    Output("c_ycomponent_parse", "n_clicks"),
    
    Input("c_ycomponent", "value"), 
    Input("subject", "n_clicks"), 
    Input("subject-tabs", "active_tab"),
    
    State("c_ycomponent", "invalid"),
    State("c_y_validated", "data"),
    State("c_ycomponent_parse", "n_clicks")
)

clientside_callback(
    r"""
    function(n_clicks, value) {
        
        let dg = window.dash_clientside.differential_geometry;
        
        let result = dg.parse_math("Z(t)=", value, ["t"]);
        
        function isValid(value) {
            return typeof value === "string" && value.startsWith("$$");
        }
        
        let valid = isValid(result);
        
        return [result, valid, !valid, valid ? value : "1"];
        
    }
    """,
    [Output("c_zcomponent_formtext", "children"),
    Output("c_zcomponent", "valid"),
    Output("c_zcomponent", "invalid"),
    Output("c_z_validated", "data")],
    Input("c_zcomponent_parse", "n_clicks"),
    State("c_zcomponent", "value"),
    prevent_initial_call=True
)

clientside_callback(
    r"""
    function(value, n_1, active_tab, inv, validated, parse_times) {
        
        if ((active_tab !== "curves") || (value === validated && !inv)) {
            return window.dash_clientside.no_update;
        }
        
        return parse_times + 1; // this should trigger a parse
        
    }
    """,
    
    Output("c_zcomponent_parse", "n_clicks"),
    
    Input("c_zcomponent", "value"), 
    Input("subject", "n_clicks"), 
    Input("subject-tabs", "active_tab"),
    
    State("c_zcomponent", "invalid"),
    State("c_z_validated", "data"),
    State("c_zcomponent_parse", "n_clicks")
)

# for t
clientside_callback(
    r"""
    function(n_clicks, ts_value, te_value, nt_value) {
        let dg = window.dash_clientside.differential_geometry;
        
        ts_value = ts_value.trim();
        te_value = te_value.trim();
        
        let results = {
            ts: dg.parse_constant("t_{\\text{start}}=", ts_value, ["t"])[0],
            te: dg.parse_constant("t_{\\text{end}}=", te_value, ["t"])[0],
            nt: dg.parse_constant("n_t=", nt_value, ["t"])[0],
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
        Output("c_tstart_formtext", "children"),
        Output("c_tend_formtext", "children"),
        Output("c_nt_formtext", "children"),
        
        Output("c_tstart", "valid"),
        Output("c_tend", "valid"),
        Output("c_nt", "valid"),
        
        Output("c_tstart", "invalid"),
        Output("c_tend", "invalid"),
        Output("c_nt", "invalid"),
        
        Output("c_tstart_validated", "data"),
        Output("c_tend_validated", "data"),
        Output("c_nt_validated", "data")
    ],
    [
        Input("c_t_parse", "n_clicks")
    ],
    [
        State("c_tstart", "value"),
        State("c_tend", "value"),
        State("c_nt", "value"),
    ],
    prevent_initial_call=True
)

clientside_callback(
    r"""
    function(s_value, e_value, n_value, n_1, active_tab, s_inv, s_validated, e_inv, e_validated, n_inv, n_validated, parse_times) {
        
        if ((active_tab !== "curves")) {
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
    
    Output("c_t_parse", "n_clicks"),
    
    Input("c_tstart", "value"),
    Input("c_tend", "value"),
    Input("c_nt", "value"),
    
    Input("subject", "n_clicks"), 
    Input("subject-tabs", "active_tab"),
    
    State("c_tstart_validated", "data"),
    State("c_tstart", "invalid"),
    
    State("c_tend_validated", "data"),
    State("c_tend", "invalid"),

    State("c_nt_validated", "data"),
    State("c_nt", "invalid"),    
    
    State("c_t_parse", "n_clicks"),
)

# for color
clientside_callback(
    """
    function(selected_value) {
        // Return true to disable, false to enable the color picker
        return selected_value !== "Solid Color";
    }
    """,
    Output("c_colorpicker", "disabled"),
    Input("c_colorby", "value"),
)

# render readiness callback
clientside_callback(
    """
    function(valid1, invalid1, valid2, invalid2, valid3, invalid3, valid4, invalid4, valid5, invalid5, valid6, invalid6) {
        let allValid = valid1 && !invalid1 &&
                       valid2 && !invalid2 &&
                       valid3 && !invalid3 &&
                       valid4 && !invalid4 &&
                       valid5 && !invalid5 &&
                       valid6 && !invalid6;
                       
        let buttonDisabled = !allValid;
        let messageHidden = allValid ? "" : "The subject can be rendered when all inputs have been parsed and validated.";

        return [buttonDisabled, allValid ? "success" : "warning", messageHidden];
    }
    """,
    [
        Output("render_curve", "disabled"),
        Output("render_curve", "color"),
        Output("c_render_ready_message", "children")
    ],
    [
        Input("c_xcomponent", "valid"), Input("c_xcomponent", "invalid"),
        Input("c_ycomponent", "valid"), Input("c_ycomponent", "invalid"),
        Input("c_zcomponent", "valid"), Input("c_zcomponent", "invalid"),
        Input("c_tstart", "valid"), Input("c_tstart", "invalid"),
        Input("c_tend", "valid"), Input("c_tend", "invalid"),
        Input("c_nt", "valid"), Input("c_nt", "invalid"),
    ]
)
