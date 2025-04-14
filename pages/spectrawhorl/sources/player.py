"""

player.py

This script builds the spectrawhorl app's media player.

M W Hefner, 2025
MIT License

"""

from dash import html, dcc
import dash_bootstrap_components as dbc

controlSetName = 'PLAYER'

layout = html.Div(
    
    children = [
        
    html.Div(
        
        children = [
            
            dbc.Label("Sample", className = "spectrawhorl-label mb-5"),

            dbc.RadioItems(
                options=[
                    {'label': 'N. Coste (Guitar)', 'value': 'COSTE'},
                    {'label': 'F. Schubert (Piano + Vocals)', 'value': 'SCHUBERT'},
                    {'label': "C.P.E. Bach (Flute)", 'value': 'BACH'},
                ],
                id="spectrawhorl-sampleMusic",
                value='COSTE',
                className = "spectrawhorl-check mb-5 w-75 mx-auto",
                inline=False,  # stack vertically; set to True if you prefer inline
                labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
            )
            
        ],
        
        id = "spectrawhorl-sampleMusicLayout"
        
        ),
    
    html.Div(
        
        children = [
        
            html.Div(
                id="spectrawhorl-uploadBoxContainer",
                children=[
                    dbc.Label("File Upload", className = "spectrawhorl-label mb-3"),
                    dcc.Upload(
                        id='spectrawhorl-uploadBox',
                        children=html.Div(
                                children = [
                                    html.Strong('Drag and drop or select a file.'),
                                    html.P('(.mp3, .ogg, .wav)'),
                                    html.P("Your files stay on your machine."),
                                    ],
                                id="spectrawhorl-uploadBoxInside"
                            ),
                        multiple=False
                    ),
                ],
                className="w-75 mx-auto"
            ),
            
            html.P("Upload a file above.",id='spectrawhorl-uploadIndicator', style={"width" : "100%", "textAlign" : "center", "fontWeight" : "bolder"}, className="mt-5")    
            
        ],
        
        id = "spectrawhorl-uploadLayout", 
        
        className = "mb-5"
        
    ),
    
    dcc.Markdown("***", className="w-75 mx-auto"),
    
    dbc.Label("Media Player", className = "spectrawhorl-label mb-5"),

    html.Div(
        children=[
            dbc.Button(
                    dbc.Row(
                        [
                        dbc.Col(html.I(className="fa-solid fa-play"), width="auto", className="text-end"),
                        dbc.Col(html.Span("PLAY", className="fw-bold"), width="auto"),
                        ], 
                        align="center"
                    ),
                    id="spectrawhorl-playPauseButton",
                    color="primary", 
                    style={'fontSize' : '1.25em'},
                    className="mx-auto"
            ),
            dbc.Button(
                    dbc.Row(
                        [
                        dbc.Col(html.I(className="fa-solid fa-stop"), width="auto", className="text-end"),
                        dbc.Col(html.Span("STOP", className="fw-bold"), width="auto"),
                        ], 
                        align="center"
                    ),
                    id="spectrawhorl-playPauseButton",
                    color="primary", 
                    style={'fontSize' : '1.25em'},
                    className="mx-auto"
            ),
        ],
        id="spectrawhorl-mediaPlayer",
        className="w-75 mx-auto mb-5"
    ),
        
    dbc.Label('Playback Rate', className = "spectrawhorl-label mb-5"),
    
    dcc.Slider(
        id='playRateSlider',
        min=-4,
        max=4,
        step=0.05,
        value=1,
        marks={
            -4: '-4x',
            -3: '-3x',
            -2: '-2x',
            -1: '-1x',
            0: '0x',
            1: {'label' : '1x', 'style' : {'fontWeight' : 'bold'}},
            2: '2x',
            3: '3x',
            4: '4x',
        },
        included=False,
        updatemode='drag', 
        className = "spectrawhorl-slider mb-5 w-75 mx-auto"
    ),
    
    dcc.Markdown("***"),
    
    ],
    id=controlSetName + "Controls"
)