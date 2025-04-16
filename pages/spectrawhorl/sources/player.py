"""

player.py

This script builds the spectrawhorl app's media player.

M W Hefner, 2025
MIT License

"""

from dash import html, dcc, clientside_callback, Output, Input, State
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
                        dbc.Col(html.I(className="fa-solid fa-play", id="spectrawhorl-playPauseButton-icon"), width="auto", className="text-end"),
                        dbc.Col(html.Span("Play", id="spectrawhorl-inner-playPauseButton", className="fw-bold"), width="auto"),
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
                        dbc.Col(html.Span("Stop", className="fw-bold"), width="auto"),
                        ], 
                        align="center"
                    ),
                    id="spectrawhorl-stopButton",
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

# Sample selection spectrawhorl-sampleMusicLayout
clientside_callback(
    """
    function(value) {
        
        if (window.spectrawhorl_namespace.unloaded) {
            return window.dash_clientside.no_update;
        }
        
        //console.log("Input source is SAMPLE and sample music changed:");
        window.spectrawhorl_namespace.sampleMusic = value;
        //console.log(window.spectrawhorl_namespace.sampleMusic);
        
        if (window.spectrawhorl_namespace.sampleMusic === "SCHUBERT") {
            window.spectrawhorl_namespace.switchToSoundFile(1);
        } else if (window.spectrawhorl_namespace.sampleMusic === "BACH") {
            window.spectrawhorl_namespace.switchToSoundFile(2);
        } else {
            window.spectrawhorl_namespace.switchToSoundFile(0);
        }
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('spectrawhorl-sampleMusic', 'value'),
    Input('spectrawhorl-sampleMusic', 'value')
)

# callback for the media player
clientside_callback(
    """
    function(_n1, _n2, _, __, current) {
        
        if (window.spectrawhorl_namespace.unloaded) {
            return window.dash_clientside.no_update;
        }

        let triggered = dash_clientside.callback_context.triggered;
        
        //console.log(current);
        
        if (triggered.length > 0 && triggered[0].prop_id === 'spectrawhorl-playPauseButton.n_clicks') {
            
            if (current.startsWith('Play')) {
                // Play
                if (window.spectrawhorl_namespace.currentSource === "soundfile") {
                    //console.log("Detected request to PLAY player.");
                    window.spectrawhorl_namespace.soundFile.loop();
                    window.spectrawhorl_namespace.soundFile.rate(window.spectrawhorl_namespace.playRate);
                }
                return ['Pause', "fa-solid fa-pause"];
            } else {
                // Pause
                if (window.spectrawhorl_namespace.currentSource === "soundfile") {
                    //console.log("Detected request to PAUSE player.");
                    window.spectrawhorl_namespace.soundFile.pause();
                }
                return ['Play', "fa-solid fa-play"];
            }
        }
        // Stop
        //console.log("Detected request to STOP player.");
        if (window.spectrawhorl_namespace.currentSource === "soundfile") {
            window.spectrawhorl_namespace.stopAllSources();
        }
        return ['Play', "fa-solid fa-play"];
    }
    
    """,
    [
        Output('spectrawhorl-inner-playPauseButton', 'children'),
        Output('spectrawhorl-playPauseButton-icon', 'className')
    ],
    [
        Input('spectrawhorl-playPauseButton', 'n_clicks'),
        Input('spectrawhorl-stopButton', 'n_clicks'),
        Input('spectrawhorl-inputSource', 'value'),
        Input('spectrawhorl-sampleMusic', 'value'),
    ],
    [State('spectrawhorl-inner-playPauseButton', 'children')]
)

# play rate slider playRateSlider
clientside_callback(
    """
    function(value) {
	
        if (window.spectrawhorl_namespace.unloaded) {
            return window.dash_clientside.no_update;
        }
		
        window.spectrawhorl_namespace.playRate = value;
        
        if (window.spectrawhorl_namespace.currentSource === "soundfile") {
            window.spectrawhorl_namespace.soundFile.rate(value);
        }
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('playRateSlider', 'value'),
    Input('playRateSlider', 'value')
)

# Clientside callback to read the file content
clientside_callback(
    """
    function(contents, filename) {
        if (contents) {

            window.spectrawhorl_namespace.previousUploadFileContentData = window.spectrawhorl_namespace.uploadFileContentData;
            
            window.spectrawhorl_namespace.uploadFileContentData = contents;
            window.spectrawhorl_namespace.uploadFileName = filename;

            window.spectrawhorl_namespace.addSoundFile()
                .then(() => {
                    window.spectrawhorl_namespace.checkAndSwitchToUploadedFile();
                })
                .catch(() => {
                    //console.log("Failed to upload the file.");
                    document.getElementById("spectrawhorl-uploadIndicator").innerText = "Upload failed.";
                });
            
            return "Now processing: " + '"' + filename + '"';
        }
        return 'Upload a file above.';
    }
    """,
    Output('spectrawhorl-uploadIndicator', 'children'),
    Input('spectrawhorl-uploadBox', 'contents'),
    Input('spectrawhorl-uploadBox', 'filename'),
)
