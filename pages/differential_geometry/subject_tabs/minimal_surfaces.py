import dash_bootstrap_components as dbc
from dash import html, Output, Input, dcc,clientside_callback,State, ClientsideFunction

# Minimal Surfaces

layout = html.Div([
    
    dcc.Markdown(
        r"""
        #### Minimal Surfaces by Enneper-Weierstrass Parameterization

        Consider as the subject of study a [**minimal surface**](https://mathworld.wolfram.com/MinimalSurface.html) $S$ defined by the parametric representation  

        $$
        S = \big( X(z), Y(z), Z(z) \big)
        $$

        where the simply connected domain of the complex parameter $z=a+bi$ is

        $$
        a \in \left[ a_{\text{start}}, a_{\text{end}} \right], \quad 
        b \in \left[ b_{\text{start}}, b_{\text{end}} \right].
        $$
        
        We call functions $f(z)$ and $g(z)$ the [Enneper-Weierstrass Parameterization](https://mathworld.wolfram.com/Enneper-WeierstrassParameterization.html) of $S$ when:
        
        $$
        X(z)= \Re \big[ \int  f \cdot (1-g^2)  dz \big]
        $$
        
        $$
        Y(z)= \Re \big[ \int if \cdot (1+g^2)  dz \big]
        $$
        
        $$
        Z(z)= \Re \big[ \int  2fg  dz \big]
        $$


        ***

        #### Directions

        WebDG will create a mesh numerical approximation of your surface using $n_a$ equally spaced intervals of the total $a$ interval and $n_b$ equally spaced intervals of the total $b$ interval.

        - Use the forms below to define these functions and values. 

        - Use "Parse" to have WebDG process, understand, and validate an input. 

        - Once all inputs have valid parses, use "Render Subject" at the bottom to begin computing the mesh approximation of your surface from the parsed inputs.
        
        You can use the functions `re()` and `im()` to refer to real and imaginary parts of complex values.


        ***

        #### Presets

        Using a preset means overwriting the form inputs below with the definitions for the selected preset surface. **Selecting 'Use' will erase any information currently in these forms.** Preset inputs must be parsed like any other.

        """, id="ms_define", mathjax=True
    ),

    dbc.InputGroup(
    [
        
        dbc.InputGroupText("Presets"),
        
        dbc.Select(
            options=[
                {"label": "Bour's minimal surface", "value": "Bour"},
                {"label": "Enneper's minimal surface", "value": "Enneper"},
                {"label": "Henneberg's minimal surface", "value": "Henneberg"},
                {"label": "Scherk's second minimal surface", "value": "Scherk"},
                {"label": 'Trinoid', "value": "Trinoid"},
            ],
            persistence=True,
            persistence_type = "memory",
            value="Bour", 
            id="ms_preset_select"
        ),
        
        dbc.Button("Use", id="ms_use_preset", color="warning"),
        
    ],
    className="mb-3"
    ),
    
    dcc.Markdown("***"),
    
    dcc.Markdown(r"""
                    
                    ### Enneper-Weierstrass Parameterization
                    
                    """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
    
    # These are calculated by a callback from the E.W. param
    dcc.Store(id="ms_x_validated"),
    dcc.Store(id="ms_y_validated"),
    dcc.Store(id="ms_z_validated"),
    
    dcc.Store(id="ms_f_validated"),
    
    dbc.InputGroup(
        [
            dbc.InputGroupText(
                dcc.Markdown("$f(z)=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(value = "1", id="ms_fcomponent", persistence=True, persistence_type = "memory",), 
            
            dbc.Button("Parse", color="info", id="ms_fcomponent_parse")
            
        ],
        
        className="mb-3"
        
    ),
    
    dcc.Markdown(r"""
                    
                    $f(z)$ has been parsed as: 
                    
                    """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
    
    dcc.Markdown(r"Please parse input for $f$", id="ms_fcomponent_formtext", 
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
    
    dcc.Store(id="ms_g_validated"),
    
    dbc.InputGroup(
        [
            dbc.InputGroupText(
                dcc.Markdown("$g(z)=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(value = "z", id="ms_gcomponent", persistence=True, persistence_type = "memory",), 
            
            dbc.Button("Parse", color="info", id="ms_gcomponent_parse")
            
        ],
        
        className="mb-3"
        
    ),
    
    dcc.Markdown(r"""
                    
                    $g(z)$ has been parsed as: 
                    
                    """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
    
    dcc.Markdown(r"Please parse input for $g$", id="ms_gcomponent_formtext", 
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
    
    dcc.Store(id="ms_astart_validated"),
    dcc.Store(id="ms_aend_validated"),
    dcc.Store(id="ms_na_validated"),
    
    dcc.Markdown(r"""
                    
                    ### Complex Domain Definition
                    
                    Given $z = a+bi$,
                    
                    define the complex domain in $z$ by defining the domains of $a$ and $b$.
                    
                    """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
    
    dcc.Markdown(r"""
                    
                    #### Define $a$
                    
                    """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
    
    dbc.InputGroup(
        [
            dbc.InputGroupText(
                dcc.Markdown(r"$a_{\text{start}}=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(value="-1", id="ms_astart", persistence=True, persistence_type = "memory",), 
            
            dbc.InputGroupText(
                dcc.Markdown(r"$a_{\text{end}}=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(value="1", id="ms_aend", persistence=True, persistence_type = "memory",), 
            
            dbc.InputGroupText(
                dcc.Markdown(r"$n_{a}=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(id="ms_na", type="number", value=10, min=1, step=1, persistence=True, persistence_type = "memory",), 
            
            dbc.Button("Parse", color="info", id="ms_a_parse")
            
        ],
        
        className="mb-3"
        
    ),
    
    dcc.Markdown(r"""
                    
                These parameters for numerical evaluation must each evaluate to a constant. 
                
                `pi` and `e` are allowed constants. 
                
                For example: "`4.28`" and "`3 + 8 * pi`" are valid, but "`4t`" and "`x * y`" are not valid.
                
                $n_a$ must be a positive whole number.
                
                The $a$ numerical parameters have been parsed as:
                    
                """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
    
    dcc.Markdown(r"Please parse input for $a_{\text{start}}$", id="ms_astart_formtext", 
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
    
    dcc.Markdown(r"Please parse input for $a_{\text{end}}$", id="ms_aend_formtext", 
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
    
    dcc.Markdown(r"Please parse input for $n_a$", id="ms_na_formtext", 
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
    
    dcc.Store(id="ms_bstart_validated"),
    dcc.Store(id="ms_bend_validated"),
    dcc.Store(id="ms_nb_validated"),
        
    dcc.Markdown(r"""
                    
                    #### Define $b$
                    
                    """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
    
    dbc.InputGroup(
        [
            dbc.InputGroupText(
                dcc.Markdown(r"$b_{\text{start}}=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(value="-1", id="ms_bstart", persistence=True, persistence_type = "memory",), 
            
            dbc.InputGroupText(
                dcc.Markdown(r"$b_{\text{end}}=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(value="1", id="ms_bend", persistence=True, persistence_type = "memory",), 
            
            dbc.InputGroupText(
                dcc.Markdown(r"$n_{b}=$", mathjax=True),
                className = "LaTeX-p"
            ), 
            
            dbc.Input(id="ms_nb", type="number", value=10, min=1, step=1, persistence=True, persistence_type = "memory",), 
            
            dbc.Button("Parse", color="info", id="s_v_parse")
            
        ],
        
        className="mb-3"
        
    ),
    
    dcc.Markdown(r"""
                    
                These parameters for numerical evaluation must each evaluate to a constant. 
                
                `pi` and `e` are allowed constants. 
                
                For example: "`4.28`" and "`3 + 8 * pi`" are valid, but "`4t`" and "`x * y`" are not valid.
                
                $n_b$ must be a positive whole number.
                
                The $b$ numerical parameters have been parsed as:
                    
                """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
    
    dcc.Markdown(r"Please parse input for $b_{\text{start}}$", id="ms_bstart_formtext", 
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
    
    dcc.Markdown(r"Please parse input for $b_{\text{end}}$", id="ms_bend_formtext", 
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
    
    dcc.Markdown(r"Please parse input for $n_b$", id="ms_nb_formtext", 
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
                id="ms_colorby",
                className="flex-grow-1",
            )
        ],
        className="mb-3"
    ),

    dcc.Markdown("***"),
    
    dcc.Markdown("""               
                    The subject can be rendered when all inputs have been parsed and validated.""", id="ms_render_ready_message", className="mx-4", style={"textAlign" : "center"}),

    # render button
    dbc.Row(
        dbc.Col(dbc.Button("Render Subject", id="render_minimal_surface", color="warning", disabled=True), width="auto"),
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
                        id="cancel-ms-sure-modal",
                        n_clicks=0,
                        color="success"
                    ),
                    dbc.Button(
                        "Continue",
                        id="continue-ms-sure-modal",
                        n_clicks=0,
                        color="warning"
                    )
                ]
            ),
        ],
        id="ms-sure-modal",
        centered=True,
        size="sm"
    ),

])

clientside_callback(
    """
    function(button_click, preset) {
        if (button_click) {
            // Define the preset values in a simple data structure
            const preset_values = {
                "Bour": {
                    "ms_fcomponent": "1",
                    "ms_gcomponent": "sqrt(z)"
                }
            };
    
            // Get the values for the selected preset
            const values = preset_values[preset] || {};

            // Return the updated values
            return [
                values["ms_fcomponent"] || "",
                values["ms_gcomponent"] || ""
            ];
        }
        return [ "", "" ];
    }
    """,
    [
        Output("ms_fcomponent", "value"),
        Output("ms_gcomponent", "value"),
    ],
    [
        Input("continue-ms-sure-modal", "n_clicks")
    ],
    [
        State("ms_preset_select", "value")
    ],
    prevent_initial_call = True
)

## ms-sure preset modal
clientside_callback(
    """
    function(n_clicks, n_2, n_3, is_open) {
        return !is_open;
    }
    """,
    Output("ms-sure-modal", "is_open"),
    [Input("continue-ms-sure-modal", "n_clicks"), Input("cancel-ms-sure-modal", "n_clicks"), Input("ms_use_preset", "n_clicks")],
    State("ms-sure-modal", "is_open"),
    prevent_initial_call=True,
)

# surface component (f and g) input callbacks
clientside_callback(
    r"""
    function(n_clicks, value) {
        
        let dg = window.dash_clientside.differential_geometry;
        
        let result = dg.parse_math("f(z)=", value, ["z"]);
        
        function isValid(value) {
            return typeof value === "string" && value.startsWith("$$");
        }
        
        let valid = isValid(result);
        
        return [result, valid, !valid, valid ? value : "1"];
        
    }
    """,
    [Output("ms_fcomponent_formtext", "children"),
    Output("ms_fcomponent", "valid"),
    Output("ms_fcomponent", "invalid"),
    Output("ms_f_validated", "data")],
    Input("ms_fcomponent_parse", "n_clicks"),
    State("ms_fcomponent", "value"),
    prevent_initial_call=True
)

clientside_callback(
    r"""
    function(n_clicks, value) {
        
        let dg = window.dash_clientside.differential_geometry;
        
        let result = dg.parse_math("g(z)=", value, ["z"]);
        
        function isValid(value) {
            return typeof value === "string" && value.startsWith("$$");
        }
        
        let valid = isValid(result);
        
        return [result, valid, !valid, valid ? value : "1"];
        
    }
    """,
    [Output("ms_gcomponent_formtext", "children"),
    Output("ms_gcomponent", "valid"),
    Output("ms_gcomponent", "invalid"),
    Output("ms_g_validated", "data")],
    Input("ms_gcomponent_parse", "n_clicks"),
    State("ms_gcomponent", "value"),
    prevent_initial_call=True
)

# callback to calculator the XYZ from the f and g

clientside_callback(
    """
    function(ms_f_validated, ms_g_validated) {
        x_validated = ms_f_validated;
        y_validated = ms_g_validated;
        z_validated = "";
        
        //console.log(x_validated, y_validated, z_validated);
        
        return [x_validated, y_validated, z_validated];
    }
    """,
    [
        Output("ms_x_validated", "data"),
        Output("ms_y_validated", "data"),
        Output("ms_z_validated", "data"),
    ],
    [
        Input("ms_f_validated", "data"),
        Input("ms_g_validated", "data")
    ]
)

# for a
clientside_callback(
    r"""
    function(n_clicks, ts_value, te_value, nt_value) {
        let dg = window.dash_clientside.differential_geometry;
        
        ts_value = ts_value.trim();
        te_value = te_value.trim();
        
        let results = {
            ts: dg.parse_constant("a_{\\text{start}}=", ts_value, ["t"])[0],
            te: dg.parse_constant("a_{\\text{end}}=", te_value, ["t"])[0],
            nt: dg.parse_constant("n_a=", nt_value, ["t"])[0],
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
        Output("ms_astart_formtext", "children"),
        Output("ms_aend_formtext", "children"),
        Output("ms_na_formtext", "children"),
        Output("ms_astart", "valid"),
        Output("ms_aend", "valid"),
        Output("ms_na", "valid"),
        Output("ms_astart", "invalid"),
        Output("ms_aend", "invalid"),
        Output("ms_na", "invalid"),
        Output("ms_astart_validated", "data"),
        Output("ms_aend_validated", "data"),
        Output("ms_na_validated", "data")
    ],
    [
        Input("ms_a_parse", "n_clicks")
    ],
    [
        State("ms_astart", "value"),
        State("ms_aend", "value"),
        State("ms_na", "value"),
    ],
    prevent_initial_call=True
)