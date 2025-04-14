import dash
from dash import Input, Output, State, dcc, html
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(
    __name__, 
    path="/nyt_best_sellers", 
    name="New York Times Best Sellers: Fiction", 
    title="New York Times Best Sellers: Fiction", 
    description="Explore the history of New York Times' Best-Selling Fiction. Made in under a week for the [Plotly community](https://community.plotly.com/)'s figure friday.", 
    image="assets/webp/thumbnails/nyt.webp"
)

# Data Wrangling----------------------

# Read the CSV and treat ISBN as a string to prevent conversion errors
df = pd.read_csv("assets/csv/bestsellers.csv", dtype={'ISBN': str})

# Get images later

layout = html.Div([
    
    html.H2("New York Times Best Sellers", style={"textAlign": "center"}, className="m-3"),
    
    html.H3("Fiction", style={"textAlign": "center"}),
    
    dcc.Store(id="current-page", data=1),  # Track pagination state

    # Pagination Controls
    dbc.Row(
        dbc.Col(
            dbc.Pagination(id="pagination", max_value=61, first_last=True, previous_next=True, fully_expanded=False),
            className="d-flex justify-content-center"  # Center the Pagination inside the column
        ),
        className="justify-content-center mt-3 mb-3"  # This ensures the column is centered inside the row
    ),

    # Book Grid (Dynamic Content)
    dbc.Row(id="book-grid"),
    
    
], style={
    "width": "100%", 
    "height": "100%", 
    'overflowY' : 'auto'},

    className = "false-body"
)

colors = {i: f"rgba(var(--bs-primary-rgb), {1 - (i - 1) * 0.05})" for i in range(1, 21)}

# Create a dictionary mapping week to week_text
week_to_text = dict(zip(df["week"], df["week_text"]))

@dash.callback(
    Output("book-grid", "children"),
    Input("pagination", "active_page")
)
def update_books(page):
    
    if not page:
        page = 1

    # Determine the range of weeks to show
    start_week = 727-((page) * 12 + 1)
    end_week = (start_week + 11)

    # Filter data for the current 10-week range
    books = df[(df["week"] >= start_week) & (df["week"] <= end_week)]

    # Create columns for each week
    cols = []
    for week, group in reversed(list(books.groupby("week"))):
        week_text = week_to_text.get(week, "Unknown Week")
        
        cards = [
            html.P("Week", 
                   style={"textAlign": "center"}, 
                   className="m-0"),
            html.P("of", 
                   style={"textAlign": "center"}, 
                   className="mb-1"),
            html.P(week_text, 
                   style={"fontWeight": "bold", "textAlign": "center"}, 
                   className="mb-1")  # Small margin for spacing
        ] + [
            dbc.Card(
                [
                    dbc.CardBody([
                        html.Img(
                            src=book["img_url"], 
                            className="img-fluid",
                            style={"width": "100%", "aspectRatio": "2/3", "objectFit": "cover"},
                            alt=f"The cover for the Rank {book['rank']}: |Title: {book['title']} |Author: {book['author']} |ISBN: {book['ISBN']}",
                        ),
                        dbc.Tooltip(
                            dbc.Card(
                                dbc.CardBody([
                                    html.P([
                                        html.Strong("Rank: "), 
                                        f"{book['rank']}"
                                    ], style={"marginBottom": "4px", "textAlign": "left"}),

                                    html.P([
                                        html.Strong("Title: "), 
                                        f"{book['title']}"
                                    ], style={"fontSize": "0.9rem", "marginBottom": "4px", "textAlign": "left"}),

                                    html.P([
                                        html.Strong("Author: "), 
                                        f"{book['author']}"
                                    ], style={"fontSize": "0.9rem", "marginBottom": "4px", "textAlign": "left"}),

                                    html.P([
                                        html.Strong("ISBN: "), 
                                        f"{book['ISBN']}"
                                    ], style={"fontSize": "0.9rem", "marginBottom": "4px", "textAlign": "left"}),

                                    html.P([
                                        html.Strong("Description: "), 
                                        book["description"]
                                    ], style={"fontSize": "0.85rem", "textAlign": "left", "marginBottom": "4px"}),
                                    
                                    html.P([
                                        html.Strong("Publication Date: "), 
                                        book["pub"]
                                    ], style={"fontSize": "0.9rem", "textAlign": "left"}),
                                ]),
                                style={"width": "250px", "padding": "10px"}
                            ),
                            target=f"tooltip-{index}",
                            placement="bottom",
                            style={"maxWidth": "300px", "whiteSpace": "normal"}
                        ),


                        html.P(book["rank"], 
                               style={"fontWeight": "bold", "textAlign": "center"}, 
                               className="m-0 p-0")
                    ],
                    style={"width": "100%", "aspectRatio": "2/3"}, className="p-0 m-0 mx-auto d-flex flex-column"),
                ],
                id=f"tooltip-{index}",
                className="p-0 m-0 mx-auto mb-2 " + f"ISBN_{book['ISBN']}",
                style={"cursor": "crosshair", "backgroundColor": colors[book["rank"]],"width": "100%", "aspectRatio": "2/3"},
            )
            for index, book in group.iterrows()
        ]

        # Add a bottom spacer to allow last card to scroll into view
        cards.append(html.Div(style={"height": "90vh"}))  

        cols.append(dbc.Col(
            dbc.Stack(cards, gap=0, className="pb-5"),  # Extra padding-bottom
            className="d-flex flex-column p-0 m-0 pe-2 mx-auto", 
            style={
                "maxHeight": "100vh",   # Full viewport height
                "overflowY": "auto",    # Enable scrolling
                "padding": "0",         # Clean up padding
                "minHeight": "0",       # Prevent flex bugs
                "overflowAnchor": "none" # Prevents jumpy scrolling
            }
        ))

    return dbc.Row(cols, className="justify-content-start mx-auto ms-1")


