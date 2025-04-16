"""

home.py

This defines the home, "landing" or "index" page of the portfolio.

M W Hefner, 2025
MIT License

"""

from dash import html, dcc, Output, Input, register_page, callback, page_registry
import dash_bootstrap_components as dbc
from pages import makeCard

register_page(
    __name__,
    path="/",
    name="Portfolio",
    title="M. W. Hefner",
    description="I tackle complex problems and transform data, math and science concepts into interactive, pedagogically-informed software solutions.",
    image="webp/images/webdg9.webp",
    meta_tags=[
        {"charset": "UTF-8"},
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0, viewport-fit=cover"},
        {"name": "robots", "content": "index, follow"},
        {"name": "keywords", "content": "Data Science, Dash Apps, Interactive Analytics, Machine Learning, Data Visualization, Research Software"},
        {"name": "author", "content": "Matt Hefner"},
        {"property": "og:type", "content": "website"},
        {"property": "og:image", "content": "webp/thumbnail.webp"},
        {"property": "og:url", "content": "{%url%}"},
        {"rel": "canonical", "href": "{%url%}"}
    ]
)

# Empty layout to be populated by a callback
layout = dbc.Row(
    id="card-container", 
    className="justify-content-center"
)

# I just manually specify the layout here for now
# and I'll make something more complicated if I need it

column_one_paths = ["/webdg"]
column_two_paths = ["/research", "/dashboards"]
column_three_paths = ["/spectrawhorl"]

# Callback to populate the layout on app startup
@callback(
    Output("card-container", "children"),
    Input("card-container", "id")  # Triggers once at startup
)
def populate_cards(_):
    
    pages = [page for page in page_registry.values()]
    
    # Create a dictionary for easy lookup
    page_dict = {page["path"]: makeCard(page) for page in pages}
    
    # Create lists of pages that match the paths, maintaining the specified order
    column_one_pages = [page_dict[path] for path in column_one_paths if path in page_dict]
    column_two_pages = [page_dict[path] for path in column_two_paths if path in page_dict]
    column_three_pages = [page_dict[path] for path in column_three_paths if path in page_dict]
    
    return dbc.Col([
        dbc.Row([
            dbc.Col(column_one_pages, className = "p-0"),
            dbc.Col(column_two_pages, className = "p-0"),
            dbc.Col(column_three_pages, className = "p-0")
        ], className = "mt-3",
                
    )],style={'overflowY': 'auto', 'height': '100vh'})
