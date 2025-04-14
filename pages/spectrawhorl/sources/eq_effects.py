"""

eq_effects.py

This script builds the spectrawhorl app's equalizer.

M W Hefner, 2025
MIT License

"""

from dash import html, dcc
import dash_bootstrap_components as dbc

controlSetName = 'EQUALIZER'

layout = html.Div(
    
    children = [
        
        html.H4("EQ", className = "spectrawhorl-label mb-4"),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Bass', className = "spectrawhorl-label mb-5"),
        
        dcc.Slider(
            id='bassGainSlider',
            min=-47,
            max=47,
            step=0.05,
            value=0,
            marks={
                -47: {'label' : 'Min', 'style' : {'fontWeight' : 'bold', 'fontSize' : '18px'}},
                
                0 : {'label':"Pass Through"},

                47: {'label' : 'Max', 'style' : {'fontWeight' : 'bold', 'fontSize' : '18px'}},
            },
            included=False,
            updatemode='drag', 
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Middle', className = "spectrawhorl-label mb-5"),
        
        dcc.Slider(
            id='middleGainSlider',
            min=-47,
            max=47,
            step=0.05,
            value=0,
            marks={
                -47: {'label' : 'Min', 'style' : {'fontWeight' : 'bold', 'fontSize' : '18px'}},
                
                0 : {'label':"Pass Through"},

                47: {'label' : 'Max', 'style' : {'fontWeight' : 'bold', 'fontSize' : '18px'}},
            },
            included=False,
            updatemode='drag', 
            className = "spectrawhorl-slider w-75 mb-5 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Treble', className = "spectrawhorl-label mb-5"),
        
        dcc.Slider(
            id='trebleGainSlider',
            min=-47,
            max=47,
            step=0.1,
            value=0,
            marks={
                -47: {'label' : 'Min', 'style' : {'fontWeight' : 'bold', 'fontSize' : '18px'}},
                
                0 : {'label':"Pass Through"},

                47: {'label' : 'Max', 'style' : {'fontWeight' : 'bold', 'fontSize' : '18px'}},
            },
            included=False,
            updatemode='drag', 
            className = "spectrawhorl-slider mb-3 w-75 mx-auto"
        ),
        
    ],


    id=controlSetName + "Controls",

)