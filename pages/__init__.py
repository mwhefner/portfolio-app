"""

__init__.py

This defines the template for cards in "landing" or "index" pages of the portfolio.

M W Hefner, 2025
MIT License

"""

from dash import html, dcc, Output, Input, page_registry
import dash_bootstrap_components as dbc

def makeCard(page):
    
    # define tags manually here
    tags_dict = {
        "/Top_100_Steam_Games": {"games", "trending", "plotly figure friday"},
        "/nyt_best_sellers": {"books", "trending", "plotly figure friday"},
        "/ggea": {"climate change", "applied science", "research"},
        "/spectrawhorl": {"music", "education", "interactive"},
        "/everest": {"climate change", "applied science", "research"},
        "/mix_paper": {"paper","climate change", "applied science"},
        "/briggs": {"paper","climate change", "applied science"},
        "/cdiac": {"dataset","climate change", "applied science"},
        "/webdg": {"math", "education", "interactive"},
    }

    # set the color of a tag here
    tag_colors = {
        "journal paper" : "primary", 
        "web app": "warning",
        "interactive": "warning",
        
        "games": "success",
        "books": "success",
        "music": "success",
        "math": "success",
        
        "climate change": "danger",
        
        "trending": "light",
        
        "education": "info",
        
        "applied science": "dark",
        "research": "dark",

    }
    
    # if a page is just a link, specify the link here
    those_that_link = {
        "/ggea" : "https://datadash.appstate.edu/cdiac",
        "/everest" : "https://datadash.appstate.edu/high-altitude-climate/lb",
        "/mix_paper" : "https://link.springer.com/article/10.1007/s11027-024-10149-x",
        '/briggs' : 'https://doi.org/10.1017/eds.2023.38',
        '/cdiac' : 'https://rieee.appstate.edu/projects-programs/cdiac/',
        #'/spectrawhorl' : 'https://www.tonetornado.com/',
    }
    
    # if the page has a "last updated", specify it here
    last_updated = {
        "/ggea" : "Last Updated 3.2024",
        "/webdg" : "Last Updated 4.2025",
        "/spectrawhorl" : "Last Updated 4.2025",
        "/everest" : "Last Updated 4.2024",
        "/mix_paper" : "",
        '/briggs' : '',
        '/cdiac' : 'Last Updated 11.2024',
        "/Top_100_Steam_Games": "Last Updated 2.2025",
        "/nyt_best_sellers": "Last Updated 2.2025",
        
    }
    
    # Get page attributes for card
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

    # Finally, piece together the card for the page
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
            
            html.P([html.I(last_update)], className="my-0 ps-3") if last_update != "" else None
        ],
        className="me-3 mb-3 p-3 custom-shadow-card"
    )
    
    