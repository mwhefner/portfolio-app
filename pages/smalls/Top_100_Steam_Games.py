import pandas as pd
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, callback_context
import math

# register with the portfolio app
dash.register_page(
    __name__, 
    path='/Top_100_Steam_Games',
    title='Top 100 Steam Games',
    name='Top 100 Steam Games',
    description="Interactively explore and compare the top 100 most played games on Steam by multiple tags and price. Made in under a week for the [Plotly community](https://community.plotly.com/)'s figure friday.", 
    image="/assets/webp/thumbnails/Top_100_Steam_Games.webp"
)
# At some point I would like to learn to make this dynamic in the app
# themes = ["CERULEAN", "COSMO", "CYBORG", "DARKLY", "FLATLY", "JOURNAL", "LITERA", "LUMEN", "LUX", "MATERIA", "MINTY", "MORPH", "PULSE", "QUARTZ", "SANDSTONE", "SIMPLEX", "SKETCHY", "SLATE", "SOLAR", "SPACELAB", "SUPERHERO", "UNITED", "VAPOR", "YETI", "ZEPHYR"]

# First I handle the data-----------------------------------------------------

# Import data from the csv
df = pd.read_csv("assets/csv/Steam Top 100 Played Games - List.csv")

# Add rank to title
df["Name"] = df["Rank"].astype(str) + ". " + df["Name"]

# Convert numeric columns
df["Current Players"] = df["Current Players"].str.replace(",", "").astype(int)
df["Peak Today"] = df["Peak Today"].str.replace(",", "").astype(int)

# Convert "Free To Play" to 0 and remove £ symbol
df['Price'] = df['Price'].apply(lambda x: 0 if x == "Free To Play" else float(x.replace('£', '')))

# Convert currencies
df['Price_GBP'] = df['Price']
df['Price_EUR'] = df['Price_GBP'] * 0.83
df['Price_USD'] = df['Price_EUR'] * 0.97
df['Price_JPY'] = df['Price_USD'] / 0.0064  # Divide for correct conversion

# Utility for formatting price
def format_price(value, currency):
    """Formats a given price value based on the currency code."""
    currency_symbols = {
        "GBP": "£",
        "EUR": "€",
        "USD": "$",
        "JPY": "¥"
    }
    
    # get the right symbol
    symbol = currency_symbols.get(currency, "")
    
    if value == 0:
        # Outright call this Free-To-Play
        return "Free-To-Play"
    
    if currency == "JPY":
        return f"{symbol}{value:,.0f}"  # No decimal places for JPY
    else:
        return f"{symbol}{value:,.2f}"  # Two decimal places for other currencies

unique_tags = set()

# Gather unique tags, dropping any that have no tags for safety
# and dropping the "+". Split by ","
df["Genre Tags"].dropna().apply(lambda tags: unique_tags.update(tag.strip() for tag in tags.split(",") if tag.strip() != "+"))

# Convert to sorted list
unique_tags = sorted(unique_tags) 

def create_sunburst(unitRadios, tagsLayers, currencyRadios, priceSlider):
    
    if unitRadios == "Price":
        unitRadios += "_" + currencyRadios
        
    # Ensure 'Price_' + currencyRadios exists in the DataFrame
    price_column = 'Price_' + currencyRadios
    if price_column not in df.columns:
        raise ValueError(f"The column '{price_column}' does not exist in the DataFrame.")

    # Filter out games not in the price range and reset the index
    df_filtered = df.loc[(df[price_column] >= priceSlider[0]) & (df[price_column] <= priceSlider[1])].reset_index(drop=True)

    sunburst = pd.DataFrame()
    
    # Defaults
    labels = df_filtered['Name']
    parents =["" for _ in df_filtered['Name']]
    values = df_filtered[unitRadios]
    tumbnails = df_filtered['Thumbnail URL']
    
    if tagsLayers:
        
        # Added for tag leaves of the sunburst
        tag_labels = [""]  # Start with an empty label so concatenation works
        tag_parents = [""]  # Start with root parent reference
        tag_values = []
        tag_tumbnails = []

        # iterate through tags selected and create leaves' labels and parents
        for i, tag in enumerate(tagsLayers):
            
            # Determine which games do and do not have the tag
            df_filtered[tag] = df_filtered["Genre Tags"].str.contains(tag, na=False)
            
            # Update games' parents
            parents = [
                parent + (" " + tag if is_tag else " Non–" + tag)
                for parent, is_tag in zip(parents, df_filtered[tag])
            ]
            
            # Add new leaves to labels
            new_labels = [label + " " + tag for label in tag_labels] + [label + " Non–" + tag for label in tag_labels]
            
            # Determine new leaves' parents
            if i == 0:
                new_parents = ["", ""]  # Base case: First tag layer should have empty parents
            else:
                new_parents = tag_labels + tag_labels  # Subsequent tag layers refer to previous labels as parents

            tag_labels = tag_labels + new_labels  # Update labels
            tag_parents =tag_parents + new_parents  # Update parents

        tag_labels = tag_labels[1:]
        tag_parents = tag_parents[1:]
        
        labels = list(labels) + tag_labels
        #print("Labels:", tag_labels)
        parents += tag_parents
        #print("Parents:", tag_parents)
        
        def get_leaf_value(label):
            """ Recursively find the value of a label in the sunburst chart. """
            if label in df_filtered['Name'].values:
                return values[labels.index(label)]

            if label not in labels:
                return 0  # Return 0 if the label is not found to prevent errors

            children_values = [
                get_leaf_value(child) for child, parent in zip(labels, parents) if parent == label
            ]

            return sum(children_values)  # Aggregate children's values


        # Compute tag values
        tag_values = [get_leaf_value(label) for label in tag_labels]
        values = list(values) + tag_values
        #print("Values:", values)
                
        #tumbnails += tag_tumbnails

    # if there are tags, build the sunburst in layers
    sunburst["labels"] = [label.strip() for label in labels]
    sunburst["parents"] = [parent.strip() for parent in parents]
    sunburst["values"] = values
    sunburst["tumbnails"] = tumbnails
        
    # For the hover
    customdata = [
            "Price: " + 
            format_price(price, currencyRadios) + 
            "<br>" + 
            f"{current_players} " + 
            "Current Players.<br>" + 
            f"{peak_today}" + 
            " Peak Today.<br>" for price, current_players, peak_today in zip(df_filtered["Price_" + currencyRadios], df_filtered["Current Players"], df_filtered["Peak Today"])
        ] + ["" for i in range(len(sunburst) - len(df_filtered))]
    
    sunburst['colors'] = ["#000" if i % 2 == 0 else "#FFF" for i in range(len(df_filtered))] + ["#000" if i % 2 == 0 else "#FFF" for i in range(len(sunburst) - len(df_filtered))]

    sunburst['pattern_shape_sequence'] = ["/" if color == "#000" else "\\" for color in sunburst['colors']]
    sunburst['bgcolor'] = ["#333" if color == "#000" else "#EEE" for color in sunburst['colors']]
    
    # Make the figure
    fig = go.Figure(
        go.Sunburst(
            labels=sunburst["labels"],
            parents=sunburst["parents"],
            values=sunburst["values"],
            branchvalues="total",
            textfont_size=78,
            leaf=dict(opacity=1),
            marker=dict(
                colors=sunburst['colors'],
                pattern=dict(
                    shape=sunburst['pattern_shape_sequence'], 
                    bgcolor=sunburst['bgcolor'],
                    solidity=0.9
                )
            ),
            customdata=customdata,  # Apply formatting
            hovertemplate="<br><b>%{label}</b><br>%{customdata}<br><extra></extra><br>",  # Use formatted price
            insidetextorientation='radial',
            
        )
    )

    # Figure layout
    fig.update_layout(
        hoverlabel=dict(
            font_size=24,
            align="auto"  # Ensures the text inside the tooltip is centered
        ),
        margin=dict(t=10, l=10, r=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
        plot_bgcolor="rgba(0,0,0,0)",   # Transparent plot area
    )
    
    
    return fig

# The controls if the offcanvas panel
controls = dbc.Stack(
            [
                
            # Header and explanation
            dbc.Col(dbc.Alert([
                html.H6([
                    "Figure Friday 2025 (Week 5) | Steam Top 100 Played Games ",
                    dbc.Badge(["by ", html.A("me.", href = "https://community.plotly.com/u/hefnermw/activity")], pill=True, color="secondary", className="me-1")
                    ]),
                html.Div(style={"minWidth" : "100px"}),
                "This app was made in under a week with the open source Dash framework. Read about this week's challenge ",
                html.A("here on Plotly's Community forum.", href = "https://community.plotly.com/t/figure-friday-2025-week-5/90285")
                ], 
            color="primary", dismissable=False, className="mb-3")),
            
            # A dismissable info section.
            dbc.Col(dbc.Alert("1. Select order.", 
                            color="info", dismissable=True, className="mb-3")),
                
            # Sets the units for sunburst; results in a callback that changes
            # visibility of the price components below.
            html.Div(
                [
                    dbc.RadioItems(
                        id="unitRadios",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Current Players", "value": "Current Players"},
                            {"label": "Peak Today", "value": "Peak Today"},
                            {"label": "Current Price", "value": "Price"},
                        ],
                        value="Current Players",
                    ),
                ],
                className="radio-group mb-3 d-flex justify-content-center",
            ),
            
            # A dismissable info section.
            dbc.Col(dbc.Alert("2. Stack genre tags.", 
                            color="info", dismissable=True, className="mb-3")),
            
            # The dropdown where you select from the tags to create new layers to the sunburst
            dbc.Col(
                dcc.Dropdown(['1980s', "1990's", '2D', '2D Fighter', '3D', '3D Fighter', '3D Platformer', '4 Player Local', '4X', 'Action', 'Action RPG', 'Action Roguelike', 'Action-Adventure', 'Addictive', 'Adventure', 'Agriculture', 'Aliens', 'Alternate History', 'Animation & Modeling', 'Anime', 'Arcade', 'Assassin', 'Atmospheric', 'Audio Production', 'Automation', 'Automobile Sim', 'Base Building', 'Basketball', 'Battle Royale', 'Beautiful', 'Building', 'Capitalism', 'Card Battler', 'Card Game', 'Cartoon', 'Cartoony', 'Casual', 'Character Customisation. Choices Matter', 'Character Customization', 'Choices Matter', 'Choose Your Own Adventure', 'Cinematic', 'City Builder', 'Class-Based', 'Classic', 'Clicker', 'Co-op', 'Co-op Campaign', 'Cold War', 'Colony Sim', 'Colorful', 'Combat', 'Comedy', 'Competitive', 'Controller', 'Conversation', 'Cooking', 'Crafting', 'Creature Collector', 'Crime', 'Cute', 'Cyberpunk', 'Dark', 'Dark Fantasy', 'Dark Humor', 'Dating Sim', 'Deckbuilding', 'Demons', 'Design & Illustration', 'Destruction', 'Detective', 'Difficult', 'Dinosaurs', 'Diplomacy', 'Dragons', 'Driving', 'Dungeon Crawler', 'Dwarf', 'Dystopian', 'Early Access', 'Economy', 'Education', 'Emotional', 'Exploration', 'Extraction Shooter', 'FPS', 'Family Friendly', 'Fantasy', 'Farming', 'Farming Sim', 'Fast-Paced', 'Female Protagonist', 'Fighting', 'First-Person', 'Fishing', 'Flight', 'Football (Soccer)', 'Foreign', 'Free to Play', 'Funny', 'Futuristic', 'Game Development', 'Games Workshop', 'Gaming', 'Gore', 'Grand Strategy', 'Great Soundtrack', 'Hack and Slash', 'Hand-drawn', 'Heist', 'Hentai', 'Hero Shooter', 'Hex Grid', 'Hidden Object', 'Historical', 'Horror', 'Horses', 'Hunting', 'Idler', 'Immersive Sim', 'Indie', 'Inventory Management', 'Investigation', 'Isometric', 'JRPG', 'Life Sim', 'Local Co-Op', 'Local Multiplayer', 'Loot', 'Looter Shooter', 'Lore-Rich', 'MMORPG', 'MOBA', 'Magic', 'Management', 'Martial Arts', 'Massively Multiplayer', 'Mature', 'Medieval', 'Memes', 'Military', 'Minigames', 'Mod', 'Moddable', 'Modern', 'Mouse only', 'Multiplayer', 'Music', 'Mystery', 'Mythology', 'NSFW', 'Nature', 'Naval Combat', 'Nonlinear', 'Nostalgia', 'Nudity', 'Old School', 'Online Co-Op', 'Open World', 'Open World Survival Craft', 'Parkour', 'Perma Death', 'Photo Editing', 'Physics', 'Pixel Graphics', 'Platformer', 'Point & Click', 'Political', 'Post-apocalyptic', 'Procedural Generation', 'Psychedelic', 'Psychological', 'Psychological Horror', 'Puzzle', 'Puzzle Platformer', 'PvE', 'PvP', 'RPG', 'RTS', 'Racing', 'Real Time Tactics', 'Real-Time', 'Real-Time with Pause', 'Realistic', 'Relaxing', 'Remake', 'Replay Value', 'Resource Management', 'Robots', 'Roguelike', 'Roguelike Deckbuilder', 'Roguelite', 'Romance', 'Runner', 'Sandbox', 'Sci-fi', 'Score Attack', 'Sexual Content', 'Shooter', 'Simulation', 'Singleplayer', 'Social Deduction', 'Software', 'Souls-like', 'Soundtrack', 'Space', 'Split Screen', 'Sports', 'Stealth', 'Story Rich', 'Strategy', 'Strategy RPG', 'Superhero', 'Supernatural', 'Surival', 'Survival', 'Survival Horror', 'Swordplay', 'Tactical', 'Tactical RPG', 'Tanks', 'Team-Based', 'Text-Based', 'Third Person', 'Third-Person Shooter', 'Thriller', 'Time Management', 'Top-Down', 'Touch-Friendly', 'Tower Defense', 'Trading', 'Trading Card Game', 'Trains', 'Transportation', 'Turn-Based', 'Turn-Based Combat', 'Turn-Based Strategy', 'Turn-Based Tactics', 'Utilities', 'VR', 'Vehicular Combat', 'Video Production', 'Violent', 'Visual Novel', 'Voxel', 'War', 'Wargame', 'Warhammer 40K', 'Web Publishing', 'Western', 'World War II', 'Zombies', 'eSports'],
                id="tagsLayers",
                value=None,
                placeholder="Select layers by tag...",
                multi=True
            ), className="mb-3"),

            # A dismissable info section.
            dbc.Col(dbc.Alert("3. Filter by price.", 
                            color="info", dismissable=True, className="mb-3")),
            
            # Currency selection for the money
            html.Div(
                [
                    dbc.RadioItems(
                        id="currencyRadios",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "$ USD", "value": "USD"},
                            {"label": "£ GBP", "value": "GBP"},
                            {"label": "€ EUR", "value": "EUR"},
                            {"label": "¥ JPY", "value": "JPY"},
                        ],
                        value="USD",
                    ),
                ],
                className="radio-group mb-4 d-flex justify-content-center",
            ),

            # Range for the money
            dbc.Col(dcc.RangeSlider(
                id="priceSlider",
                min=0,
                max=100,
                step=0.1,
                marks={i: f"${i}" for i in range(0, 101, 25)},
                tooltip={"always_visible": True, "placement": "top"},
                # Only use if callbacks are all clientside...
                #updatemode='drag'
            ), className="mb-3"),
            
            # Credits section for source and license
            dbc.Col(dbc.Alert([
                dbc.Badge("Plotly Community", pill=True, color="dark", href="https://community.plotly.com", target="_blank", className="m-1 p-2"),
                dbc.Badge("Source on GitHub", pill=True, color="dark", href="https://github.com/mwhefner/figure-friday/blob/main/Week%205/ff_2025_05.py", target="_blank", className="m-1 p-2"),
                dbc.Badge("MIT License", pill=True, color="dark", href="https://opensource.org/licenses/MIT", target="_blank", className="m-1 p-2")
                ], 
                color="dark",
                className="mb-3", 
                style={"textAlign": "center"}
            ))
            ],
            gap=3,
        ),

# Callback for toggling the offcanvas panel
@dash.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Callback for toggling currency
@dash.callback(
    [
        Output("priceSlider", "max"),
        Output("priceSlider", "step"),
        Output("priceSlider", "marks"),
        Output("priceSlider", "value")
    ],
    Input("currencyRadios", "value")
)
def update_price_slider(currency):
    m = math.ceil(max(df['Price_' + currency]))  # Ensure max is an integer
    
    if currency == "USD" or currency == "EUR" or currency == "GBP":
        d = 0.01
    else:
        d = 1

    marks = {i: f"{format_price(i, currency)}" for i in range(0, m + 1, m)}  # Ensure proper range

    return m, d, marks, [0,m]

# Callback for recreating the sunburst
@dash.callback(
    Output("sunburstDisplay", "figure"),
    [
        Input("unitRadios", "value"),
        Input("tagsLayers", "value"),
        Input("currencyRadios", "value"),
        Input("priceSlider", "value")
    ]
)
def redraw_sunburst(unitRadios, tagsLayers, currencyRadios, priceSlider):
    return create_sunburst(unitRadios, tagsLayers, currencyRadios, priceSlider)

@dash.callback(
    [Output("modal", "is_open"), Output("modalTitle", "children"), Output("modalBody", "children")],
    [Input("sunburstDisplay", "clickData"), Input("close", "n_clicks")],
    [State("modal", "is_open"), State("currencyRadios", "value")]
)
def display_click_data(clickData, n_close, is_open, currencyRadios):
    # For the game modal when a game leaf is clicked
    triggered_id = callback_context.triggered_id
    if not triggered_id:  # This means it was triggered initially (no input yet)
        return dash.no_update  # Do not trigger any update for the initial callback

    if is_open:
        return not is_open, "Collapsed", "Collapsed"
    
    if clickData:
        clicked_label = clickData["points"][0]["label"]  # Get the clicked leaf's name
        
        # If you clicked a game lead, show the card modal
        if clicked_label in df["Name"].values:
            filtered_data = df.loc[df["Name"] == clicked_label].iloc[0]  # Extract the first (and in this case, only) row
            
            # Makes a nice little card for the game
            modal_body = dbc.Col([
                html.Img(src=filtered_data['Thumbnail URL'], style={"width": "100%", "margin-bottom": "20px"}),
                dbc.Card([
                    dbc.CardHeader("Details"),
                    dbc.CardBody([
                        html.P(f"Rank: {filtered_data['Rank']}"),
                        html.P(f"Price: {format_price(filtered_data['Price_' + currencyRadios], currencyRadios)}"),
                        html.P(f"Current Players: {filtered_data['Current Players']}"),
                        html.P(f"Peak Today: {filtered_data['Peak Today']}"),
                        html.P(f"Genre Tags: {filtered_data['Genre Tags']}"),
                        html.P([
                            "Store Link: ", 
                            html.A("Click Here", href=filtered_data['Store Link'], target="_blank")
                        ]),
                    ])
                ], style={"margin-top": "20px"})
            ])

            return True, f"{filtered_data['Name']}", modal_body

    return dash.no_update

# Define the applications layout
layout = html.Div(dbc.Container([
    
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Header", id="modalTitle")),
            dbc.ModalBody(id="modalBody"),
            dbc.ModalFooter(
                dbc.Button(
                    "Close", id="close", className="ms-auto", n_clicks=0
                )
            ),
        ],
        id="modal",
        centered=True,
        is_open=False,
        size="sm",
    ),
    
    html.Span(id="output"),
    
    # The layout is in three main parts:
    
    # The toggle for the offcanvas panel
    dbc.Button(
        [
            html.I(className="fa-solid fa-bars me-2"),
            "Top 100 Games on Steam",
        ],
        id="open-offcanvas",
        n_clicks=0,
        style={
            "position": "fixed",
            "top": "10px",
            "left": "10px",
            "zIndex": "2"
        }
    ),
    
    # The offcanvas panel itself
    dbc.Offcanvas(
        controls,
        id="offcanvas",
        title="Top 100 Games on Steam",
        is_open=False,
        className="dbc",
        backdrop=False
    ),

    # The plot itself (with defaults)
    dcc.Graph(id = "sunburstDisplay", style={"flex": "1", "width": "100%"}),

], fluid=True, className="vh-100 d-flex flex-column"))

