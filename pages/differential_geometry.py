import dash
from dash import html, dcc, Input, Output, State, clientside_callback, register_page, ClientsideFunction
import dash_bootstrap_components as dbc
import pages.differential_geometry.subjects as dg_subjects
import pages.differential_geometry.analytics as dg_analytics
import pages.differential_geometry.settings as dg_settings

register_page(
    __name__, 
    path="/webdg", 
    name="WebDG", 
    title="WebDG", 
    description="**WebDG** is a free **Web** application for **D**ifferential **G**eometry education. WebDG provides students and instructors a free and accessible web app robust enough to interactively explore abstract differentiable curves and surfaces without the substantial overhead of learning to script computer algebra systems.", 
    image="/assets/as_webp/webdg.webp"
)

# Is the following necessary for anything?
'''clientside_callback(
    """
    function(n_clicks) {
        //console.log("Button pressed.");
    }
    """,
    Output("DGWE_Store", "data"),
    Input("DGWE_start", "n_clicks"),
    prevent_initial_call=True 
)'''

# Page layout
layout = html.Div(
    [
    
    # "utility" components
    
    dcc.Store(data= {'rendered':False}, id='store_math', storage_type='memory'),

    dcc.Store(id="stop_orbit_control_on_modal_open"),
    
    dcc.Store(id = "refresh_dummy_target"),
    
    dcc.Store(id = "killswitch_dummy_target"),
    
    dcc.Location(id='webdg_url', refresh=False),

    
    # Help menu button
    dbc.Stack([
        dbc.Button(
            dbc.Col(html.I(className="fa-solid fa-question fs-2"), align="center"),
            id="help-button",
            color="primary",
            style={"borderRadius": "50%", "aspectRatio": "1 / 1"}
        )
    ], className="position-fixed bottom-0 start-0 m-3"),

    # 4 Buttons at the top
    dbc.Row(
        [
            dbc.Col(
                dbc.Button(
                    dbc.Row([
                        
                        dbc.Col(html.Span("Reset 3D Engine", className="fw-bold"), width="auto"),
                        
                        dbc.Col(html.I(className="fa-solid fa-rotate"), width="auto", className="text-end")
                        
                    ], className="d-flex justify-content-between align-items-center", align="center"),
                    
                    id="re_start_engine", color="primary", n_clicks=0, style={"width": "100%"}),
                
                width=True, className="m-3"
            ),
            dbc.Col(
                dbc.Button(
                    dbc.Row([
                        
                        dbc.Col(html.Span("Subjects", className="fw-bold"), width="auto"),
                        
                        dbc.Col(html.I(className="fa-solid fa-subscript"), width="auto", className="text-end")
                        
                    ], className="d-flex justify-content-between align-items-center", align="center"),
                    
                    id="subject", color="primary", n_clicks=0, style={"width": "100%"}),
                
                width=True, className="m-3"
            ),
            dbc.Col(
                dbc.Button(
                    dbc.Row([
                        
                        dbc.Col(html.Span("Analytics", className="fw-bold"), width="auto"),
                        
                        dbc.Col(html.I(className="fa-solid fa-chart-line"), width="auto", className="text-end")
                        
                    ], className="d-flex justify-content-between align-items-center", align="center"),
                    
                    id="analytics", color="primary", n_clicks=0, style={"width": "100%"}),
                
                width=True, className="m-3"
            ),
            dbc.Col(
                dbc.Button(
                    dbc.Row([
                        
                        dbc.Col(html.Span("Settings", className="fw-bold"), width="auto"),
                        
                        dbc.Col(html.I(className="fa-solid fa-gear"), width="auto", className="text-end")
                        
                    ], className="d-flex justify-content-between align-items-center", align="center"),
                    
                    id="settings", color="primary", n_clicks=0, style={"width": "100%"}),
                
                width=True, className="m-3"
            ),
        ],
        justify="space-between"
    ),
    
    # help popover
    dbc.Popover(
        dbc.PopoverBody(html.Em("expand info modal about WebDG")),
        target="help-button",
        trigger="hover",
        placement="right"
    ),
        
    # Subjects Modal
    dbc.Modal(
        [

            dbc.ModalHeader(dbc.ModalTitle("Subjects")),
            
            dbc.ModalBody(
                dg_subjects.layout
            ),
            dbc.ModalFooter(

                dbc.Row([
                    dbc.Button(
                        "Close",
                        id="close_subject_modal",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ], justify="center", style={"textAlign": "center"}, className = "gap-3")

            ),
        ],
        id="subject_modal",
        centered=True,
        size="lg"
    ),
        
    # Analytics Modal
    dbc.Modal(
        [

            dbc.ModalHeader(dbc.ModalTitle("Products of Analysis")),
            dbc.ModalBody(
                dg_analytics.layout
            ),
            dbc.ModalFooter(

                dbc.Row([
                    dbc.Button(
                        "Close",
                        id="close-analytics-modal",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ], justify="center", style={"textAlign": "center"}, className = "gap-3")

            ),
        ],
        id="analytics-modal",
        centered=True,
        size="lg"
    ),
        
    # Settings Modal
    dbc.Modal(
        [

            dbc.ModalHeader(dbc.ModalTitle("WebDG Settings")),
            dbc.ModalBody(
                dg_settings.layout
            ),
            dbc.ModalFooter(

                dbc.Row([
                    dbc.Button(
                        "Close",
                        id="close-settings-modal",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ], justify="center", style={"textAlign": "center"}, className = "gap-3")

            ),
        ],
        id="settings-modal",
        centered=True,
        size="lg"
    ),
    
    # Help Modal
    dbc.Modal(
        [

            dbc.ModalHeader(dbc.ModalTitle("Welcome!")),
            dbc.ModalBody(
                [
                    
                dcc.Markdown(
                    r"""          
          
                    **WebDG**
                    
                    """,
                    style={
                        "textAlign": "center", 
                        "fontSize": "3em",
                    }
                    
                ),
                
                html.Img(src="/assets/as_webp/webdg.webp", 
                        style={"height": "200px", "display": "block", "margin": "0 auto", "marginBottom": "1.5rem"},
                        alt="A Klein bottle at an angle."),
                
                dcc.Markdown(
                    r"""          
                    
                    Version 1.0.1
                    
                    _A free **Web** application for **D**ifferential **G**eometry education._
                    
                    """,
                    style={
                        "textAlign": "center", 
                        "fontSize": "1.25em",
                    }
                    
                ),
                
                dcc.Markdown(
                    """

                    ***
                    
                    #### About
                    """, mathjax=True, className="mb-5"
                ),
                
                dcc.Markdown(
                    r"""    
                    Made for both students and instructors, WebDG is a free and accessible web app robust enough to interactively explore the differential geometry of abstract curves and surfaces without the substantial overhead of learning to script computer algebra systems.
                    
                    **This software is free for anyone to use to learn or to teach others about differential geometry. No login, download, license, or subscription is required.**
                    
                    This app costs money to maintain and keep online. People like you can keep this tool free and available for everyone with [a one-time or recurring donation through Buy Me a Coffee.](https://www.buymeacoffee.com/mwhefner) All major credit cards are accepted and no login is required to donate.
                    
                    **You can also show your support by sharing this app!**
                    
                    ***
                    
                    #### What does it do?
                    
                    """, mathjax=True, className="mb-5"
                ),
                
                dcc.Markdown(
                    r"""    
                    
                    ##### Subjects
                    
                    WebDG can be used to study either an abstract parametric curve or surface in space. Give WebDG the $\mathbb{R}^3$ parameterization of your differentiable manifold to see an interactive visualization and analytics.
                    
                    """, mathjax=True, className="mb-5"
                ),
                
                dcc.Markdown(
                    r"""    
                    
                    ##### Analytics
                    
                    For **curves**, WebDG symbolically computes explicit formulas for:
                    
                    - the first, second, and third derivatives;
                    - the Frenet-Serret frame;
                    - the speed;
                    - the curvature;
                    - and the torsion
                    
                    with plots for the latter three.
                    
                    For **surfaces**, WebDG symbolically computes explicit formulas for:
                    
                    - the Jacobian (all first-order partial derivatives),
                    - the Hessian(s) (all second-order partial derivatives),
                    - the First Fundamental Form coefficients,
                    - the Second Fundamental Form coefficients,
                    - and the Gaussian, mean, and principal curvatues
                    
                    with plots for the three curvatures.
                    
                    ***
                    
                    #### Citation
                    """, mathjax=True, className="mb-5"
                ),
                
                dcc.Markdown(
                    r"""    
                    As a professional courtesy, I ask to be acknowledged with citation when appropriate.
                    
                    **Author:** Hefner, M. W.
                    
                    **Title:** WebDG
                    
                    **URL:** https://mathymattic.pythonanywhere.com/webdg
                    
                    ***
                    
                    #### Acknowledgements
                    """, mathjax=True, className="mb-5"
                ),
                
                dcc.Markdown(
                    r"""    

                    This application is built with free and open source technologies. To read more about the software used, see the [Dash web application framework](https://dash.plotly.com/), [mathjs](https://mathjs.org), and the [p5.js javascript library](https://p5js.org/). To suggest features, report a bug, or get more information, please select the "creator" button at the bottom right.
                    
                    ***
                    
                    """, mathjax=True
                ),
                
                dcc.Markdown(
                    r"""          
                    
                    **Reopen this info modal at any time by selecting the question mark at the bottom left.**
                    
                    """,
                    style={
                        "textAlign": "center", 
                        "fontSize": "1.25em",
                    }
                    
                ),
                
                ]
            ),
            dbc.ModalFooter(

                dbc.Row([
                    dbc.Button(
                        "Close Info Modal",
                        id="close-help-modal",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ], justify="center", style={"textAlign": "center"}, className = "gap-3")

            ),
        ],
        id="help-modal",
        centered=True,
        size="lg"
    ),
    

    
    dbc.Alert(["WebDG is ready! Change the visualization by rendering a subject to study using the Subjects (", html.I(className="fa-solid fa-subscript"), ") menu above. You can close info alerts such as this with the X to the right."], color="info", dismissable=True, is_open=True, className = "m-3", id="refresh_alert", style = { 'user-select': 'none' }),
    
    dbc.Alert([dbc.Spinner(color="warning", size="sm"), " Please wait while WebDG is processing your subject."], id= "rendering_alert", color="warning", dismissable=False, is_open=True, className = "m-3", style = { 'display': 'none', 'user-select': 'none' }),

    dbc.Alert(
        [
            'Success! WebDG has rendered your subject. Orbit your view around the focal point by left-clicking and dragging. Move the focal point with the arrow keys, and hold shift while pressing the up or down arrow to move it forward or backward. Zoom using the mouse wheel. Explore more adjustments in the Settings menu with the ',
            html.I(className="fa-solid fa-gear"),
            ' icon on the top right.'
        ],
        color="success",
        dismissable=True,
        id="success_alert",
        is_open=True,
        className="m-3",
        style={'display': 'none', 'user-select': 'none'}  # Disable text selection
    ),

    
    dbc.Alert(["Sorry, WebDG failed to render your subject. Please try again."], id = "failure_alert", color="danger", dismissable=False, is_open=True, className = "m-3", style = { 'display': 'none', 'user-select': 'none' }),
        
    ],
    
    style={
        "display": "flex",
        "flexDirection": "column",
        "height": "100vh"  # Makes the whole app take up the full viewport height
    }
)

"""dbc.Alert(["Use the Refresh (", html.I(className="fa-solid fa-rotate"), ") button at the top left to start (and to re-start) the WebDG graphing calculator. You can close info alerts such as this with the X to the right."], color="info", dismissable=True, is_open=True, className = "m-3", style = { 'user-select': 'none' }),"""

# this callback opens the "engine refreshed" alert when the refresh button is pressed
clientside_callback(
    """
    function(n_clicks) {
        return true;
    }
    """,
    Output("refresh_alert", "is_open"),
    [Input("re_start_engine", "n_clicks")],
    prevent_initial_call=True,
)

# This callback runs the refresh function
clientside_callback(
    ClientsideFunction(namespace="differential_geometry", function_name="refresh"),
    Output("refresh_dummy_target", "data"),
    Input("re_start_engine", "n_clicks")
)

# This callback will run the 'killswitch_engage' function when the URL changes
clientside_callback(
    ClientsideFunction(namespace="differential_geometry", function_name="killswitch_engage"),
    Output("killswitch_dummy_target", "data"),
    Input("webdg_url", "pathname")  # Trigger when the URL changes
)

# The following callbacks operate the modals for the Subject,
# Analytics, and Settings

## Subject
clientside_callback(
    """
    function(n_1, n_2, is_open) {
        
        return !is_open;
        
    }
    """,
    Output("subject_modal", "is_open"),
    [
        Input("subject", "n_clicks"), 
        Input("close_subject_modal", "n_clicks")
    ],
    State("subject_modal", "is_open"),
    prevent_initial_call=True,
)

## Analytics
clientside_callback(
    """
    function(n_clicks, n_2, is_open) {
        return !is_open;
    }
    """,
    Output("analytics-modal", "is_open"),
    [Input("analytics", "n_clicks"), Input("close-analytics-modal", "n_clicks")],
    State("analytics-modal", "is_open"),
    prevent_initial_call=True,
)

## Settings
clientside_callback(
    """
    function(n_clicks, n_2, is_open) {
        return !is_open;
    }
    """,
    Output("settings-modal", "is_open"),
    [Input("settings", "n_clicks"), Input("close-settings-modal", "n_clicks")],
    State("settings-modal", "is_open"),
    prevent_initial_call=True,
)

## Help
clientside_callback(
    """
    function(n_clicks, n_2, is_open) {
        return !is_open;
    }
    """,
    Output("help-modal", "is_open"),
    [Input("help-button", "n_clicks"), Input("close-help-modal", "n_clicks")],
    State("help-modal", "is_open"),
    prevent_initial_call=False,
)

clientside_callback(
    """
    function(subject, analytics, settings, theme, portfolio, help) {
        let dg = window.dash_clientside.differential_geometry;
        let allClosed = !subject && !analytics && !settings && !theme && !portfolio && !help;
        dg.orbitControlled = allClosed;
        return "";
    }
    """,
    Output("stop_orbit_control_on_modal_open", "data"),
    Input("subject_modal", "is_open"),
    Input("analytics-modal", "is_open"),
    Input("settings-modal", "is_open"),
    Input("theme-modal", "is_open"),
    Input("portfolio-modal", "is_open"),
    Input("help-modal", "is_open"),
)
