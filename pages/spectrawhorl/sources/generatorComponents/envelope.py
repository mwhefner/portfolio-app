"""

envelope.py

This script builds the spectrawhorl app's built-in generator's envelope control set.

M W Hefner, 2025
MIT License

"""

from dash import html, dcc,clientside_callback, Output, Input
import dash_bootstrap_components as dbc

controlSetName = 'ENVELOPE'

layout = html.Div(
    
    children = [
           
        dbc.Label("Sequence Envelope", className = "spectrawhorl-label"),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        # TODO: Show a dynamic envelope here!
        
        dbc.Label('Attack Time', className = "spectrawhorl-label mb-5"),
        
        dcc.Slider(
            id='spectrawhorl-attackSlider',
            min=0.001,
            max=1,
            step=0.001,
            value=0.15,
            marks={
                0.001: '0 sec.',
                
                0.5: '.5 sec.',
                
                1: '1 sec.',
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Decay Time', className = "spectrawhorl-label mb-5"),
        
        dcc.Slider(
            id='spectrawhorl-decaySlider',
            min=0,
            max=1,
            step=0.01,
            value=0.15,
            marks={
                0: '0 sec.',
                
                0.5: '.5 sec.',
                
                1: '1 sec.',
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Sustain Time', className = "spectrawhorl-label mb-5"),
        
        dcc.Slider(
            id='spectrawhorl-sustainTimeSlider',
            min=1,
            max=10,
            step=0.01,
            value=1,
            marks={
                1: '1 sec.',
                
                5: '.5 secs.',
                
                10: '10 secs.',
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Sustain Percentage', className = "spectrawhorl-label mb-5"),
        
        dcc.Slider(
            id='spectrawhorl-sustainSlider',
            min=0,
            max=1,
            step=0.01,
            value=0.15,
            marks={
                0: '0%',
                
                0.5: '50%',
                
                1: '100%',
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Release Time', className = "spectrawhorl-label mb-5"),
        
        dcc.Slider(
            id='spectrawhorl-releaseSlider',
            min=0,
            max=1,
            step=0.01,
            value=0.15,
            marks={
                0: '0 sec.',
                
                0.5: '.5 sec.',
                
                1: '1 sec.',
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***"),
        
    ],


    id=controlSetName + "Controls",

)

# attack
clientside_callback(
    """
    function(value) {
        
        window.spectrawhorl_namespace.attack = value;
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('spectrawhorl-attackSlider', 'value'),
    Input('spectrawhorl-attackSlider', 'value'),
)

# decay
clientside_callback(
    """
    function(value) {
        
        window.spectrawhorl_namespace.decay = value;
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('spectrawhorl-decaySlider', 'value'),
    Input('spectrawhorl-decaySlider', 'value'),
)

# sustainTime
clientside_callback(
    """
    function(value) {
        
        window.spectrawhorl_namespace.sustainTime = value;
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('spectrawhorl-sustainTimeSlider', 'value'),
    Input('spectrawhorl-sustainTimeSlider', 'value'),
)

# sustain (time)
clientside_callback(
    """
    function(value) {
        
        window.spectrawhorl_namespace.sustain = value;
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('spectrawhorl-sustainSlider', 'value'),
    Input('spectrawhorl-sustainSlider', 'value'),
)

# release
clientside_callback(
    """
    function(value) {
        
        window.spectrawhorl_namespace.release = value;
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('spectrawhorl-releaseSlider', 'value'),
    Input('spectrawhorl-releaseSlider', 'value'),
)
