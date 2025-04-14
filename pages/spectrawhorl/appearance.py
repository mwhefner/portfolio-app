"""

appearance.py

This script builds the spectrawhorl app's appearance menu tab.

M W Hefner, 2025
MIT License

"""

from dash import html, dcc, clientside_callback, Output, Input
import dash_bootstrap_components as dbc

# EVERYTHING COLOR PALETTES

# Use this to get the string used in layout_dynamics for the globalStorage callback whenever palettes are changed
"""# Convert the python palette arrays into one string containing 4 javascript
# constant definitions: PALETTES, REVERSED_PALETTES, NOTE_PALETTES, and REVERSED_NOTE_PALETTES
def python_to_js_array(array):
    return json.dumps(array).replace("'", '"')
palettes_for_js = (
    f"const PALETTES = {python_to_js_array(typeAndThemeControlSet.palettes)};\n"
    f"const REVERSED_PALETTES = {python_to_js_array(typeAndThemeControlSet.reversed_palettes)};\n"
    f"const NOTE_PALETTES = {python_to_js_array(typeAndThemeControlSet.note_palettes)};\n"
    f"const REVERSED_NOTE_PALETTES = {python_to_js_array(typeAndThemeControlSet.reversed_note_palettes)};"
)

# Print or use the JavaScript constants string
print(palettes_for_js)
"""

old_palettes = [
    ['#543005','#8c510a','#bf812d','#dfc27d','#f6e8c3','#c7eae5','#80cdc1','#35978f','#01665e','#003c30','#f5f5f5'],
    ['#8e0152','#c51b7d','#de77ae','#f1b6da','#fde0ef','#e6f5d0','#b8e186','#7fbc41','#4d9221','#276419','#f7f7f7'],
    ['#40004b','#762a83','#9970ab','#c2a5cf','#e7d4e8','#d9f0d3','#a6dba0','#5aae61','#1b7837','#00441b','#f7f7f7'],
    ['#7f3b08','#b35806','#e08214','#fdb863','#fee0b6','#d8daeb','#b2abd2','#8073ac','#542788','#2d004b','#f7f7f7'],
    ['#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de','#4393c3','#2166ac','#053061','#f7f7f7'],
    ['#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#e0e0e0','#bababa','#878787','#4d4d4d','#1a1a1a','#ffffff'],
    ['#a50026','#d73027','#f46d43','#fdae61','#fee090','#e0f3f8','#abd9e9','#74add1','#4575b4','#313695','#ffffbf'],
    ['#a50026','#d73027','#f46d43','#fdae61','#fee08b','#d9ef8b','#a6d96a','#66bd63','#1a9850','#006837','#ffffbf'],
    ['#9e0142','#d53e4f','#f46d43','#fdae61','#fee08b','#e6f598','#abdda4','#66c2a5','#3288bd','#5e4fa2','#ffffbf']
]

palettes = [
    ['#f5f5f5','#543005','#8c510a','#bf812d','#dfc27d','#f6e8c3','#c7eae5','#80cdc1','#35978f','#01665e','#003c30'],
    ['#f7f7f7','#8e0152','#c51b7d','#de77ae','#f1b6da','#fde0ef','#e6f5d0','#b8e186','#7fbc41','#4d9221','#276419'],
    ['#f7f7f7','#40004b','#762a83','#9970ab','#c2a5cf','#e7d4e8','#d9f0d3','#a6dba0','#5aae61','#1b7837','#00441b'],
    ['#f7f7f7','#7f3b08','#b35806','#e08214','#fdb863','#fee0b6','#d8daeb','#b2abd2','#8073ac','#542788','#2d004b'],
    ['#f7f7f7','#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de','#4393c3','#2166ac','#053061'],
    ['#ffffff','#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#e0e0e0','#bababa','#878787','#4d4d4d','#1a1a1a'],
    ['#ffffbf','#a50026','#d73027','#f46d43','#fdae61','#fee090','#e0f3f8','#abd9e9','#74add1','#4575b4','#313695'],
    ['#ffffbf','#a50026','#d73027','#f46d43','#fdae61','#fee08b','#d9ef8b','#a6d96a','#66bd63','#1a9850','#006837'],
    ['#ffffbf','#9e0142','#d53e4f','#f46d43','#fdae61','#fee08b','#e6f598','#abdda4','#66c2a5','#3288bd','#5e4fa2']
]

note_palettes = [
    [
        '#1f78b4', # C
        '#a6cee3',
        '#33a02c', # D
        '#b2df8a',
        '#b15928', # E
        '#e31a1c', # F
        '#fb9a99', 
        '#ff7f00', # G
        '#fdbf6f',
        '#6a3d9a', # A
        '#cab2d6',
        '#ffff99'], # B
    ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f']
]

reversed_palettes = [palette[::-1] for palette in old_palettes]

reversed_note_palettes = [
    [
        # Transform to Phrygian so it instead colors the flats
        '#b15928', # E
        '#fb9a99', 
        '#e31a1c', # F
        '#fdbf6f',
        '#ff7f00', # G
        '#ffff99',
        '#cab2d6',
        '#6a3d9a', # A
        '#a6cee3',
        '#1f78b4', # C
        '#b2df8a',
        '#33a02c', # D
        ], # B

    note_palettes[1][::-1]
]

def showPalette(index, reversed=False, type="OCTAVE"):
    if index < 0 or index >= len(palettes):
        raise ValueError("Index out of range")
    
    palette = palettes[index]

    if type == "NOTE" :
        palette = note_palettes[index]

    if reversed:
        palette = reversed_palettes[index]

        if type == "NOTE" :
            palette = reversed_note_palettes[index]

    if type == "OCTAVE" :
        palette = palette[1:]

    squares = [
        html.Div(
            style={
                'background-color': color,
                'margin': '0px',

                'flex-grow': '1',   # Make each square take equal space
                'flex-basis': '0',  # Allow flex items to grow equally
                'min-width': '0',   # Prevent items from shrinking below a certain size

                'box-sizing': 'border-box',  # Include padding in the element's total width and height
                'aspect-ratio': '1 / 1',
            }
        ) for color in palette
    ]

    return html.Div(
        squares,
        style={
            'display': 'flex',
            'align-items': 'center',
            'margin': '0px',
            'width': '100%',  # Ensure the container takes up the full width of the parent
        }
    )

note_mapping = {
    0: 'C', 1: 'C♯ / D♭', 2: 'D', 3: 'D♯ / E♭', 4: 'E', 5: 'F',
    6: 'F♯ / G♭', 7: 'G', 8: 'G♯ / A♭', 9: 'A', 10: 'A♯ / B♭', 11: 'B'
}

controlSetName = 'THEME'

layout = html.Div(
    
    children = [
        
        dcc.Markdown("***"),
        
        dbc.Label('Menu Opacity', className = "spectrawhorl-label mb-5"),

        dcc.Slider(
            id='spectrawhorl-menuTransparency',
            min=0.4,
            max=1,
            step=0.01,
            value=1,
            marks={
                0.4: 'Phantom',
                1: 'Opaque',
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),

        dcc.Markdown("***"),

        dbc.Label("Viewer Background Color",className="spectrawhorl-label mb-3"),
        
        dbc.Input(
            type="color",
            id="bg_colorpicker",
            value="#2e2e2e",
            className="p-0 mb-5 w-75 mx-auto",
            style={"width": "100%", "height": 100, 'user-select': 'none', "fontSize": "1.5em",}
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),

        dbc.Label("Spectragram Shape",className="spectrawhorl-label mb-3"),

        dbc.RadioItems(
            options=[
                {'label': 'Spiral', 'value': 'SPIRAL'},
                {'label': 'Concentric Circles', 'value': 'CIRCLES'},
                {'label': 'Radial from Point', 'value': 'POINT'},
            ],
            id="spectrogramType",
            value='SPIRAL',
            className = "spectrawhorl-check mb-5 w-75 mx-auto",
            inline=False,  # stack vertically; set to True if you prefer inline
            labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),

        dbc.Label("Color Palette",className="spectrawhorl-label mb-3"),

        dbc.RadioItems(
            options=[
                {'label': "Color by Octave", 'value': "OCTAVE"},
                {'label': "Color by Note", 'value': "NOTE"},
            ],
            id="colorBy",
            value="OCTAVE",
            className = "spectrawhorl-check mb-5 w-75 mx-auto",
            inline=False,  # stack vertically; set to True if you prefer inline
            labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
        ),

        dbc.RadioItems(
            persistence=True,
            options=[
                {'label': "Default Order", 'value': "DEFAULT"},
                {'label': "Reverse Order", 'value': "REVERSE"},
            ],
            id="colorPaletteOrder",
            value="DEFAULT",
            className = "spectrawhorl-check mb-5 w-75 mx-auto",
            inline=False,  # stack vertically; set to True if you prefer inline
            labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
        ),

        dbc.Label("Palettes for Octaves",className="spectrawhorl-label mb-5"),

        dbc.RadioItems(
            persistence=True,
            options = [{'label': showPalette(i), 'value': i} for i in range(len(palettes))],

            id="octaveColorPalette",
            value=0,
            className = "spectrawhorl-check mb-5 w-75 mx-auto spectrawhorl-palette",
            inline=False,  # stack vertically; set to True if you prefer inline
            labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
        ),

        dbc.Label("Palettes for Notes",className="spectrawhorl-label mb-5"),

        dbc.RadioItems(
            persistence=True,
            options = [{'label': showPalette(i,type="NOTE"), 'value': i} for i in range(len(note_palettes))],

            id="noteColorPalette",
            value=0,
            className = "spectrawhorl-check mb-5 w-75 mx-auto spectrawhorl-palette",
            inline=False,  # stack vertically; set to True if you prefer inline
            labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),

        dbc.Label("Level Visibility",className="spectrawhorl-label mb-5"),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Checklist(
                        options=[{'label': f"Octave {index + 1}", 'value': index} for index in range(10)],
                        id="octaveLegendSelection",
                        value=[i for i in range(10)],
                        className = "spectrawhorl-check mb-5 w-75 mx-auto spectrawhorl-palette",
                        inline=False,  # stack vertically; set to True if you prefer inline
                        labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
                    ),
                    md=6, # Take up half the width on medium and larger screens
                ),
                dbc.Col(
                    dbc.Checklist(
                        options=[{'label': note_mapping[index], 'value': index} for index in range(12)],
                        id="noteLegendSelection",
                        value=[i for i in range(12)],
                        className = "spectrawhorl-check mb-5 w-75 mx-auto spectrawhorl-palette",
                        inline=False,  # stack vertically; set to True if you prefer inline
                        labelClassName="spectrawhorl-inner-label",  # spacing between stacked items
                    ),
                    md=6, # Take up half the width on medium and larger screens
                ),
            ],
            className="mb-5 w-75 mx-auto", # Add some margin below the row
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),

        dbc.Label('Line Width', className = "spectrawhorl-label mb-5"),

        dcc.Slider(
            id='lineWidthSlider',
            min=1,
            max=30,
            step=1,
            value=10,
            marks={
                1: 'Min',
                30: 'Max'
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Detection Threshold', className = "spectrawhorl-label mb-5"),

        dcc.Slider(
            id='thresholdSlider',
            min=0,
            max=1,
            step=0.01,
            value=0,
            marks={
                0: 'All',
                1: 'None'
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Width Between Octaves', className = "spectrawhorl-label mb-5"),

        dcc.Slider(
            id='octaveWidthSlider',
            min=0,
            max=1,
            step=0.01,
            value=1,
            marks={
                0: 'Min',
                1: 'Max'
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Radial Height', className = "spectrawhorl-label mb-5"),

        dcc.Slider(
            id='octaveHeightSlider',
            min=0.01,
            max=10,
            step=0.01,
            value=5,
            marks={
                0.01: 'Min',
                10: 'Max'
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Peak Balance Transform', className = "spectrawhorl-label mb-5"),

        dcc.Slider(
            id='peakAccentuationSlider',
            min=0,
            max=16,
            step=0.1,
            value=4,
            marks={
                0: 'Min',
                16: 'Max'
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Visual Opacity', className = "spectrawhorl-label mb-5"),

        dcc.Slider(
            id='fadeSlider',
            min=0,
            max=1,
            step=0.01,
            value=0.1,
            marks={
                0: 'Opaque',
                1: 'Transparent'
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('FFT Bin Density', className = "spectrawhorl-label mb-5"),

        dcc.Slider(
            id='binDensitySlider',
            min=8,
            max=14,
            step=1,
            value=13,
            marks={
                8: 'Min',
                14: 'Max'
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),
        
        dcc.Markdown("***", className="w-75 mx-auto"),
        
        dbc.Label('Time-Averaged Smoothing', className = "spectrawhorl-label mb-5"),

        dcc.Slider(
            id='timeSmoothingSlider',
            min=0,
            max=0.9,
            step=0.1,
            value=0,
            marks={
                0: 'NONE',
                0.9: 'Max'
            },
            included=True,
            updatemode='drag',
            className = "spectrawhorl-slider mb-5 w-75 mx-auto"
        ),

    ],

    id=controlSetName + "Controls",
)

clientside_callback(
    """
    function(opacity) {
        console.log(opacity);
        document.documentElement.style.setProperty('--spectrawhorl-menu-opacity', opacity);
        return window.dash_clientside.no_update;
    }
    """,
    Output('spectrawhorl-menuTransparency', 'value'),
    Input('spectrawhorl-menuTransparency', 'value')
)