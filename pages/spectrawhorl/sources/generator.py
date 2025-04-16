"""

generator.py

This script builds the spectrawhorl app's built-in generator.

M W Hefner, 2025
MIT License

"""

from dash import html, dcc, clientside_callback, Input, Output
import dash_bootstrap_components as dbc
import pages.spectrawhorl.sources.generatorComponents.freeOscillator as freeOscillator
import pages.spectrawhorl.sources.generatorComponents.sequencer as sequencer
import pages.spectrawhorl.sources.generatorComponents.envelope as envelope

midiMarkdown = """**These midi controls are experimental and still under development.**

_Slider output ranges are mapped from 0-127 in **Data Byte 2** (e.g. Bass Gain slider ranges -47 to +47, so **Data Byte 2** = 0 -> Bass Gain = -47, so **Data Byte 2** = 63 -> Bass Gain = 0, so **Data Byte 2** = 127 -> Bass Gain = +47)._

| Control          | Status Byte | **Data Byte 1** | **Data Byte 2** |
|------------------|-------------|-------------|-------------|
| Key Mode Value   | 0xB0 (176)  | 0x03 (3)    | 0x00-0x7F (0-127) |
| Key Note Value   | 0xB0 (176)  | 0x04 (4)    | 0x00-0x7F (0-127) |
| BPM              | 0xB0 (176)  | 0x05 (5)    | 0x00-0x7F (0-127) |
| NOTES PER BEAT   | 0xB0 (176)  | 0x06 (6)    | 0x00-0x7F (0-127) |
| Triad Degree 1   | 0xB0 (176)  | 0x10 (16)   | 0x00-0x7F (0-127) |
| Triad Degree 2   | 0xB0 (176)  | 0x11 (17)   | 0x00-0x7F (0-127) |
| Triad Degree 3   | 0xB0 (176)  | 0x12 (18)   | 0x00-0x7F (0-127) |
| Triad Degree 4   | 0xB0 (176)  | 0x13 (19)   | 0x00-0x7F (0-127) |
| Triad Degree 7   | 0xB0 (176)  | 0x15 (21)   | 0x00-0x7F (0-127) |
| Triad Degree 6   | 0xB0 (176)  | 0x16 (22)   | 0x00-0x7F (0-127) |
| Triad Degree 5   | 0xB0 (176)  | 0x17 (23)   | 0x00-0x7F (0-127) |
| Play/Pause       | 0xB0 (176)  | 0x14 (20)   | 0x00-0x7F (0-127) |
| Sequence Mode    | 0xB0 (176)  | 0x18 (24)   | 0x00-0x7F (0-127) |
| Sequence Direction | 0xB0 (176) | 0x1C (28)   | 0x00-0x7F (0-127) |
| Attack           | 0xB0 (176)  | 0x46 (70)   | 0x00-0x7F (0-127) |
| Decay            | 0xB0 (176)  | 0x47 (71)   | 0x00-0x7F (0-127) |
| Sustain Time     | 0xB0 (176)  | 0x48 (72)   | 0x00-0x7F (0-127) |
| Release          | 0xB0 (176)  | 0x49 (73)   | 0x00-0x7F (0-127) |
| Sustain          | 0xB0 (176)  | 0x4A (74)   | 0x00-0x7F (0-127) |
| Bass Gain        | 0xB0 (176)  | 0x4B (75)   | 0x00-0x7F (0-127) |
| Middle Gain      | 0xB0 (176)  | 0x4C (76)   | 0x00-0x7F (0-127) |
| Treble Gain      | 0xB0 (176)  | 0x4D (77)   | 0x00-0x7F (0-127) |


"""

layout = [
    html.H1("SpectraWhorl Generator", className="spectrawhorl-label"),
    
    dbc.Alert(
        dcc.Markdown(
            """
            **Warning** 
            
            At high volumes, this generator can cause **damage to hearing and audio equipment** (such as speakers). 
            
            This can occur at frequencies outside your individual range of hearing. 
            
            **Ensure the volume remains as low as possible** while allowing you to still comfortably hear the generator.
            """, 
            style = {'textAlign' : 'center'},
        ),
        color = "warning",
        dismissable = True
    ),
    
    dcc.Markdown("***", className="w-75 mx-auto"),
    
    dbc.Label("Generator Control", id="spectrawhorl-generatorSourceTarget", className = "spectrawhorl-label mb-5"),
    
    # Sample Music Controls
    dbc.RadioItems(
        options=[
            {'label': 'Free Oscillator', 'value': 'free'},
            {'label': 'Arpeggiator', 'value': 'sequence'},
            {'label': 'MIDI Polyphonic', 'value': 'midi'},
        ],
        id="spectrawhorl-generatorSource",
        value='free',
        className = "spectrawhorl-check mb-5 w-75 mx-auto",
        inline=False,  # stack vertically; set to True if you prefer inline
        labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
    ),
    
    dcc.Markdown("***", className="w-75 mx-auto"),
    
    dbc.Label('Oscillator Shape', className = "spectrawhorl-label mb-5"),
    
    # Sample Music Controls
    dbc.RadioItems(
        options=[
            {'label': 'Sine Wave', 'value': 'sine'},
            {'label': "Triangle Wave", 'value': 'triangle'},
            {'label': 'Square Wave', 'value': 'square'},
            {'label': 'Sawtooth Wave', 'value': 'sawtooth'},
        ],
        id="spectrawhorl-oscillatorType",
        value='sine',
        className = "spectrawhorl-check mb-5 w-75 mx-auto",
        inline=False,  # stack vertically; set to True if you prefer inline
        labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
    ),
    
    dcc.Markdown("***", className="w-75 mx-auto"),
    
    html.Div(
        
        children = freeOscillator.layout,
        
        id = "spectrawhorl-freeOscillatorLayout"
        
        ),
    
    html.Div(
        
        children = sequencer.layout,
        
        id = 'spectrawhorl-sequencerLayout'  
    ),
    
    html.Div(
        
        children = envelope.layout,
        
        id = 'spectrawhorl-envelopeLayout'  
    ),
    
    html.Div(
        
        children = [
            html.H5("Attempting to connect to your midi device...",id='spectrawhorl-midiControlIndicator', style={"width":"100%", "textAlign":'center'},className="mb-5"),
            dcc.Markdown(midiMarkdown)
            ],
        
        id = 'spectrawhorl-midiLayout',
        className="mb-5"
    ),
    
    dcc.Markdown("***")

]

# callback for changing the input source layout
clientside_callback(
    """
    function(inputSourceValue) {
        const show = {'display' : 'block'};
        const hide = {'display' : 'none'};
        
        if (inputSourceValue == "free") {
            
            return [show, hide, hide, hide];
            
        } else if (inputSourceValue == "sequence") {
            
            return [hide, show, show, hide];
            
        } else if (inputSourceValue == "midi") {
            
            return [hide, hide, hide, show];
            
        } else {
            return [show, show, show, show];
        }
        
    }
    """,

    # OUTPUTS------------------------------------------------
    [    
        Output('spectrawhorl-freeOscillatorLayout', 'style'),
        Output('spectrawhorl-sequencerLayout', 'style'),
        Output('spectrawhorl-envelopeLayout', 'style'),
        Output('spectrawhorl-midiLayout', 'style'),
    ],

    # INPUTS--------------------------------------------------
    [
        Input('spectrawhorl-generatorSource', 'value')
    ]

)

# generator source
clientside_callback(
    """
    function(value) {
	
        if (window.spectrawhorl_namespace.unloaded) {
            return window.dash_clientside.no_update;
        }
		
        window.spectrawhorl_namespace.generatorSource = value;

        window.spectrawhorl_namespace.stopGenerator();
        window.spectrawhorl_namespace.startGenerator();
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('spectrawhorl-generatorSourceTarget', 'value'),
    Input('spectrawhorl-generatorSource', 'value')
)

# Oscillator Shape
clientside_callback(
    """
    function(value) {
	
        if (window.spectrawhorl_namespace.unloaded) {
            return window.dash_clientside.no_update;
        }
		
        window.spectrawhorl_namespace.oscillatorType = value;

        window.spectrawhorl_namespace.stopGenerator();
        window.spectrawhorl_namespace.initOscillators();
        window.spectrawhorl_namespace.startGenerator();
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('spectrawhorl-oscillatorType', 'value'),
    Input('spectrawhorl-oscillatorType', 'value')
)