import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input, State, clientside_callback, no_update, ClientsideFunction, ctx
import plotly.graph_objects as go
import numpy as np

not_yet_rendered = html.Div(
    [
        dcc.Markdown(r"""

            Analytics can be computed here after a subject has been rendered.
            
            *Note that equations are rendered in $\LaTeX$. This must be done by the main thread, so large expressions may take some time to render and lead to sluggish performance.*

        """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),


    ], id="not_yet_rendered_analytics_container"
)

curves = html.Div(
    
    [
        
        dcc.Store(id = "store_curves_data", storage_type='memory'),
        
        # TITLE AND XYZ COMPONENTS
        
        dcc.Markdown(r"""

            # Curve Analytics
            
            ***
            
            **NOTICE** 
            
            These calculations are done using [mathjs](https://mathjs.org). Please be aware that, while the results presented are typically accurate, mathjs generally __does not *simplify* trigonometric expressions.__
            
            Large equations scroll horizontally.
            
            The results below come with no guarantee of accuracy or fitness for any purpose.
            
            ***
            
            ## The curve 
            
            $$\alpha=(X(t),Y(t),Z(t))$$

        """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(
            id="c_xyz", 
            mathjax=True, 
            className="mx-4 text-wrap w-90",
            style={
                "textAlign": "center", 
                "fontSize": "1.5em",
                "overflowWrap": "break-word", 
                "wordBreak": "break-word", 
                "whiteSpace": "normal",  
                "display": "block",  
                "maxWidth": "100%", 
                "overflowX": "auto"
            }
        ),
        
        dcc.Markdown(r"""

            #### Selectable $\LaTeX$

        """, mathjax=True, className="mx-4 mt-4 text-wrap", style={"textAlign" : "center"}),
        
        # Centered Row
        dbc.Row(
            dbc.Col(
                dbc.Input(readonly=True, id="c_xyz_latex", type="text", className="text-center"),
                width=10  # Adjust width as needed
            ),
            className="d-flex justify-content-center align-items-center mb-4",  # Centers everything
        ),
        
        # First Derivative
        
        dcc.Markdown(r"""
            
            ***
            
            ## The first derivative 
            
            $$\alpha'=(X'(t),Y'(t),Z'(t))$$

        """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(
            id="c_d1", 
            mathjax=True, 
            className="mx-4 text-wrap w-90",
            style={
                "textAlign": "center", 
                "fontSize": "1.5em",
                "overflowWrap": "break-word", 
                "wordBreak": "break-word", 
                "whiteSpace": "normal",  
                "display": "block",  
                "maxWidth": "100%", 
                "overflowX": "auto"
            }
        ),
        
        dcc.Markdown(r"""

            #### Selectable $\LaTeX$

        """, mathjax=True, className="mx-4 mt-4 text-wrap", style={"textAlign" : "center"}),
        
        # Centered Row
        dbc.Row(
            dbc.Col(
                dbc.Input(readonly=True, id="c_d1_latex", type="text", className="text-center"),
                width=10  # Adjust width as needed
            ),
            className="d-flex justify-content-center align-items-center mb-4",  # Centers everything
        ),
        
        # Second Derivative
        
        dcc.Markdown(r"""
            
            ***
            
            ## The second derivative 
            
            $$\alpha''=(X''(t),Y''(t),Z''(t))$$

        """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(
            id="c_d2", 
            mathjax=True, 
            className="mx-4 text-wrap w-90",
            style={
                "textAlign": "center", 
                "fontSize": "1.5em",
                "overflowWrap": "break-word", 
                "wordBreak": "break-word", 
                "whiteSpace": "normal",  
                "display": "block",  
                "maxWidth": "100%", 
                "overflowX": "auto"
            }
        ),
        
        dcc.Markdown(r"""

            #### Selectable $\LaTeX$

        """, mathjax=True, className="mx-4 mt-4 text-wrap", style={"textAlign" : "center"}),
        
        # Centered Row
        dbc.Row(
            dbc.Col(
                dbc.Input(readonly=True, id="c_d2_latex", type="text", className="text-center"),
                width=10  # Adjust width as needed
            ),
            className="d-flex justify-content-center align-items-center mb-4",  # Centers everything
        ),
        
        # Third Derivative
        
        dcc.Markdown(r"""
            
            ***
            
            ## The third derivative 
             
            $$\alpha'''=(X'''(t),Y'''(t),Z'''(t))$$

        """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(
            id="c_d3", 
            mathjax=True, 
            className="mx-4 text-wrap w-90",
            style={
                "textAlign": "center", 
                "fontSize": "1.5em",
                "overflowWrap": "break-word", 
                "wordBreak": "break-word", 
                "whiteSpace": "normal",  
                "display": "block",  
                "maxWidth": "100%", 
                "overflowX": "auto"
            }
        ),
        
        dcc.Markdown(r"""

            #### Selectable $\LaTeX$

        """, mathjax=True, className="mx-4 mt-4 text-wrap", style={"textAlign" : "center"}),
        
        # Centered Row
        dbc.Row(
            dbc.Col(
                dbc.Input(readonly=True, id="c_d3_latex", type="text", className="text-center"),
                width=10  # Adjust width as needed
            ),
            className="d-flex justify-content-center align-items-center mb-4",  # Centers everything
        ),
        
        # Curvature and Torsion
        
        dcc.Markdown(r"""
            
            ***
            
            ## The Speed $||\alpha'||$, Curvature $\kappa$, and the Torsion $\tau$
            
            Due to computational cost and complexity, these functions may not be simplified from their explicit formula. Trigonometric expressions are not simplified by **mathjs**.
        

        """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(
            id="c_kappa_tau", 
            mathjax=True, 
            className="mx-4 text-wrap w-90",
            style={
                "textAlign": "center", 
                "fontSize": "1.5em",
                "overflowWrap": "break-word", 
                "wordBreak": "break-word", 
                "whiteSpace": "normal",  
                "display": "block",  
                "maxWidth": "100%", 
                "overflowX": "auto"
            }
        ),
        
        dcc.Markdown(r"""

            #### Selectable $\LaTeX$

        """, mathjax=True, className="mx-4 mt-4 text-wrap", style={"textAlign" : "center"}),
        
        # Centered Row
        dbc.Row(
            dbc.Col(
                dbc.Input(readonly=True, id="c_kappa_tau_latex", type="text", className="text-center"),
                width=10  # Adjust width as needed
            ),
            className="d-flex justify-content-center align-items-center mb-4",  # Centers everything
        ),
        
        dcc.Store(id="c_kappa_tau_plot_data"),
        
        # Kappa and Tau plot
        dcc.Graph(id="c_kappa_tau_plot"),
        
        # Frenet–Serret frame
        
        dcc.Markdown(r"""
            
            ***
            
            ## Frenet-Serret Frame
            
            Also known as a "TNB Frame" for Tangent, Normal, Binormal:
             
            $\mathbf{T}(t)$ is the curve's unit Tangent vector at $t$
            
            $\mathbf{N}(t)$ is the curve's unit Normal vector at $t$
            
            $\mathbf{B}(t)$ is the curve's unit Binormal vector at $t$
            
            Due to computational cost and complexity, these functions may not be simplified from their explicit formula. Trigonometric expressions are not simplified by **mathjs**.
            
            *Will display the zero vector when not well-defined.*

        """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(
            id="c_TNB", 
            mathjax=True, 
            className="mx-4 text-wrap w-90",
            style={
                "textAlign": "center", 
                "fontSize": "1.5em",
                "overflowWrap": "break-word", 
                "wordBreak": "break-word", 
                "whiteSpace": "normal",  
                "display": "block",  
                "maxWidth": "100%", 
                "overflowX": "auto"
            }
        ),
        
        dcc.Markdown(r"""

            #### Selectable $\LaTeX$

        """, mathjax=True, className="mx-4 mt-4 text-wrap", style={"textAlign" : "center"}),
        
        # Centered Row
        dbc.Row(
            dbc.Col(
                dbc.Input(readonly=True, id="c_TNB_latex", type="text", className="text-center"),
                width=10  # Adjust width as needed
            ),
            className="d-flex justify-content-center align-items-center mb-4",  # Centers everything
        ),
        

        
    ],
    
    id = "curves_analytics_container",
    
    style = {'display' : 'none'}
    
)

surfaces = html.Div(
    
    [
        
        dcc.Store(id = "surfaces_analytics", storage_type='memory'),
        
        dcc.Store(id = "store_surfaces_data", storage_type='memory'),
        
        dcc.Markdown(r"""

            # Surface Analytics
            
            ***
            
            ## The surface $S$

        """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
    ],
    
    id = "surfaces_analytics_container",
    
    style = {'display' : 'none'}
    
)

embedded_curves = html.Div(
    
    [
        
        dcc.Store(id = "embedded_curves_analytics", storage_type='memory'),
        
        dcc.Store(id = "store_embedded_curves_data", storage_type='memory'),
        
        dcc.Markdown(r"""

            # Curve on a Surface Analytics
            
            ***
            
            ## The surface $S$

        """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
    ],
    
    id = "embedded_curves_analytics_container",
    
    style = {'display' : 'none'}
    
)

layout = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Div(
                    
                    children = [
                        
                        dbc.Row(
                            dbc.Col(dbc.Button("Compute Analytics", id="analytics_button", color="warning", disabled=True), width="auto"),
                            justify="center", className="m-4"
                        ),
                        
                        not_yet_rendered,
                        curves,
                        surfaces,
                        embedded_curves,

                    ]
                )
            ]
        ),
    ],
    className = "px-0"
)

clientside_callback(
    """
    function(data, n_clicks) {
        
    const triggered = dash_clientside.callback_context.triggered.map(t => t.prop_id)
    
    if (triggered[0] === "store_math.data" && data.rendered) {
        
        return false;
    } else {
        
        return true;
    }
        
    }
    """,
    Output("analytics_button", "disabled"),
    Input("store_math", "data"),
    Input("analytics_button", "n_clicks")
)

clientside_callback(
    """
    function(is_disabled) {
        
        if (is_disabled) {
            return "warning";
        } else {
            return "success";
        }
        
    }
    """,
    Output("analytics_button", "color"),
    Input("analytics_button", "disabled"),
)


@callback(
    Output("curves_analytics_container", "style"),
    Output("surfaces_analytics_container", "style"),
    Output("embedded_curves_analytics_container", "style"),
    Output("not_yet_rendered_analytics_container", "style"),
    
    Output("store_curves_data", "data"),
    Output("store_surfaces_data", "data"),
    Output("store_embedded_curves_data", "data"),
    
    Input("analytics_button", "n_clicks"),

    Input("store_math", "data"),
    
    prevent_initial_callback=True
)
def analytics_content(n_clicks, data) :
    
    hide = {'display' : 'none'}
    show = {'display' : 'block'}
    
    if ctx.triggered_id == "store_math" :
        return hide, hide, hide, show, no_update, no_update, no_update
    
    if data['rendered'] :
        
        if data['subject'] == "render_curve" :
            return show, hide, hide, hide, data, no_update, no_update
        
        if data['subject'] == "render_surface" :
            
            return hide, show, hide, hide, no_update, data, no_update

        if data['subject'] == "render_embedded_curve" :
            return hide, hide, show, hide, no_update, no_update, data
        
    return hide, hide, hide, show, no_update, no_update, no_update


# callback function for rendering analytics
clientside_callback(
    ClientsideFunction(namespace="differential_geometry", function_name="render_curve_analytics"),
    Output("c_xyz", "children"),
    Output("c_xyz_latex", "value"),
    Output("c_d1", "children"),
    Output("c_d1_latex", "value"),
    Output("c_d2", "children"),
    Output("c_d2_latex", "value"),
    Output("c_d3", "children"),
    Output("c_d3_latex", "value"),
    Output("c_kappa_tau", "children"),
    Output("c_kappa_tau_latex", "value"),
    Output("c_TNB", "children"),
    Output("c_TNB_latex", "value"),
    Output("c_kappa_tau_plot_data", "data"),
    Input("store_curves_data", "data"),
    prevent_initial_call=True  # This stops it from running on page load
)

@callback(
    Output("c_kappa_tau_plot", "figure"),
    Input("c_kappa_tau_plot_data", "data"),
    Input('theme-switch', 'value'),
)
def c_tau_kappa_plot_callback(curve_data, light):
    
    if curve_data is None :
        return go.Figure()
    
    # Extract curvature and torsion from curve_data
    speed_values = curve_data["speed"]
    curvature_values = curve_data["curvature"]
    torsion_values = curve_data["torsion"]
    
    # Convert to single precision floats (float32)
    # this is to eliminate annoying (double) precision errors
    speed_values = np.array(speed_values, dtype=np.float32)
    curvature_values = np.array(curvature_values, dtype=np.float32)
    torsion_values = np.array(torsion_values, dtype=np.float32)
    
    # Create a list of t values (use range for plotting, or create your own)
    t_values = curve_data["t_values"]  # Assuming curve_data['curvature'] and ['torsion'] are of same length
    
    # Create the figure
    fig = go.Figure()

    # Plot Speed
    fig.add_trace(go.Scatter(
        x=t_values,
        y=speed_values,
        mode='lines+markers',
        name="Speed",
        line=dict(color='green'),
    ))

    # Plot Curvature (kappa)
    fig.add_trace(go.Scatter(
        x=t_values,
        y=curvature_values,
        mode='lines+markers',
        name="Curvature (κ)",
        line=dict(color='blue'),
    ))

    # Plot Torsion (tau)
    fig.add_trace(go.Scatter(
        x=t_values,
        y=torsion_values,
        mode='lines+markers',
        name="Torsion (τ)",
        line=dict(color='red'),
    ))
    
    theme = "plotly_dark"
    
    if (light) :
        theme = "plotly_white"

    # Customize the layout
    fig.update_layout(
        title="Curvature and Torsion vs. t",
        xaxis_title="t",
        yaxis_title="Value",
        legend_title="Metrics",
        template=theme,
        hovermode="closest"
    )

    # Return the plotly figure
    return fig

