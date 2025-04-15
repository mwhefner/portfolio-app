"""

overlays.py

This script builds the spectrawhorl app's overlay menu tab.

M W Hefner, 2025
MIT License

"""

from dash import register_page, html, dcc, clientside_callback, Input, Output, State, ClientsideFunction
import dash_bootstrap_components as dbc

controlSetName = 'OVERLAY'

layout = html.Div(
    
    children = [
        
            dcc.Markdown("***"),
            
            dbc.Label('Notes to Show', className = "spectrawhorl-label mb-5"),
            
            dbc.RadioItems(
                options=[
                    {'label': 'Hide Note Overlay', 'value': 'NONE'},
                    {'label': 'Tonality Menu: Triad', 'value': 'TRIAD'},
                    {'label': 'Tonality Menu: Key', 'value': 'KEY'},
                    {'label': 'All (Chromatic)', 'value': 'ALL'},
                ],
                id="noteOverlayType",
                value='ALL',
                className = "spectrawhorl-check mb-3 w-75 mx-auto",
                inline=False,  # stack vertically; set to True if you prefer inline
                labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
            ),
            
            dbc.Label("Color",className="spectrawhorl-label mb-3"),
            
            dbc.Input(
                type="color",
                id="noteOverlay_colorpicker",
                value="#ffffff",
                className="p-0 mb-5 w-75 mx-auto",
                style={"width": "100%", "height": 100, 'user-select': 'none', "fontSize": "1.5em",}
            ),
            
#            dbc.Label('CHORD FACTORS', className = "spectrawhorl-label mb-5"),
#            
#            dcc.RadioItems(
#                options=[
#                    {'label': 'NONE', 'value': 'NONE'},
#                    {'label': 'TRIAD', 'value': 'TRIAD'},
#                    {'label': 'KEY', 'value': 'KEY'},
#                    {'label': 'ALL', 'value': 'ALL'},
#                ],
#                id="chordFactors",
#                value='NONE',
#                inputStyle={'marginRight': '10px', 'width' : '30px', 'height' : '30px'},
#                labelStyle={'display': 'flex', 'align-items': 'center'} 
#            ),

            dcc.Markdown("***"),
            
            dbc.Label('Harmonic Series Overlay', className = "spectrawhorl-label mb-5"),
            
            dbc.RadioItems(
                options=[
                    {'label': 'Hide Harmonic Series', 'value': 'NONE'},
                    {'label': 'Show Free Harmonic Series', 'value': 'FREE'},
                    {'label': 'Show Nearest Chromatic Pitch', 'value': 'NOTE'},
                ],
                id="harmonicSeriesOverlayType",
                value='NONE',
                className = "spectrawhorl-check mb-5 w-75 mx-auto",
                inline=False,  # stack vertically; set to True if you prefer inline
                labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
            ),
            
            dbc.Label('Fundamental Frequency', className = "spectrawhorl-label mb-5"),
            
            dcc.Slider(
                id='seriesFundamentalSlider',
                min=24,
                max=108,
                step=0.001,
                value=60,
                marks={
                    24: 'C₁',
                    36: 'C₂',
                    48: 'C₃',
                    60: 'C₄',
                    72: 'C₅',
                    84: 'C₆',
                    96: 'C₇',
                    108: 'C₈',
                    # 120: 'C₁₀',
                },
                included=True,
                updatemode='drag',
                className="spectrawhorl-slider w-75 mb-5 mx-auto"
            ),
            
            dbc.Label("Color",className="spectrawhorl-label mb-3"),
            
            dbc.Input(
                type="color",
                id="harmonicSeriesOverlay_colorpicker",
                value="#ffffff",
                className="p-0 mb-5 w-75 mx-auto",
                style={"width": "100%", "height": 100, 'user-select': 'none', "fontSize": "1.5em",}
            ),
            
            #html.P("Read about inharmonicity."), #https://en.wikipedia.org/wiki/Inharmonicity
            
            html.P([
                "Something not lining up? Read about ",
                html.A("inharmonicity!", href="https://en.wikipedia.org/wiki/Inharmonicity", target="_blank", style = {'color' : '#0060DF'})
            ], className = "spectrawhorl-label mb-5", style={'fontSize' : '1em'}),
            
            dcc.Markdown("***"),
            
            dbc.Label('Overlay Appearance', className = "spectrawhorl-label mb-5"),

            dbc.RadioItems(
                options=[
                    {'label': 'Show Behind Spectrogram', 'value': 'BACK'},
                    {'label': 'Show Atop Spectrogram', 'value': 'FRONT'},
                ],
                id="overlayPosition",
                value='BACK',
                className = "spectrawhorl-check mb-5 w-75 mx-auto",
                inline=False,  # stack vertically; set to True if you prefer inline
                labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
            ),
            
            dcc.Markdown("***", className="w-75 mx-auto mb-5"),
            
            dcc.Slider(
                id='overlayStrokeWidthSlider',
                min=1,
                max=30,
                step=1,
                value=5,
                marks={
                    1: 'Thin',
                    
                    30: 'Thick',
                },
                included=True,
                updatemode='drag',
                className="spectrawhorl-slider w-75 mb-5 mx-auto"
            ),
            
            dcc.Slider(
                id='opacitySlider',
                min=0,
                max=256,
                step=1,
                value=64,
                marks={
                    0: 'Transparent',
                    
                    256: 'Opaque',
                },
                included=True,
                updatemode='drag',
                className="spectrawhorl-slider w-75 mb-5 mx-auto"
            ),

        ],

    id=controlSetName + "Controls",

)