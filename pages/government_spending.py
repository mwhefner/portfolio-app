import dash
from dash import Input, Output, State, dcc, html, ctx
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

"""dash.register_page(
    __name__, 
    path="/government_spending", 
    name="Forecasting Daily U.S. Government Spending in Python", 
    title="3 Methods for Forecasting Daily U.S. Government Spending in Python", 
    description="See today's U.S. government spending, interactively analyze past spending, and compare statistical machine learning techniques that forecast future spending.", 
    image="assets/as_webp/government_spending.webp"
)"""

# Data Wrangling----------------------

# Read the CSV and treat ISBN as a string to prevent conversion errors
# df = pd.read_csv("assets/bestsellers.csv", dtype={'ISBN': str})

# Main page layout

layout = html.Div(
    
    [
        
        dcc.Location(id = "url"),
        
        # Navigation bar
        dbc.Navbar(
            dbc.Container(
                [

                dbc.Nav(
                    children=[
                        dbc.NavItem(dbc.NavLink("Overview", href="#Overview", id= "Overview", n_clicks=0)),
                        dbc.NavItem(dbc.NavLink("Temporal Fusion Transformer", href="#TFT", id= "TFT", n_clicks=0)),
                        dbc.NavItem(dbc.NavLink("VARMAX", href="#VARMAX", id="VARMAX", n_clicks=0)),
                        dbc.NavItem(dbc.NavLink("DeepAR", href="#DeepAR", id="DeepAR", n_clicks=0)),
                        dbc.NavItem(dbc.NavLink("Discussion", href="#Discussion", id="Discussion", n_clicks=0)),
                    ],
                    style={"display": "flex", "justify-content": "space-around", "width": "100%"}
                ),
                
                ]
            ),
            color="primary",
            dark=True,
        ),
        
        html.Div(
            
            id="scroll-container", 
            
            className = "p-5",
    
            style = {
                "width": "100%", 
                "height": "100%", 
                'overflowY' : 'auto'
            }
            
        ),
    
    ], 
    
    style = {
        "width": "100%", 
        "height": "100%"
    }
)

# Overview subpage layout

overview_markdown_1 = dcc.Markdown(
    """
    # Overview
    
    For this week's [Plotly figure friday](https://community.plotly.com/t/figure-friday-2025-week-7/90557), I applied time series forecasting techniques to **daily U.S. government spending** with data from [The Hamilton Project](https://www.hamiltonproject.org/data/tracking-federal-expenditures-in-real-time/). These techniques were:
    
    - a [**Temporal Fusion Transformer (TFT)** model](#TFT), a deep learning model that captures long-range dependencies,
    - a [**Vector AutoRegressive Moving-Average with Exogenous Variables (VARMAX)** model](#VARMAX), a classical statistical model for multivariate time series and
    - a [**DeepAR**](#) model, a probabilistic forecasting model using recurrent neural networks.
    
    I use the [discussion](#Discussion) tab above to discuss interpretability and quantification of uncertainty.
    
    # Data
    
    """
)

overview_fig_1 = "I am a plotly time series figure that can be toggled between proportional or absolute over time. Similar to the CDIAC dashboard, each of my categories can be toggled."

overview_fig_2 = "I am (a row of) button(s) for changing the figure above. 1) proportion - to - absolute."

overview_layout = html.Div(
    [
        overview_markdown_1,
        
        overview_fig_2,
        
        overview_fig_1,
    ], 
    
    style = {
        "width": "100%", 
        "height": "100%"
    }
)

# TFT subpage layout

tft_markdown = dcc.Markdown(
    """
    # TFT
    """
)

# Plot of forecast
# explanation of model (shows implementation)
# training (shows implementation)
# diagnostics
        
tft_layout = html.Div(
    [
        tft_markdown,
        # Plot of forecast
        # explanation of model (shows implementation)
        # training (shows implementation)
        # diagnostics
    ], 
    
    style = {
        "width": "100%", 
        "height": "100%"
    }
)

# Varmax subpage layout

varmax_markdown = dcc.Markdown(
    """
    # VARMAX
    """
)

varmax_layout = html.Div(
    [
        varmax_markdown
    ], 
    
    style = {
        "width": "100%", 
        "height": "100%"
    }
)

# DeepAR subpage layout

deepar_markdown = dcc.Markdown(
    """
    # DeepAR
    """
)

deepar_layout = html.Div(
    [
        deepar_markdown
    ], 
    
    style = {
        "width": "100%", 
        "height": "100%"
    }
)

# Discussion subpage layout

discussion_markdown = dcc.Markdown(
    """
    # Discussion
    """
)

discussion_layout = html.Div(
    [
        discussion_markdown
    ], 
    
    style = {
        "width": "100%", 
        "height": "100%"
    }
)

# Callback to select subpage layout

@dash.callback(
    [Output("scroll-container", "children"),
     Output("Overview", "active"),
     Output("TFT", "active"),
     Output("VARMAX", "active"),
     Output("DeepAR", "active"),
     Output("Discussion", "active")],
    [Input("url", "hash")]
)
def update_window(hash):
    if not hash:
        hash = "#Overview"  # Default to Overview if no hash is present

    content_map = {
        "#Overview": overview_layout,
        "#TFT": tft_layout,
        "#VARMAX": varmax_layout,
        "#DeepAR": deepar_layout,
        "#Discussion": discussion_layout,
    }
    
    active_map = {key: key == hash for key in content_map}

    return (content_map.get(hash, overview_layout),
            active_map["#Overview"],
            active_map["#TFT"],
            active_map["#VARMAX"],
            active_map["#DeepAR"],
            active_map["#Discussion"])
