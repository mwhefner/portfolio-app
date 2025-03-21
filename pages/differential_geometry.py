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
    description="WebDG is a free Web application for Differential Geometry education. WebDG provides students and instructors a free and accessible technology robust enough to interactively explore abstract differentiable curves and surfaces without the substantial overhead of computer algebra systems.", 
    image="/assets/as_webp/differential_geometry.webp"
)

# Is the following necessary for anything?
'''clientside_callback(
    """
    function(n_clicks) {
        console.log("Button pressed.");
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

    
    dcc.Store(id = "refresh_dummy_target"),

    
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
                        id="close-surface-modal",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ], justify="center", style={"textAlign": "center"}, className = "gap-3")

            ),
        ],
        id="surface-modal",
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
                        "fontSize": "2em",
                    }
                    
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
                    
                    Made for both students and instructors, WebDG is a free and accessible technology robust enough to interactively explore the differential geometry of abstract curves and surfaces without the substantial overhead of learning to script computer algebra systems.
                    
                    **This software is free for anyone to use to learn or teach others about differential geometry. No login, download, licence, or subscription is required.**
                    
                    ***
                    
                    #### Citation
                    
                    As a professional courtesy, I ask to be acknowledged with citation when appropriate (e.g. American Mathematical Society style citation):
                    
                    Hefner, M. W. (2025), *WebDG*, https://mathymattic.pythonanywhere.com/webdg, (accessed Debructober 32, 3025).
                    
                    ***
                    
                    #### Support
                    
                    If you find this app useful and would like for it to stay online and ad-free — or if you would just like to support it and apps like it — [please consider joining me on my patreon.]() You can also help by sharing this app!
                    
                    This application is built with free and open source technology. To read more about the software used, see the [Dash web application framework](), [mathjs](https://mathjs.org), and the [p5.js javascript library](). To suggest features, report a bug, or get more information, please select the "artist home" button at the bottom right.
                    
                    Check out the [video tutorial for WebDG here on youtube]().
                    
                    ***
                    
                    """
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
            'Success! WebDG has rendered your subject. Orbit your view (or that of your "camera") in this space around your focal point by left-click and dragging. Adjust the position of your focal point with your arrow keys. Zoom with your mouse wheel. Explore more subject and lighting adjustments in the Settings menu with the ',
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

# The following callbacks operate the modals for the Subject,
# Analytics, and Settings

## Subject
clientside_callback(
    """
    function(n_1, n_2, is_open) {
        
        return !is_open;
        
    }
    """,
    Output("surface-modal", "is_open"),
    [
        Input("subject", "n_clicks"), 
        Input("close-surface-modal", "n_clicks")
    ],
    State("surface-modal", "is_open"),
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

