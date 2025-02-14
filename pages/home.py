import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path="/",
    name="Portfolio",
    title="Data Science & Interactive Analytics Portfolio",
    description="Transforming complex data, math, and science concepts into interactive and pedagogically-informed software solutions. Explore publications, web projects, and interactive dashboards.",
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
        "/tonetornado": {"web app", "music", "education", "interactive"},
        "/everest": {"web app", "education","climate change", "applied science", "research"},
        "/mix_paper": {"journal paper","climate change", "applied science", "research"},
        "/briggs": {"journal paper","climate change", "applied science", "research"},
        "/cdiac": {"education","climate change", "applied science", "research"},
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
        "/tonetornado" : "https://www.tonetornado.com",
        "/everest" : "https://datadash.appstate.edu/high-altitude-climate/lb",
        "/mix_paper" : "https://link.springer.com/article/10.1007/s11027-024-10149-x",
        '/briggs' : 'https://doi.org/10.1017/eds.2023.38',
        '/cdiac' : 'https://rieee.appstate.edu/projects-programs/cdiac/',
    }
    
    page_path = page["path"]
    
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
                    html.P(
                        page.get("description", "No description available."),
                        className="card-text",
                    ),
                    dbc.Button("Visit", color="primary", href=page_path),
                ]
            ),
        ],
        className="me-3 mb-3 p-3"
    )



# Empty layout to be populated by a callback
layout = dbc.Row(
    id="card-container", 
    className="justify-content-center"
)

excluded_pages = ["/not-found-404", "/"] + ["/gregg", "/differential_geometry"]

# Callback to populate the layout on app startup
@dash.callback(
    Output("card-container", "children"),
    Input("card-container", "id")  # Triggers once at startup
)
def populate_cards(_):

    pages = [page for page in dash.page_registry.values() if (page["path"] not in excluded_pages)]
    return dbc.Col([
        html.Div([html.H1(["Portfolio", html.Br(), html.I(className="fa-solid fa-newspaper mt-2 mb-2"), html.Br(), "Updated weekly."], className="mt-3 mb-3")], style={"textAlign": "center"}),
        dbc.Row([
            dbc.Col([makeCard(page) for i, page in enumerate(pages) if i % 3 == 0], className = "p-0"),
            dbc.Col([makeCard(page) for i, page in enumerate(pages) if i % 3 == 1], className = "p-0"),
            dbc.Col([makeCard(page) for i, page in enumerate(pages) if i % 3 == 2], className = "p-0")
        ],
    )],style={'overflowY': 'auto', 'height': '100vh'})

