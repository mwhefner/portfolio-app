import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input, State, clientside_callback, no_update, ClientsideFunction, ctx
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

not_yet_rendered = html.Div(
    [
        dcc.Markdown(r"""

            Analytics can be computed here after a subject has been rendered.
            
            *Note that these are computed in real time and rendered in $\LaTeX$. This must be done by the "main thread," so to speak, so __large or complicated expressions may take some time to render and lead to sluggish performance.__*
            
            **Complicated surfaces** (e.g. Klein Bottle) and surfaces with a high $n_u$ or $n_v$ may take upwards of a minute to compute analytics for, during which time your browser's performance may be significantly impacted. *It is recommended to open WebDG in a dedicated browser window for such surfaces.*

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
        
        dcc.Store(id = "store_surfaces_data", storage_type='memory'),
        
        # TITLE AND XYZ COMPONENTS
        
        dcc.Markdown(r"""

            # Surface Analytics
            
            ***
            
            **NOTICE** 
            
            These calculations are done using [mathjs](https://mathjs.org). Please be aware that, while the results presented are typically accurate, mathjs generally __does not *simplify* trigonometric expressions.__
            
            Large equations scroll horizontally.
            
            The results below come with no guarantee of accuracy or fitness for any purpose.
            
            ***
            
            ## The surface
            
            $$S = \big( X(u,v), Y(u,v), Z(u,v) \big)$$

        """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(
            id="s_xyz", 
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
                dbc.Input(readonly=True, id="s_xyz_latex", type="text", className="text-center"),
                width=10  # Adjust width as needed
            ),
            className="d-flex justify-content-center align-items-center mb-4",  # Centers everything
        ),
        
        # JACOBIAN
        
        dcc.Markdown(r"""

            ***

            # The Jacobian
            
            All first-order partial derivatives.
            
            $$
            J =
            \begin{bmatrix} S_u & S_v \end{bmatrix}=
            \begin{bmatrix}
            \frac{\partial X}{\partial u} & \frac{\partial X}{\partial v} \\
            \frac{\partial Y}{\partial u} & \frac{\partial Y}{\partial v} \\
            \frac{\partial Z}{\partial u} & \frac{\partial Z}{\partial v}
            \end{bmatrix}
            $$

        """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(
            id="s_jacobian", 
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
                dbc.Input(readonly=True, id="s_jacobian_latex", type="text", className="text-center"),
                width=10  # Adjust width as needed
            ),
            className="d-flex justify-content-center align-items-center mb-4",  # Centers everything
        ),
        
        # HESSIAN(S)
        
        dcc.Markdown(r"""
                     
            ***

            # The Hessian(s)
            
            All second-order partial derivatives.
            
            $$
            H_X =
            \begin{bmatrix}
            \frac{\partial^2 X}{\partial u^2} & \frac{\partial^2 X}{\partial u \partial v} \\
            \frac{\partial^2 X}{\partial v \partial u} & \frac{\partial^2 X}{\partial v^2}
            \end{bmatrix},
            $$
            
            $$
            H_Y =
            \begin{bmatrix}
            \frac{\partial^2 Y}{\partial u^2} & \frac{\partial^2 Y}{\partial u \partial v} \\
            \frac{\partial^2 Y}{\partial v \partial u} & \frac{\partial^2 Y}{\partial v^2}
            \end{bmatrix},
            $$
            
            $$
            H_Z =
            \begin{bmatrix}
            \frac{\partial^2 Z}{\partial u^2} & \frac{\partial^2 Z}{\partial u \partial v} \\
            \frac{\partial^2 Z}{\partial v \partial u} & \frac{\partial^2 Z}{\partial v^2}
            \end{bmatrix}
            $$

        """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(
            id="s_hessian", 
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
                dbc.Input(readonly=True, id="s_hessian_latex", type="text", className="text-center"),
                width=10  # Adjust width as needed
            ),
            className="d-flex justify-content-center align-items-center mb-4",  # Centers everything
        ),
        
        # FIRST FUNDAMENTAL FORM
        
        dcc.Markdown(r"""
                     
            ***

            # First Fundamental Form Coefficients $E$, $F$, and $G$
            
            $$
            \begin{bmatrix}
            E & F \\
            F & G
            \end{bmatrix}
            =
            \begin{bmatrix}
            S_u \cdot S_u & S_u \cdot S_v \\
            S_v \cdot S_u & S_v \cdot S_v
            \end{bmatrix}
            $$

        """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(
            id="s_fff", 
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
                dbc.Input(readonly=True, id="s_fff_latex", type="text", className="text-center"),
                width=10  # Adjust width as needed
            ),
            className="d-flex justify-content-center align-items-center mb-4",  # Centers everything
        ),
        
                # FIRST FUNDAMENTAL FORM
        
        # SECOND FUNDAMENTAL FORM
        
        dcc.Markdown(r"""
                     
            ***

            # Second Fundamental Form Coefficients $L$, $M$, and $N$
            
            $$
            \mathbf{n} = \frac{S_u \times S_v}{|S_u \times S_v|}
            $$
            
            $$
            \begin{bmatrix}
            L & M \\
            M & N
            \end{bmatrix}
            =
            \begin{bmatrix}
            S_{uu} \cdot \mathbf{n} & S_{uv} \cdot \mathbf{n} \\
            S_{vu} \cdot \mathbf{n} & S_{vv} \cdot \mathbf{n}
            \end{bmatrix}
            $$

        """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(
            id="s_sff", 
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
                dbc.Input(readonly=True, id="s_sff_latex", type="text", className="text-center"),
                width=10  # Adjust width as needed
            ),
            className="d-flex justify-content-center align-items-center mb-4",  # Centers everything
        ),
        
        
        # Gaussian $K$, Mean $H$, and Principal ($\kappa_1$ and $\kappa_2$) Curvatures
        
        dcc.Markdown(r"""
                     
            ***

            # Gaussian $K$, Mean $H$, and Principal ($\kappa_1$ and $\kappa_2$) Curvatures
            
            $$
            K = \frac{LN - M^2}{EG - F^2}
            $$
            
            $$
            H = \frac{EN - 2FM + GL}{2(EG - F^2)}
            $$
            
            $$
            \kappa_1 = H + \sqrt{H^2 - K}
            $$
            
            $$
            \kappa_2 = H - \sqrt{H^2 - K}
            $$

        """, mathjax=True, className="mx-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Markdown(
            id="s_curvatures", 
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
                dbc.Input(readonly=True, id="s_curvatures_latex", type="text", className="text-center"),
                width=10  # Adjust width as needed
            ),
            className="d-flex justify-content-center align-items-center mb-4",  # Centers everything
        ),
        
        # surface curvature plots
        dcc.Store(id="s_curvature_plot_data"),
        
        dcc.Markdown(r"""

            ##### Gaussian

        """, mathjax=True, className="mx-4 mt-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Graph(figure = go.Figure(), id="s_curvature_plot_K"),
        
        dcc.Markdown(r"""

            ##### Mean

        """, mathjax=True, className="mx-4 mt-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Graph(figure = go.Figure(), id="s_curvature_plot_H"),
        
        dcc.Markdown(r"""

            ##### Principal $\kappa_1$

        """, mathjax=True, className="mx-4 mt-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Graph(figure = go.Figure(), id="s_curvature_plot_k1"),
        
        dcc.Markdown(r"""

            ##### Principal $\kappa_2$

        """, mathjax=True, className="mx-4 mt-4 text-wrap", style={"textAlign" : "center"}),
        
        dcc.Graph(figure = go.Figure(), id="s_curvature_plot_k2"),
        
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


# callback functions for rendering curve analytics
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


# callback functions for rendering surface analytics
clientside_callback(
    ClientsideFunction(namespace="differential_geometry", function_name="render_surface_analytics"),
    Output("s_xyz", "children"),
    Output("s_xyz_latex", "value"),
    
    Output("s_jacobian", "children"),
    Output("s_jacobian_latex", "value"),
    Output("s_hessian", "children"),
    Output("s_hessian_latex", "value"),
    Output("s_fff", "children"),
    Output("s_fff_latex", "value"),
    Output("s_sff", "children"),
    Output("s_sff_latex", "value"),
    Output("s_curvatures", "children"),
    Output("s_curvatures_latex", "value"),
    Output("s_curvature_plot_data", "data"),
    
    Input("store_surfaces_data", "data"),

    prevent_initial_call=True  # This stops it from running on page load
)

def makeSurfaceCurvaturePlot(surface_data, light, c):
    if surface_data is None:
        return go.Figure()

    # Set theme
    theme = "plotly_dark" if not light else "plotly_white"
    u = np.array(surface_data['u'])
    v = np.array(surface_data['v'])

    # Create the figure with the Heatmap trace
    fig = go.Figure(data=go.Heatmap(
        x=v,
        y=u,
        z=surface_data[c],
        colorscale='Cividis',  # Set the color scale
        hovertemplate=(
            'u: %{x}<br>'    # Display the u value
            'v: %{y}<br>'    # Display the v value
            '{c}: %{z}'  # Display the selected column value (with 2 decimal places)
            '<extra></extra>'  # Remove the extra trace information (default behavior)
        )
    ))

    # Ensure the axis labels and ranges are set correctly
    fig.update_layout(
        template=theme,
        margin=dict(t=0, b=0, l=0, r=0),
        xaxis=dict(
            title="u",  # Label the x-axis as "u"
            range=[v.min(), v.max()],  # Set x-axis range to match u
            scaleanchor="y",  # Lock x-axis to y-axis for equal scaling
        ),
        yaxis=dict(
            title="v",  # Label the y-axis as "v"
            range=[u.min(), u.max()],  # Set y-axis range to match v
            scaleanchor="x",  # Lock y-axis to x-axis for equal scaling
            autorange="reversed"  # Reverse the y-axis as needed
        ),
        autosize=True,  # Allow the figure to resize to the container's size
    )


    return fig


@callback(
    Output("s_curvature_plot_K", "figure"),
    Input("s_curvature_plot_data", "data"),
    Input('theme-switch', 'value'),
)
def c_tau_kappa_plot_callback(surface_data, light):
    
    return makeSurfaceCurvaturePlot(surface_data, light, 'K')

@callback(
    Output("s_curvature_plot_H", "figure"),
    Input("s_curvature_plot_data", "data"),
    Input('theme-switch', 'value'),
)
def c_tau_kappa_plot_callback(surface_data, light):
    
    return makeSurfaceCurvaturePlot(surface_data, light, 'H')

@callback(
    Output("s_curvature_plot_k1", "figure"),
    Input("s_curvature_plot_data", "data"),
    Input('theme-switch', 'value'),
)
def c_tau_kappa_plot_callback(surface_data, light):
    
    return makeSurfaceCurvaturePlot(surface_data, light, 'k_1')

@callback(
    Output("s_curvature_plot_k2", "figure"),
    Input("s_curvature_plot_data", "data"),
    Input('theme-switch', 'value'),
)
def c_tau_kappa_plot_callback(surface_data, light):
    
    return makeSurfaceCurvaturePlot(surface_data, light, 'k_2')