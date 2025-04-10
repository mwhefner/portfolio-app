"""

not_found_404.py

This defines the app's 404 page.

M W Hefner, 2025
MIT License

"""

import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([html.H1([html.I(className="fa-solid fa-road-barrier"), html.Br(), "Sorry, there's nothing here."])], style={"textAlign": "center", "paddingTop": "20vh", "fontSize": "20px"})