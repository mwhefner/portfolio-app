import dash_bootstrap_components as dbc
from dash import html, callback, Output, Input

layout = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Subject", tab_id="Subject"),
                    dbc.Tab(label="Camera", tab_id="Camera"),
                    dbc.Tab(label="Lighting", tab_id="Lighting"),
                ],
                id="settings-tabs",
                active_tab="Subject",
            )
        ),
        dbc.CardBody(html.Div(id="settings-content", className="card-text")),
    ],
    
    className = "px-0"
    
)

@callback(
    Output("settings-content", "children"), [Input("settings-tabs", "active_tab")]
)
def tab_content(active_tab):
    return "This is tab {}".format(active_tab)