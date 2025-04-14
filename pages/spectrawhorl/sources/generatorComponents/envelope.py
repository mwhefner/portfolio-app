"""

envelope.py

This script builds the spectrawhorl app's built-in generator's envelope control set.

M W Hefner, 2025
MIT License

"""

from dash import html, dcc
import dash_bootstrap_components as dbc

controlSetName = 'ENVELOPE'

layout = html.Div(
    
    children = [
           
        dbc.Label("Sequence Envelope", className = "spectrawhorl-label"),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        # TODO: Show a dynamic envelope here!
        
        dbc.Label('Attack Time', className = "spectrawhorl-label mb-5"),
        
        dcc.Slider(
            id='attackSlider',
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
            id='decaySlider',
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
            id='sustainTimeSlider',
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
        
        dbc.Label('Sustain Percentage', className = "spectrawhorl-label mb-5"),
        
        dcc.Slider(
            id='sustainSlider',
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
            id='releaseSlider',
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