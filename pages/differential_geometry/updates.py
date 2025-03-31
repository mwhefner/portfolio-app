from dash import html, dcc, Input, Output, State, clientside_callback, register_page, ClientsideFunction
import dash_bootstrap_components as dbc


layout = html.Div(
    [
        dbc.Alert([
            html.I(className="fa-solid fa-highlighter"), 
            html.Strong(" Version 1.0.2"),
            dcc.Markdown("""
                         
                         ***
                         
                         Version 1.0.2 of WebDG has an all-new feature and some asked-for fixes.
                         
                         **WebDG now plots level surfaces (a.k.a. "isosurfaces" or "implicit surfaces")!** In addition to defining surfaces parametrically, you can now also define them implicitly.  Check out this new feature tab in the Subjects menu.
                         
                         The current presets are:
                         
                         - Scherk's (first) surface, 
                         - Scherk's (second) surface, 
                         - Schwarz P-Surface, 
                         - Schwarz D-Surface, and
                         - the Gyroid.
                         
                         If you have a surface to recommend as a preset, let me know!
                         
                         2. I've listened to the fantastic feedback I've received, and I've streamlined the input process. **There is no longer and need to parse inputs;** this is now done automatically with type-responsive feedback.
                         
                         3. This update modal is new to version 1.0.2.
                         
                         **March 29, 2025**
                         
                         """),
            ],  
            color="success", 
            dismissable=False, 
            is_open=True, 
            className = "m-3", 
            id="update_1.0.2", 
            style = { 'user-select': 'none' }),
        
        dbc.Alert([
            html.I(className="fa-solid fa-highlighter"), 
            html.Strong(" Version 1.0.1"),
            dcc.Markdown(r"""
                         
                         ***
                         
                         Today's update brings some minor bug patches and 3 new surface presets: [Dini's surface](https://en.wikipedia.org/wiki/Dini%27s_surface), the [Enneper surface](https://en.wikipedia.org/wiki/Enneper_surface), and the [helicatenoid](https://en.wikipedia.org/wiki/Weierstrass%E2%80%93Enneper_parameterization#Helicatenoid)!
                         
                         **March 26, 2025**
                         
                         """),
            ], 
            color="info", 
            dismissable=False, 
            is_open=True, 
            className = "m-3", 
            id="update_1.0.1", 
            style = { 'user-select': 'none' }),
        
        dbc.Alert([
            html.I(className="fa-solid fa-highlighter"), 
            html.Strong(" Version 1.0.0"),
            dcc.Markdown("""
                         
                         ***
                         
                         WebDG is launched!
                         
                         **March 24, 2025**
                         
                         """),
            ], 
            color="info", 
            dismissable=False, 
            is_open=True, 
            className = "m-3", 
            id="update_1.0.0", 
            style = { 'user-select': 'none' }),
    ]
)