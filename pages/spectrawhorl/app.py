"""

app.py

This script builds the spectrawhorl app's main page.

M W Hefner, 2025
MIT License

"""

from dash import register_page, html, dcc, clientside_callback, Input, Output, State
import dash_bootstrap_components as dbc
from pages.spectrawhorl.input_source import layout as input_source
from pages.spectrawhorl.appearance import layout as appearance
from pages.spectrawhorl.overlays import layout as overlays
from pages.spectrawhorl.tonality import layout as tonality

register_page(
    __name__, 
    path="/spectrawhorl", 
    name="SpectraWhorl", 
    title="SpectraWhorl", 
    description="SpectraWhorl is a free and open-source spectrogram in a whorled pattern. This creates a real-time geometric conceptual lens through which to view and learn about the physics of sound and the math of harmony.", 
    image="/assets/webp/thumbnails/SpectraWhorl.webp"
)

layout = html.Div(
    
    children = [

        # A location object tracks the address bar url
        dcc.Location(id='spectrawhorl_url'),
        
        dcc.Store(id = "spectrawhorl_refresh_dummy_target"),
        dcc.Store(id = "spectrawhorl_theme_dummy_target"),
        
        # Help menu button
        dbc.Stack([
            dbc.Button(
                dbc.Col(html.I(className="fa-solid fa-question fs-2"), align="center"),
                id="spectrawhorl-help-button",
                color="primary",
                style={"borderRadius": "50%", "aspectRatio": "1 / 1"}
            )
        ], className="position-fixed bottom-0 start-0 m-3"),
        
        # help popover
        dbc.Popover(
            dbc.PopoverBody(html.Em("expand the info modal")),
            target="spectrawhorl-help-button",
            trigger="hover",
            placement="right"
        ),
        
        # Help/information/welcome Modal
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Welcome")),
                dbc.ModalBody(
                    [
                        
                    dcc.Markdown("**SpectraWhorl**",
                        style={
                            "textAlign": "center", 
                            "fontSize": "3em",
                        }
                    ),
                    
                    dcc.Markdown(
                        r"""          
                        
                        Version 1.0.0
                        
                        """,
                        style={
                            "textAlign": "center"
                        }
                        
                    ),
                    
                    dbc.Carousel(
                        items=[
                            {"key": "6", "src": "/assets/webp/images/tonetornado_still.webp", "caption" : "The Harmonic Series at C3"},
                        ],
                        controls=False,
                        indicators=False,
                        className="carousel-fade",
                        interval=3000,
                    ),
                    
                    dcc.Markdown(
                        r"""    
                        **SpectraWhorl** is a [**free and open-source**](https://github.com/mwhefner/portfolio-app/blob/main/LICENSE) [**spectrogram**](https://en.wikipedia.org/wiki/Spectrogram) in a [**whorled pattern.**](https://en.wikipedia.org/wiki/Whorl)

                        Like many spectrograms, SpectraWhorl plots pitch (or the frequency **spectrum**) of different sound sources (e.g., your microphone, an uploaded file, etc). What makes SpectraWhorl different is that it does so in a clock-like **whorled** pattern where one 360° rotation represents rising (counter-clockwise) or falling (clockwise) an octave.  This creates a real-time geometric conceptual lens through which to view and learn about the physics of sound and the math of harmony.
                        
                        Use the menu to customize overlays and the spectragram's source, audio processing parameters, and appearance.
                        
                        **SpectraWhorl is free for everyone. No login, download, license, or subscription is required.**
                    
                        I created, maintain, and host this open-source educational tool as a labor of love, freely available to everyone. If you find it useful and would like to support its continued development and hosting, you’re welcome to make a small, optional donation via [Buy Me a Coffee](https://www.buymeacoffee.com/mwhefner). No account is needed, and all major credit cards are accepted. Thank you for helping keep this resource online and accessible!
                        
                        **You can also show your support by simply sharing this app!**
                        
                        """, mathjax=True, className="m-5", style = {'textAlign' : 'center', 'fontSize' : '1.25em'}
                    ),
                    
                    ]
                ),
                dbc.ModalFooter(

                    dbc.Row([
                        dbc.Button(
                            "Close Info Modal",
                            id="close-spectrawhorl-help-modal",
                            className="ms-auto",
                            n_clicks=0,
                        )
                    ], justify="center", style={"textAlign": "center"}, className = "gap-3")

                ),
            ],
            id="spectrawhorl-help-modal",
            centered=True,
            is_open = True,
            size="lg"
        ),
        
        # Viewer
        html.Div(
            id = "spectrawhorl_viewer"
        ),

        # Floating button using Affix-like positioning MENU BUTTON
        dbc.Stack(
            [
                dbc.Button(
                    dbc.Row(
                        [
                        dbc.Col(html.I(className="fa-solid fa-bars"), width="auto", className="text-end"),
                        dbc.Col(html.Span("Menu", className="fw-bold"), width="auto"),
                        ], 
                        className="d-flex justify-content-between align-items-center",
                        align="center"
                    ),
                    id="spectrawhorl-menu",
                    color="primary"
                )
            ], 
            gap=3, 
            className = "position-fixed top-0 start-0 m-3 justify-content-end"
        ),
        
        # Floating button using Affix-like positioning VOUME CONTROLS
        
        dbc.Stack(
            dbc.Alert(
            [
                # Decide which volume container to show based on
                # input source via none/block style toggle in
                # clientside callback
                
                # regular volume slider container
                html.Div(

                    children = [
                        
                        dbc.Label('Volume', style={'textAlign':'center', 'width' : '250px', 'fontSize' : '1.25em'}, className = "spectrawhorl-label mb-2"),
                        
                        dcc.Slider(
                            id='spectrawhorlVolumeSlider',
                            min=0,
                            max=1,
                            step=0.01,
                            value=0.5,
                            marks={
                                0: {'label' : 'Mute', 'style' : {'fontWeight' : 'bold', 'color' : 'red'}},
                            
                                1: {'label' : 'Full', 'style' : {'fontWeight' : 'bold'}},
                            },
                            included=True,
                            updatemode='drag',
                            className = 'spectrawhorl-slider'
                        ),
                        
                        ],
                    
                    id = "spectrawhorl-volumeLayout"
                    
                    ),
                
                # mic monitor volume slider container
                html.Div(
                    
                    children = [
                        
                        dbc.Label('Monitor Volume', style={'textAlign':'center', 'width' : '250px', 'fontSize' : '1.25em'}, className = "spectrawhorl-label mb-2"),
                        
                        dcc.Slider(
                            id='spectrawhorl-micMonitorVolumeSlider',
                            min=0,
                            max=1,
                            step=0.01,
                            value=0,
                            marks={
                                0: {'label' : 'Mute', 'style' : {'fontWeight' : 'bold', 'color' : 'red'}},
                            
                                1: {'label' : 'Full', 'style' : {'fontWeight' : 'bold'}},
                            },
                            included=True,
                            updatemode='drag',
                            className = 'spectrawhorl-slider'
                        ),
                        
                        ],
                    
                    id = "spectrawhorl-micMonitorVolumeLayout"
                    
                    ),
            ], color="dark", className = "p-3 pb-4 pt-2"), 
            gap=3, 
            className = "position-fixed top-0 end-0 m-3 justify-content-end"
        ),
        
        # Menu Modal
        dbc.Modal(
            [

                dbc.ModalHeader(dbc.ModalTitle("Menu")),
                
                dbc.ModalBody(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                dbc.Tabs(
                                    [
                                        dbc.Tab(label="Sound Source", tab_id="Input Source", tabClassName="mx-auto"),
                                        dbc.Tab(label="Appearance", tab_id="Appearance", tabClassName="mx-auto"),
                                        dbc.Tab(label="Visual Overlays", tab_id="Overlays", tabClassName="mx-auto"),
                                        dbc.Tab(label="Tonality", tab_id="Tonality", tabClassName="mx-auto"),

                                    ],
                                    id="spectrawhorl-menu-tabs",
                                    active_tab="Input Source", 
                                    style = {'fontSize' : '1.25em'}
                                )
                            ),
                            dbc.CardBody(
                                html.Div(
                                    id="spectrawhorl-menu-content", className="card-text", 
                                    children = [
                                        html.Div(input_source, id="spectrawhorl-input-source-container", style={"display": "block"}),
                                        html.Div(appearance, id="spectrawhorl-appearance-container", style={"display": "block"}),
                                        html.Div(overlays, id="spectrawhorl-overlays-container", style={"display": "block"}),
                                        html.Div(tonality, id="spectrawhorl-tonality-container", style={"display": "block"}),

                                    ]
                                )
                            ),
                        ],
                        className="px-0"
                    ),
                    id="spectrawhorl-menu-body"
                ),
                dbc.ModalFooter(

                    dbc.Row([
                        dbc.Button(
                            "Close",
                            id="close-spectrawhorl-menu-modal",
                            className="ms-auto",
                            n_clicks=0,
                        )
                    ], justify="center", style={"textAlign": "center"}, className = "gap-3")

                ),
            ],
            id="spectrawhorl-menu-modal",
            centered=True,
            size="lg"
        ),
    ]
)

# This callback creates, refreshes, or kills (when exiting) the sketch
clientside_callback(
    """
    function (path) {

        if (window.spectrawhorl_namespace.spectrawhorl_sketch) {
            // This properly disposes of the old instance
            window.spectrawhorl_namespace.sketch.remove();
        }
        
        if (path === "/spectrawhorl") {
            // Create a fresh sketch
            window.spectrawhorl_namespace.sketch = new p5(window.spectrawhorl_namespace.build_sketch);   
        }
        
        if (window.spectrawhorl_namespace.sketch && path !== "/spectrawhorl") {
            // Get rid of the instance if you leave the page
            window.spectrawhorl_namespace.sketch.remove();
        }
        
        return "";
    
    }    
    """,
    Output("spectrawhorl_refresh_dummy_target", "data"),
    Input("spectrawhorl_url", "pathname")
)

## Help modal open/close
clientside_callback(
    """
    function(n_clicks, n_2, is_open) {
        return !is_open;
    }
    """,
    Output("spectrawhorl-help-modal", "is_open"),
    [Input("spectrawhorl-help-button", "n_clicks"), Input("close-spectrawhorl-help-modal", "n_clicks")],
    State("spectrawhorl-help-modal", "is_open"),
    prevent_initial_call=True,
)

## spectrawhorl-menu modal open/close
clientside_callback(
    """
    function(n_clicks, n_2, is_open) {
        return !is_open;
    }
    """,
    Output("spectrawhorl-menu-modal", "is_open"),
    [Input("spectrawhorl-menu", "n_clicks"), Input("close-spectrawhorl-menu-modal", "n_clicks")],
    State("spectrawhorl-menu-modal", "is_open"),
    prevent_initial_call=True,
)

clientside_callback(
    """
    function(active_tab) {
        let hide = {"display": "none"};
        let show = {"display": "block"};

        let inputSourceStyle = hide;
        let appearanceStyle = hide;
        let overlaysStyle = hide;
        let tonalityStyle = hide;

        if (active_tab === "Input Source") {
            inputSourceStyle = show;
        } else if (active_tab === "Appearance") {
            appearanceStyle = show;
        } else if (active_tab === "Overlays") {
            overlaysStyle = show;
        } else if (active_tab === "Tonality") {
            tonalityStyle = show;
        }

        return [inputSourceStyle, appearanceStyle, overlaysStyle, tonalityStyle];
    }
    """,
    [Output("spectrawhorl-input-source-container", "style"),
    Output("spectrawhorl-appearance-container", "style"),
    Output("spectrawhorl-overlays-container", "style"),
    Output("spectrawhorl-tonality-container", "style"),],
    Input("spectrawhorl-menu-tabs", "active_tab"),
)

# volume
clientside_callback(
    """
    function(v_value, m_value, inputSource) {
	
        if (window.spectrawhorl_namespace.unloaded) {
            return window.dash_clientside.no_update;
        }
             
        if (inputSource === "MICROPHONE") {
            window.spectrawhorl_namespace.volume = m_value;
        } else {
            window.spectrawhorl_namespace.volume = v_value;
        }
        
        window.spectrawhorl_namespace.sketch.outputVolume(window.spectrawhorl_namespace.volume);
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('spectrawhorlVolumeSlider', 'value'),
    Input('spectrawhorlVolumeSlider', 'value'),
    Input('spectrawhorl-micMonitorVolumeSlider', 'value'),
    Input('spectrawhorl-inputSource', 'value'),
)

# peakAccentuationSlider
clientside_callback(
    """
    function(value) {

        window.spectrawhorl_namespace.uiLightTheme = value;

        return window.dash_clientside.no_update;
    }
    """,
    Output('spectrawhorl_theme_dummy_target', 'data'),
    Input('theme-switch', 'value')
)
