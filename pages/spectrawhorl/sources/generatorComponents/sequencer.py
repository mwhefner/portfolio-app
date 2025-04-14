"""

sequencer.py

This script builds the spectrawhorl app's built-in generator's sequencer control set.

M W Hefner, 2025
MIT License

"""

from dash import html, dcc
import dash_bootstrap_components as dbc

controlSetName = 'SEQUENCE'

layout = html.Div(
    
    children = [
        
        dbc.Row(
            dbc.Col(dbc.Button("Play Sequence", id="playSequenceButton", color="info"), width="auto"),
            justify="center", className="m-5"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Sequence Along', className = "spectrawhorl-label mb-5"),
        
        dbc.RadioItems(
            options=[
                {'label': 'Chromatic Scale', 'value': 'CHROMATIC'},
                {'label': 'Tonality Menu: Key', 'value': 'KEY'},
                {'label': 'Tonality Menu: Triad', 'value': 'TRIAD'},
            ],
            id="sequenceAlong",
            value='CHROMATIC',
            className = "spectrawhorl-check mb-5 w-75 mx-auto",
            inline=False,  # stack vertically; set to True if you prefer inline
            labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Beats Per Minute (BPM)', id = "bpmTitle", className = "spectrawhorl-label mb-5 "),

        dcc.Slider(
            id='bpmSlider',
            min=20,
            max=240,
            step=1,
            value=120,
            marks={
                20: '20',
                
                75: '75',
                
                130: '130',
                
                185: '185',
                
                240: '240',
            },
            tooltip={
                "always_visible": True,
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Notes Per Beat', className = "spectrawhorl-label mb-5 "),

        dcc.Slider(
            id='notesPerBeatSlider',
            min=-2,
            max=3,
            step=None,
            value=0,
            marks={
                -2: '.25 (𝅝)', # whole note
                
                -1: '.5 (𝅗𝅥)', # half note
                
                0: '1 (𝅘𝅥)', # quarter note
                
                1: '2 (𝅘𝅥𝅮)', # eighth notes
                
                2: '4 (𝅘𝅥𝅯)', # sixteenth
                
                3: '8 (𝅘𝅥𝅰)', # 32nd
            },
            included=False,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Sequence Starting Frequency', className = "spectrawhorl-label mb-5 "),

        dcc.Slider(
            id='baseFrequencySlider',
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
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Sequence Pitch Direction', className = "spectrawhorl-label mb-5 "),
        
        dbc.RadioItems(
            options=[
                {'label': "Down in Pitch", 'value': 'DOWN'},
                {'label': 'Up in Pitch', 'value': 'UP'},
            ],
            id="sequenceDirection",
            value='DOWN',
            className = "spectrawhorl-check mb-5 w-75 mx-auto",
            inline=False,  # stack vertically; set to True if you prefer inline
            labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Sequence Length', id = "sequenceLengthTitle", className = "spectrawhorl-label mb-5"),

        dcc.Slider(
            id='sequenceLengthSlider',
            min=1,
            max=60,
            step=1,
            value=12,
            marks={
                1: '1',
                12: '12',
                24: '24',
                36: '36',
                48: '48',
                60: '60',
            },
            tooltip={
                "always_visible": True,
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***"),

    ],


    id=controlSetName + "Controls",

)