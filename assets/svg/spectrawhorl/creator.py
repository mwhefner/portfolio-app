import math

# Define the circle properties
cx, cy, radius = 52, 52, 50

# Define the modes and their intervals in terms of steps from the root
MODES = {
    "IONIAN": [0, 2, 4, 5, 7, 9, 11],     # Major scale
    "DORIAN": [0, 2, 3, 5, 7, 9, 10],     # Minor with a raised 6th
    "PHRYGIAN": [0, 1, 3, 5, 7, 8, 10],   # Minor with a flat 2nd
    "LYDIAN": [0, 2, 4, 6, 7, 9, 11],     # Major with a raised 4th
    "MIXOLYDIAN": [0, 2, 4, 5, 7, 9, 10], # Major with a flat 7th
    "AEOLIAN": [0, 2, 3, 5, 7, 8, 10],    # Natural minor
    "LOCRIAN": [0, 1, 3, 5, 6, 8, 10],    # Minor with flat 2nd and 5th
}

# Function to calculate coordinates
def calculate_coordinates(cx, cy, radius, angle):
    x = cx + radius * math.cos(angle)
    y = cy - radius * math.sin(angle)  # SVG y-axis is downwards
    return x, y

# Function to create SVG content
def create_svg(cx, cy, radius, angles, colors, styles, widths, gColor, mode_intervals, root_angle):
    svg_header = '<!-- Copyright 2024. All rights reserved.  DO NOT DUPLICATE OR REDISTRIBUTE. -->\n<svg width="104" height="104" xmlns="http://www.w3.org/2000/svg">\n'
    svg_footer = '</svg>'
    
    # Draw the notches for notes in the key
    notes_in_key = ""
    for interval in mode_intervals:
        angle = (interval * math.pi / 6) + root_angle
        x, y = calculate_coordinates(cx, cy, radius, angle)
        notes_in_key += f'  <circle cx="{x}" cy="{y}" r="3" fill="{gColor}" />\n'

    # Draw the lines for the chord
    line_elements = ""
    for angle, color, style, width in zip(angles, colors, styles, widths):
        x, y = calculate_coordinates(cx, cy, radius, angle)
        line_elements += f'  <line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{color}" stroke-width="{width}" {style} />\n'

    svg_content = svg_header + notes_in_key + line_elements + svg_footer
    return svg_content

# Function to save SVG content to a file
def save_svg(filename, svg_content):
    with open(filename, 'w') as file:
        file.write(svg_content)

# Function to get note and octave from MIDI note
def get_note_and_octave(midi_note):
    notes = ["C", "C#(Db)", "D", "D#(Eb)", "E", "F", "F#(Gb)", "G", "G#(Ab)", "A", "A#(Bb)", "B"]
    note = notes[midi_note % 12]
    return note

# Define gColors
gColors = ["white", "black"]

# Loop through each gColor, mode, and interval to create SVG files
for gColor in gColors:
    for mode_name, mode_intervals in MODES.items():
        for interval in range(12):
            root_angle = interval * math.pi / 6
            # Define the line properties for the current chord
            chord_intervals = [mode_intervals[i] for i in [0, 2, 4]]  # Triad intervals
            angles = [(chord_interval * math.pi / 6) + root_angle for chord_interval in chord_intervals]
            # Colors: white, green, red
            colors = [gColor, "#e41a1c", "#4daf4a"]
            styles = ["", 'stroke-dasharray="1,2"', 'stroke-dasharray="10,5"']
            widths = [10, 10, 10]

            # Create the SVG content
            svg_content = create_svg(cx, cy, radius, angles, colors, styles, widths, gColor, mode_intervals, root_angle)

            # Get the note name
            note = get_note_and_octave(interval)

            # Save the SVG content to a file
            filename = f"{mode_name}_{note}_{gColor.upper()}.svg"
            save_svg(filename, svg_content)

            print(f"SVG file created: {filename}")
