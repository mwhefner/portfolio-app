"""

input_source.py

This script builds the spectrawhorl app's input source menu tab.

M W Hefner, 2025
MIT License

"""

from dash import html, dcc, clientside_callback, Output, Input
import dash_bootstrap_components as dbc
import pages.spectrawhorl.sources.generator as genr
import pages.spectrawhorl.sources.eq_effects as eqfx
import pages.spectrawhorl.sources.player as play

controlSetName = 'inputSource'

layout = html.Div(
    
    children = [
        
        dcc.Markdown("***"),
        
        dbc.Label("Source", className = "spectrawhorl-label mb-5"),

        dbc.RadioItems(
            options=[
                {'label': 'Sample Music', 'value': 'SAMPLE'},
                {'label': 'Microphone In', 'value': 'MICROPHONE'},
                {'label': 'File Upload', 'value': 'UPLOAD'},
                {'label': 'SpectraWhorl Generator', 'value': 'GENERATOR'},
            ],
            id="spectrawhorl-inputSource",
            className = "spectrawhorl-check mb-5 w-75 mx-auto",
            value='SAMPLE',
            inline=False,  # optional: makes them display horizontally
            labelClassName="spectrawhorl-inner-label",  # optional: margin between items
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        html.Div(
            
            children = play.layout,
            
            id = "spectrawhorl-playerLayout"
            
            ),
        
        html.Div(
            
            children = genr.layout,
            
            id = "spectrawhorl-generatorLayout"
            
            ),
        
        html.Div(
            
            children = eqfx.layout,
            
            id = "spectrawhorl-eqfxLayout"
            
            ),
        
    ],


    id=controlSetName + "Controls",

)

# callback for changing the input source layout
clientside_callback(
    """
    function(inputSourceValue, generatorSourceValue) {
        const show = {'display' : 'block'};
        const hide = {'display' : 'none'};
        
        if (inputSourceValue == "SAMPLE") {
            
            return [show, hide, show, hide, show];
            
        } else if (inputSourceValue == "MICROPHONE") {
            
            return [hide, hide, hide, hide, show];
            
        } else if (inputSourceValue == "UPLOAD") {
            
            return [hide, show, show, hide, show];
            
        } else if (inputSourceValue == "GENERATOR") {
            
            if (generatorSourceValue != "midi") {
                return [hide, hide, hide, show, show];
            } else {
                return [hide, hide, hide, show, hide];
            }
            
        } else {
            return [show, show, show, show, show];
        }
        
    }
    """,

    # OUTPUTS------------------------------------------------
    [    
        Output('spectrawhorl-sampleMusicLayout', 'style'),
        Output('spectrawhorl-uploadLayout', 'style'),
        Output('spectrawhorl-playerLayout', 'style'),
        Output('spectrawhorl-generatorLayout', 'style'),
        Output('spectrawhorl-eqfxLayout', 'style')
    ],

    # INPUTS--------------------------------------------------
    [
        Input('spectrawhorl-inputSource', 'value'),
        Input('spectrawhorl-generatorSource', 'value')
    ]

)