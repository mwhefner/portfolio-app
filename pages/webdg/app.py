"""

webdg.py

This defines the home, "landing" or "index" page of the portfolio.

In addition to structuring the Dash application properly,
to run this application on its own, all one must do is replace
the page registration below with the multipage app with an app
initialization and define the app.layout to be the layout below.

M W Hefner, 2025
MIT License

"""

from dash import html, dcc, Input, Output, State, clientside_callback, register_page, ClientsideFunction
import dash_bootstrap_components as dbc
import pages.webdg.subjects as dg_subjects
import pages.webdg.analytics as dg_analytics
import pages.webdg.settings as dg_settings
import pages.webdg.updates as dg_updates

# Page registration
register_page(
    __name__, 
    path="/webdg", 
    name="WebDG 1.0.3", 
    title="WebDG 1.0.3", 
    description="""WebDG is for anyone studying, teaching, or just curious about differential geometry. It is a free, open-source web app robust enough to explore interactive 3D visualizations and analyses of abstract curves and surfaces without the substantial overhead of learning to script computer algebra systems.""",
    image="/assets/webp/thumbnails/webdg.webp"
)

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
            # Refresh
            dbc.Col(
                dbc.Button(
                    dbc.Row([
                        
                        dbc.Col(html.Span("Reset", className="fw-bold"), width="auto"),
                        
                        dbc.Col(html.I(className="fa-solid fa-rotate"), width="auto", className="text-end")
                        
                    ], className="d-flex justify-content-between align-items-center", align="center"),
                    
                    id="re_start_engine", color="primary", n_clicks=0, style={"width": "100%"}),
                
                width=True, className="m-3"
            ),
            # Subjects
            dbc.Col(
                dbc.Button(
                    dbc.Row([
                        
                        dbc.Col(html.Span("Subjects", className="fw-bold"), width="auto"),
                        
                        dbc.Col(html.I(className="fa-solid fa-subscript"), width="auto", className="text-end")
                        
                    ], className="d-flex justify-content-between align-items-center", align="center"),
                    
                    id="subject", color="primary", n_clicks=0, style={"width": "100%"}),
                
                width=True, className="m-3"
            ),
            # Analytics
            dbc.Col(
                dbc.Button(
                    dbc.Row([
                        
                        dbc.Col(html.Span("Analytics", className="fw-bold"), width="auto"),
                        
                        dbc.Col(html.I(className="fa-solid fa-chart-line"), width="auto", className="text-end")
                        
                    ], className="d-flex justify-content-between align-items-center", align="center"),
                    
                    id="analytics", color="primary", n_clicks=0, style={"width": "100%"}),
                
                width=True, className="m-3"
            ),
            # Settings
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
    
    # Updates Modal
    dbc.Modal(
        [

            dbc.ModalHeader(dbc.ModalTitle("Updates")),
            dbc.ModalBody(
                dg_updates.layout
            ),
            dbc.ModalFooter(

                dbc.Row([
                    dbc.Button(
                        "Close",
                        id="close-updates-modal",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ], justify="center", style={"textAlign": "center"}, className = "gap-3")

            ),
        ],
        is_open=False,
        id="updates-modal",
        centered=True,
        size="lg"
    ),
    
    # Help/information/welcome Modal
    dbc.Modal(
        [

            dbc.ModalHeader(dbc.ModalTitle("Welcome")),
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
                
                dcc.Markdown(
                    r"""          
                    
                    Version 1.0.3
                    
                    """,
                    style={
                        "textAlign": "center"
                    }
                    
                ),
                
                dbc.Carousel(
                    items=[
                        {"key": "1", "src": "/assets/webp/images/webdg3.webp", "caption" : "A Gyroid"},
                        {"key": "2", "src": "/assets/webp/images/webdg6.webp", "caption" : "A Cross Section of a Schwarz Surface"},
                        #{"key": "3", "src": "/assets/webp/images/webdg2.webp", "caption" : "A Helicatenoid"},
                        #{"key": "4", "src": "/assets/webp/images/webdg6.webp", "caption" : "Cross Section of a Gyroid"},
                        {"key": "3", "src": "/assets/webp/images/webdg5.webp", "caption" : "A Figure-8 Immersion of a Klein Bottle"},
                        {"key": "4", "src": "/assets/webp/images/webdg4.webp", "caption" : "A Frenet-Serret Frame on a Torus Knot"},
                    ],
                    controls=True,
                    indicators=False,
                    className="carousel-fade",
                    interval=3000,
                ),
                
                dbc.Row(
                    dbc.Col(dbc.Button("Updates Log", id="updates-button", color="info"), width="auto"),
                    justify="center", className="m-4"
                ),
                
                dcc.Markdown(
                    r"""          
                    
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
                    WebDG is for anyone studying, teaching, or just curious about [differential geometry](https://www.britannica.com/science/differential-geometry). It is an open-source web app robust enough to explore interactive 3D visualizations and analyses of abstract curves and surfaces without the substantial overhead of learning to script computer algebra systems.
                    
                    **WebDG is free for everyone. No login, download, license, or subscription is required.**
                    
                    I created, maintain, and host this open-source educational tool as a labor of love, freely available to everyone. If you find it useful and would like to support its continued development and hosting, you’re welcome to make a small, optional donation via [Buy Me a Coffee](https://www.buymeacoffee.com/mwhefner). No account is needed, and all major credit cards are accepted. Thank you for helping keep this resource online and accessible!
                    
                    **You can also show your support by simply sharing this app!**
                    
                    ***
                    
                    #### What does it do?
                    
                    """, mathjax=True, className="mb-5"
                ),
                
                dcc.Markdown(
                    r"""    
                    
                    WebDG can be used to study 3 abstract *subjects*: 
                    
                    - **curves**, 
                    - **parametric surfaces**,
                    - and **level surfaces** (a.k.a. "isosurfaces" or "implicit surfaces").
                    
                    Use the Subjects menu to choose and define a subject to study. Curves and parametric surfaces are defined parametrically, and level surfaces are defined implicitly. Once you finish defining and "render" your subject, WebDG will create an interactive visualization of it.
                    
                    ***
                    
                    **Curves** are defined by parametric equations (i.e. $x$, $y$, and $z$ are defined in terms of $t$) and can be colored by speed, curvature, torsion, t coordinate, or x-y-z coordinates. As analytics, WebDG symbolically computes these explicit expressions for curves:
                    
                    - the first, second, and third derivatives;
                    - the Frenet-Serret frame;
                    - the speed;
                    - the curvature;
                    - and the torsion

                    with plots for the latter three.
                    
                    ***
                    
                    **Parametric surfaces** are defined by parametric equations also (i.e. $x$, $y$, and $z$ are defined in terms of $u$, and $v$) and can be colored by u-v coordinates, x-y-z coordinates, scene lighting, surface normal, Gaussian curvature, mean curvature, or principal curvature (k1 or k2). As analytics, WebDG symbolically computes these explicit expressions for parametric surfaces:
                    
                    - the Jacobian (all first-order partial derivatives),
                    - the Hessian(s) (all second-order partial derivatives),
                    - the First Fundamental Form coefficients,
                    - the Second Fundamental Form coefficients,
                    - and the Gaussian, mean, and principal curvatures

                    with plots for the three curvatures.
                    
                    ***
                    
                    **Level surfaces** (a.k.a. "isosurfaces" or "implicit surfaces") can be defined implicitly (i.e. defined by a function $f$ assuming $f(x,y,z)=0$). They can be colored by scene lighting or surface normal. Analytics are not currently available for level surfaces.
                    
                    ***
                    
                    *Tip: In WebDG, as in computer graphics, the $y$-axis points up in space. This is different from the $z$-up representation traditionally encountered in math contexts.*
                    
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
        
    # help popover
    dbc.Popover(
        dbc.PopoverBody(html.Em("expand info modal about WebDG")),
        target="help-button",
        trigger="hover",
        placement="right"
    ),
    
    # "WebDG is ready" alert
    dbc.Alert(
        [
            "Change the visualization by rendering a subject to study using the Subjects (", 
            html.I(className="fa-solid fa-subscript"), 
            ") menu above. You can close info alerts (like this) with the X to the right."
        ], 
        color="info", 
        dismissable=True, 
        is_open=True, 
        className = "m-3", 
        id="refresh_alert", 
        style = { 'user-select': 'none','textAlign' : 'center'}
    ),
    
    # A "please wait" during rendering
    dbc.Alert(
        [
            html.Div(
                dbc.Spinner(color="warning", size="md"),
                className="d-flex justify-content-center mb-2", 
                style = {'textAlign' : 'center', 'user-select': 'none', "fontSize": "2em"}
            ),
            html.P("Please wait while WebDG is processing your subject", 
                id="inner_loading_alert", 
                style = {'textAlign' : 'center', 'user-select': 'none', "fontSize": "1.5em"}
            )
        ],
        id="rendering_alert",
        color="warning",
        dismissable=False,
        is_open=True,
        className="m-3",
        style={'display': 'none', 'user-select': 'none'}
    ),


    # The following have their style 'display' toggled
    # in javascript by the rendering pipeline

    # Render success alert
    dbc.Alert(
        [
            
            html.P(
                [
                
                html.P('Success! WebDG has rendered your subject. ', style={'textAlign' : 'center',"fontSize": "1.5em"}),
                
                'Orbit your view around the focal point by left-clicking and dragging. Move the focal point with the arrow keys, and hold shift while pressing the up or down arrow to move it forward or backward. Zoom using the mouse wheel. Explore more adjustments in the Settings menu with the ',
                
                html.I(className="fa-solid fa-gear"),
                
                ' icon on the top right.'           
                
                ],
                    
                style={'textAlign' : 'center'}
            )
            
        ],
        color="success",
        dismissable=True,
        id="success_alert",
        is_open=True,
        className="m-3",
        style={'display': 'none', 'user-select': 'none'}  # Disable text selection
    ),

    # Render failure alert
    dbc.Alert(
        [
            html.P("Sorry, WebDG failed to render your subject", 
                style={'textAlign' : 'center', "fontSize": "1.5em"}
            ),
            html.P("Unspecified error.", 
                id="failure_alert_inner",
                style={'textAlign' : 'center'}
            )
        ], 
        id = "failure_alert", 
        color="danger", 
        dismissable=False, 
        is_open=True, 
        className = "m-3", 
        style = { 'display': 'none'}
    ),
        
    ],
    
    style={
        "display": "flex",
        "flexDirection": "column",
        "height": "100vh"  # Makes the whole app take up the full viewport height
    }
)

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
    ClientsideFunction(
        namespace="differential_geometry", 
        function_name="refresh"),
    Output("refresh_dummy_target", "data"),
    Input("re_start_engine", "n_clicks")
)

# This callback will run the 'killswitch_engage' function when the URL changes
clientside_callback(
    ClientsideFunction(
        namespace="differential_geometry", 
        function_name="killswitch_engage"), # there is loveeeee
    Output("killswitch_dummy_target", "data"),
    Input("webdg_url", "pathname")  # Trigger when the URL changes
)

# The following callbacks operate the modals

## Subject modal open/close
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

## Analytics modal open/close
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

## Settings modal open/close
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

## Help modal open/close
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

## Updates modal open/close
clientside_callback(
    """
    function(n_clicks, n_2, is_open) {
        return !is_open;
    }
    """,
    Output("updates-modal", "is_open"),
    [Input("updates-button", "n_clicks"), Input("close-updates-modal", "n_clicks")],
    State("updates-modal", "is_open"),
    prevent_initial_call=True,
)

# Halt orbit control when a modal is open
clientside_callback(
    """
    function(subject, analytics, settings, theme, portfolio, help, updates) {
        let dg = window.dash_clientside.differential_geometry;
        let allClosed = !subject && !analytics && !settings && !theme && !portfolio && !help && !updates;
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
    Input("updates-modal", "is_open"),
)
