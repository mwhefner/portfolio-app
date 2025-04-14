"""

tonality.py

This script builds the spectrawhorl app's tonality menu tab.

M W Hefner, 2025
MIT License

"""

from dash import html, dcc, clientside_callback, Input, Output, State, ClientsideFunction
import dash_bootstrap_components as dbc

controlSetName = 'TONALITY'

layout = [
    
    html.Div(
        
        children = [
        
            dcc.Markdown("***"),
            
            html.Div(
                [
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Root", className="me-2"),
                            dbc.Select(
                                options=[
                                    {'label': 'C', 'value': 0},
                                    {'label': 'C♯ / D♭', 'value': 1},
                                    {'label': 'D', 'value': 2},
                                    {'label': 'D♯ / E♭', 'value': 3},
                                    {'label': 'E', 'value': 4},
                                    {'label': 'F', 'value': 5},
                                    {'label': 'F♯ / G♭', 'value': 6},
                                    {'label': 'G', 'value': 7},
                                    {'label': 'G♯ / A♭', 'value': 8},
                                    {'label': 'A', 'value': 9},
                                    {'label': 'A♯ / B♭', 'value': 10},
                                    {'label': 'B', 'value': 11}
                                ],
                                id="spectrawhorl-keyNote",
                                value=4,
                            ),
                        ],
                        className="me-4 d-flex align-items-center",
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Mode", className="me-2"),
                            dbc.Select(
                                options=[
                                    {'label': 'MAJOR', 'value': -1},
                                    {'label': 'MINOR (as vi.)', 'value': -6},
                                    {'label': 'IONIAN', 'value': 1},
                                    {'label': 'DORIAN', 'value': 2},
                                    {'label': 'PHRYGIAN', 'value': 3},
                                    {'label': 'LYDIAN', 'value': 4},
                                    {'label': 'MIXOLYDIAN', 'value': 5},
                                    {'label': 'AEOLIAN', 'value': 6},
                                    {'label': 'LOCRIAN', 'value': 7},
                                ],
                                id="spectrawhorl-keyMode",
                                value=-1,
                            ),
                        ],
                        className="d-flex align-items-center",
                    ),
                ],
                className="d-flex mb-5",
            ),

            
            dcc.Markdown("***"),

            dbc.Label("TRIAD", id = "midi1", className = "spectrawhorl-label mb-5"),
            
            html.Div(
                children = [
                    html.Div(
                        children = [
                            html.Button(
                                children = [
                                    
                                    # Scale degree name (e.g. "Mediant")
                                    html.I("IV. LOADING TEXT",id = "spectrawhorl-scale_degree_4_title_1"),
                                    
                                    html.Img(id = "spectrawhorl-scale_degree_4_svg", draggable="false"),
                                    
                                    # Title 1: Roman numeral, Tonic Note, Mode (e.g. "iii. E Phyrigian")
                                    html.H4("LOADING TEXT",id = "spectrawhorl-scale_degree_4_title_2"),
                                ],
                                id = "spectrawhorl-scale_degree_4"
                            ),
                            html.Button(
                                children = [
                                    html.I("V. LOADING TEXT",id = "spectrawhorl-scale_degree_5_title_1"),
                                    
                                    html.Img(id = "spectrawhorl-scale_degree_5_svg", draggable="false"),
                                    
                                    html.H4("LOADING TEXT",id = "spectrawhorl-scale_degree_5_title_2"),
                                ],
                                id = "spectrawhorl-scale_degree_5"
                            ),
                        ],
                        id = "spectrawhorl-tc_column_1"
                    ),
                    html.Div(
                        children = [
                            html.Button(
                                children = [
                                    html.I("III. LOADING TEXT",id = "spectrawhorl-scale_degree_3_title_1"),
                                    
                                    html.Img(id = "spectrawhorl-scale_degree_3_svg", draggable="false"),
                                    
                                    html.H4("LOADING TEXT",id = "spectrawhorl-scale_degree_3_title_2"),
                                ],
                                id = "spectrawhorl-scale_degree_3"
                            ),
                            html.Button(
                                children = [
                                    html.I("I. LOADING TEXT",id = "spectrawhorl-scale_degree_1_title_1"),
                                    
                                    html.Img(id = "spectrawhorl-scale_degree_1_svg", draggable="false"),
                                    
                                    html.H4("LOADING TEXT",id = "spectrawhorl-scale_degree_1_title_2"),
                                ],
                                id = "spectrawhorl-scale_degree_1"
                            ),
                            html.Button(
                                children = [
                                    html.I("VI. LOADING TEXT",id = "spectrawhorl-scale_degree_6_title_1"),
                                    
                                    html.Img(id = "spectrawhorl-scale_degree_6_svg", draggable="false"),
                                    
                                    html.H4("LOADING TEXT",id = "spectrawhorl-scale_degree_6_title_2"),
                                ],
                                id = "spectrawhorl-scale_degree_6"
                            ),
                        ],
                        id = "spectrawhorl-tc_column_2"
                    ),
                    html.Div(
                        children = [
                            html.Button(
                                children = [
                                    html.I("II. LOADING TEXT",id = "spectrawhorl-scale_degree_2_title_1"),
                                    
                                    html.Img(id = "spectrawhorl-scale_degree_2_svg", draggable="false"),
                                    
                                    html.H4("LOADING TEXT",id = "spectrawhorl-scale_degree_2_title_2"),
                                ],
                                id = "spectrawhorl-scale_degree_2"
                            ),
                            html.Button(
                                children = [
                                    html.I("VII. LOADING TEXT",id = "spectrawhorl-scale_degree_7_title_1"),
                                    
                                    html.Img(id = "spectrawhorl-scale_degree_7_svg", draggable="false"),
                                    
                                    html.H4("LOADING TEXT",id = "spectrawhorl-scale_degree_7_title_2"),
                                ],
                                id = "spectrawhorl-scale_degree_7"
                            ),
                        ],
                        id = "spectrawhorl-tc_column_3"
                    ),
                ],
                id = "spectrawhorl-tc_base"
            ),
            
            html.P([
                "Not sure where to start? ",
                html.A("Try these songs!", href="https://en.wikipedia.org/wiki/I%E2%80%93V%E2%80%93vi%E2%80%93IV_progression#Songs_using_the_progression", target="_blank", style = {'color' : '#0060DF'})
            ], className = "spectrawhorl-label my-5"),

        ],
        
        id = "spectrawhorl-tonality_layout"

    ),
    
    # Show this instead when spectrawhorl-generatorSource === "midi"
    dbc.Label("These controls are currently controlled by your MIDI device.", id = "midi1", className = "spectrawhorl-label mb-5")
]

clientside_callback(
    """
    function(value) {
        const show = {'display' : 'block'};
        const hide = {'display' : 'none'};
        console.log(value);
        if (value === "midi") {
            return [hide, show];
        } else {
            return [show, hide];
        }
    }
    """,
    [Output("spectrawhorl-tonality_layout", "style"),
    Output("midi1", "style")],
    Input("spectrawhorl-generatorSource", "value")
)

# TODO: Found in the javascript - add back in!!
clientside_callback(
    """
    function(keyNoteValue, keyModeValue, themeValue) {
        return window.spectrawhorl_namespace.updateScaleDegrees(keyNoteValue, keyModeValue, themeValue);
    }
    """,
    [
        Output("spectrawhorl-scale_degree_4_title_1", "children"),
        Output("spectrawhorl-scale_degree_4_svg", "src"),
        Output("spectrawhorl-scale_degree_4_title_2", "children"),

        Output("spectrawhorl-scale_degree_5_title_1", "children"),
        Output("spectrawhorl-scale_degree_5_svg", "src"),
        Output("spectrawhorl-scale_degree_5_title_2", "children"),

        Output("spectrawhorl-scale_degree_3_title_1", "children"),
        Output("spectrawhorl-scale_degree_3_svg", "src"),
        Output("spectrawhorl-scale_degree_3_title_2", "children"),

        Output("spectrawhorl-scale_degree_1_title_1", "children"),
        Output("spectrawhorl-scale_degree_1_svg", "src"),
        Output("spectrawhorl-scale_degree_1_title_2", "children"),
        
        Output("spectrawhorl-scale_degree_6_title_1", "children"),
        Output("spectrawhorl-scale_degree_6_svg", "src"),
        Output("spectrawhorl-scale_degree_6_title_2", "children"),
        
        Output("spectrawhorl-scale_degree_2_title_1", "children"),
        Output("spectrawhorl-scale_degree_2_svg", "src"),
        Output("spectrawhorl-scale_degree_2_title_2", "children"),
        
        Output("spectrawhorl-scale_degree_7_title_1", "children"),
        Output("spectrawhorl-scale_degree_7_svg", "src"),
        Output("spectrawhorl-scale_degree_7_title_2", "children")
    ],
    [
        Input("spectrawhorl-keyNote", "value"),
        Input("spectrawhorl-keyMode", "value"),
        Input("theme-switch", "value")
    ]
)

# TODO: Add back in!!
clientside_callback(
    """
    function(n_clicks_1, n_clicks_2, n_clicks_3, n_clicks_4, n_clicks_5, n_clicks_6, n_clicks_7, themeValue) {
        
        // TODO: add back in!!
        
        //cancelScheduledNotes();
        
        return window.spectrawhorl_namespace.triadButtonSelection(n_clicks_1, n_clicks_2, n_clicks_3, n_clicks_4, n_clicks_5, n_clicks_6, n_clicks_7, themeValue);
    }
    """,
    [
        Output("spectrawhorl-scale_degree_1", "className"),
        
        Output("spectrawhorl-scale_degree_2", "className"),
        
        Output("spectrawhorl-scale_degree_3", "className"),
        
        Output("spectrawhorl-scale_degree_4", "className"),

        Output("spectrawhorl-scale_degree_5", "className"),
        
        Output("spectrawhorl-scale_degree_6", "className"),
        
        Output("spectrawhorl-scale_degree_7", "className"),
    ],
    [
        Input("spectrawhorl-scale_degree_1", "n_clicks"),
        Input("spectrawhorl-scale_degree_2", "n_clicks"),
        Input("spectrawhorl-scale_degree_3", "n_clicks"),
        Input("spectrawhorl-scale_degree_4", "n_clicks"),
        Input("spectrawhorl-scale_degree_5", "n_clicks"),
        Input("spectrawhorl-scale_degree_6", "n_clicks"),
        Input("spectrawhorl-scale_degree_7", "n_clicks"),
        Input("theme-switch", "value"),
    ]
)