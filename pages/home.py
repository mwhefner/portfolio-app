import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path="/",
    name="Portfolio",
    title="Data Science & Interactive Analytics Portfolio",
    description="Transforming complex data, math, and science concepts into interactive and pedagogically-informed software solutions. Explore publications, web projects and interactive dashboards.",
    image="as_webp/thumbnail.webp",
    meta_tags=[
        {"charset": "UTF-8"},
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0, viewport-fit=cover"},
        {"name": "robots", "content": "index, follow"},
        {"name": "keywords", "content": "Data Science, Dash Apps, Interactive Analytics, Machine Learning, Data Visualization, Research Software"},
        {"name": "author", "content": "Matt Hefner"},
        {"property": "og:type", "content": "website"},
        {"property": "og:image", "content": "as_webp/thumbnail.webp"},
        {"property": "og:url", "content": "{%url%}"},
        {"rel": "canonical", "href": "{%url%}"}
    ]
)

def makeCard(page):
    
    tags_dict = {
        "/Top_100_Steam_Games": {"web app", "games", "trending", "plotly figure friday", "interactive"},
        "/nyt_best_sellers": {"web app", "books", "trending", "plotly figure friday", "interactive"},
        "/ggea": {"web app", "education", "climate change", "applied science", "research", "interactive"},
        "/spectrawhorl": {"web app", "music", "education", "interactive"},
        "/everest": {"web app", "education","climate change", "applied science", "research"},
        "/mix_paper": {"journal paper","climate change", "applied science", "research"},
        "/briggs": {"journal paper","climate change", "applied science", "research"},
        "/cdiac": {"education","climate change", "applied science", "research"},
        "/webdg": {"web app", "education", "interactive"},
    }

    tag_colors = {
        "journal paper" : "primary", 
        "web app": "warning",
        "interactive": "warning",
        
        "games": "success",
        "books": "success",
        "music": "success",
        
        "climate change": "danger",
        
        "trending": "light",
        
        "education": "info",
        
        "applied science": "dark",
        "research": "dark",

    }
    
    those_that_link = {
        "/ggea" : "https://datadash.appstate.edu/cdiac",
        "/everest" : "https://datadash.appstate.edu/high-altitude-climate/lb",
        "/mix_paper" : "https://link.springer.com/article/10.1007/s11027-024-10149-x",
        '/briggs' : 'https://doi.org/10.1017/eds.2023.38',
        '/cdiac' : 'https://rieee.appstate.edu/projects-programs/cdiac/',
        '/spectrawhorl' : 'https://www.tonetornado.com/',
    }
    
    last_updated = {
        "/ggea" : "Last Updated 3.2024",
        "/webdg" : "Last Updated 3.2025",
        "/spectrawhorl" : "Last Updated 3.2025",
        "/everest" : "Last Updated 4.2024",
        "/mix_paper" : "",
        '/briggs' : '',
        '/cdiac' : 'Last Updated 11.2024',
        "/Top_100_Steam_Games": "Last Updated 2.2025",
        "/nyt_best_sellers": "Last Updated 2.2025",
        
    }
    
    last_update = ""
    
    page_path = page["path"]
    
    if page_path in last_updated :
        last_update = last_updated[page_path]
    
    if page_path in those_that_link :
        page_path = those_that_link[page_path]
    
    badges = []
    
    if page["path"] in tags_dict:
        badges = [
            dbc.Badge(tag, color=tag_colors.get(tag, "light"), className="m-1")
            for tag in tags_dict[page["path"]]
        ]
    
    image = []
    
    if page['image'] != "" :
        image = html.A(
            dbc.CardImg(alt=page.get("description", "/static/images/placeholder286x180.png"),src=page.get("image", "/static/images/placeholder286x180.png"), top=True),
            href=page_path
        )

    return dbc.Card(
        [
            image,
            dbc.CardBody(
                [
                    html.A(
                        html.H4(page["name"], className="card-title", style={"font-weight": "bold"}),
                        href=page_path,
                        className="text-decoration-none"  # Optional styling
                    ),
                    html.Div(badges, className="mb-2"),  # Display badges between H4 and P
                    dcc.Markdown(
                        page.get("description", "No description available."),
                        className="card-text",
                    ),
                    dbc.Button("Visit", color="primary", href=page_path),
                ]
            ),
            
            html.P([html.I(last_update)], className="my-0 ps-3") if last_update is not "" else None
        ],
        className="me-3 mb-3 p-3 custom-shadow-card"
    )

# Empty layout to be populated by a callback
layout = dbc.Row(
    id="card-container", 
    className="justify-content-center"
)

excluded_pages = ["/not-found-404", "/"] + ["/gregg"]

column_one_paths = ["/webdg", "/mix_paper", "/spectrawhorl"]
column_two_paths = ["/ggea", "/everest", "/Top_100_Steam_Games"]
column_three_paths = ["/cdiac", "/briggs", "/nyt_best_sellers"]

# Callback to populate the layout on app startup
@dash.callback(
    Output("card-container", "children"),
    Input("card-container", "id")  # Triggers once at startup
)
def populate_cards(_):

    pages = [page for page in dash.page_registry.values() if (page["path"] not in excluded_pages)]
    
    # Create a dictionary for easy lookup
    page_dict = {page["path"]: makeCard(page) for page in pages}
    
    # Create lists of pages that match the paths, maintaining the specified order
    column_one_pages = [page_dict[path] for path in column_one_paths if path in page_dict]
    column_two_pages = [page_dict[path] for path in column_two_paths if path in page_dict]
    column_three_pages = [page_dict[path] for path in column_three_paths if path in page_dict]
    
    return dbc.Col([
        
        html.Div([
            html.H1([
                "Web Portfolio", 
                html.Br(), 
                html.I(className="fa-solid fa-newspaper mt-2 mb-2"), 
            ], className="m-0"),
            
            html.Strong("Updated Weekly", className="m-0")
        ], style={"textAlign": "center"}, className="mt-3 mb-3"),

        
        dbc.Row([
            dbc.Col(column_one_pages, className = "p-0"),
            dbc.Col(column_two_pages, className = "p-0"),
            dbc.Col(column_three_pages, className = "p-0")
        ],
                
    )],style={'overflowY': 'auto', 'height': '100vh'})

