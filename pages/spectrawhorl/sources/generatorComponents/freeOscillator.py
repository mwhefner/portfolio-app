"""

freeOscillator.py

This script builds the spectrawhorl app's built-in generator's free oscillator control set.

M W Hefner, 2025
MIT License

"""

from dash import html, dcc, clientside_callback, Output, Input
import dash_bootstrap_components as dbc

controlSetName = 'OSCILLATOR'

layout = html.Div(
    
    children = [

        dbc.Label('Amplitude', className = "spectrawhorl-label mb-5"),
        
        dcc.Slider(
            id='spectrawhorl-amplitudeSlider',
            min=0,
            max=0.5,
            step=0.001,
            value=0,
            marks={
                0: 'Mute',
                
                0.5: 'Full',
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider w-75 mx-auto mb-5"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Frequency', className = "spectrawhorl-label mb-5"),
        
        dcc.Slider(
            id='spectrawhorl-fundamentalSlider',
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
            className = "spectrawhorl-slider w-75 mx-auto  mb-5"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label("Snap Frequency to Nearest", className = "spectrawhorl-label mb-5"),
        
        # SNAP TO Controls
        dbc.RadioItems(
            options=[
                {'label': 'No Snapping', 'value': 'NONE'},
                {'label': 'Chromatic Note', 'value': 'CHROMATIC'},
                {'label': 'Tonality Menu: Key', 'value': 'KEY'},
                {'label': "Tonality Menu: Triad", 'value': 'TRIAD'},
            ],
            id="spectrawhorl-freeSnapTo",
            value='NONE',
            className = "spectrawhorl-check mb-5 w-75 mx-auto",
            inline=False,  # stack vertically; set to True if you prefer inline
            labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
        ),
        
        dcc.Markdown("***"),
        
    ],


    id=controlSetName + "Controls",

)

# Oscillator amp
clientside_callback(
    """
    function(value) {
	
        if (window.spectrawhorl_namespace.unloaded) {
            return window.dash_clientside.no_update;
        }
		
        window.spectrawhorl_namespace.freeOscillatorAmplitude = value;

        window.spectrawhorl_namespace.freeOscillator.amp(window.spectrawhorl_namespace.freeOscillatorAmplitude);
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('spectrawhorl-amplitudeSlider', 'value'),
    Input('spectrawhorl-amplitudeSlider', 'value')
)

# Oscillator fundamental
clientside_callback(
    """
    function(slider, snap) {
	
        if (window.spectrawhorl_namespace.unloaded) {
            return window.dash_clientside.no_update;
        }
		
        window.spectrawhorl_namespace.freeOscillatorFundamental = slider;
        window.spectrawhorl_namespace.snapToState = snap;

        window.spectrawhorl_namespace.freeOscillator.freq(
            window.spectrawhorl_namespace.snapFreqTo(window.spectrawhorl_namespace.noteToFreq(Number(window.spectrawhorl_namespace.freeOscillatorFundamental)))
        );
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('spectrawhorl-fundamentalSlider', 'value'),
    Input('spectrawhorl-fundamentalSlider', 'value'),
    Input("spectrawhorl-freeSnapTo", 'value'),
)