import dash_bootstrap_components as dbc
from dash import html, Output, Input, dcc,clientside_callback,State, ClientsideFunction
from pages.differential_geometry.subject_tabs import curves, surfaces, embedded_curves, minimal_surfaces

# RENDER CALLBACK
# This renders the p5.js sketch of the requested subject
clientside_callback(
    ClientsideFunction(namespace="differential_geometry", function_name="render_webdg"),
    [
        Output("rendering_alert", "style"),
        Output("store_math", "data")
    ],
    [
        Input("render_curve", "n_clicks"),
        Input("render_surface", "n_clicks"),
    ],
    [
        State("c_x_validated", "data"),
        State("c_y_validated", "data"),
        State("c_z_validated", "data"),
        
        State("c_tstart_validated", "data"),
        State("c_tend_validated", "data"),
        State("c_nt_validated", "data"),
        State("c_colorby", "value"),
        State("c_colorpicker", "value"),
        
        State("s_x_validated", "data"),
        State("s_y_validated", "data"),
        State("s_z_validated", "data"),
        State("s_ustart_validated", "data"),
        State("s_uend_validated", "data"),
        State("s_nu_validated", "data"),
        State("s_vstart_validated", "data"),
        State("s_vend_validated", "data"),
        State("s_nv_validated", "data"),
        State("s_colorby", "value")
        
        
    ],
    prevent_initial_call=True,
)

# Subject modal layout
layout = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Curves", tab_id="curves"),
                    dbc.Tab(label="Surfaces", tab_id="surfaces"),
                    #dbc.Tab(label="Embedded Curves", tab_id="embedded curves"),
                    #dbc.Tab(label="Minimal Surfaces", tab_id="minimal surfaces"),
                ],
                id="subject-tabs",
                active_tab="curves",
            )
        ),
        dbc.CardBody(
            html.Div(
                id="subject-content", className="card-text", 
                children=[
                    html.Div(curves.layout, id="curves-content", style={"display": "block"}),
                    html.Div(surfaces.layout, id="surfaces-content", style={"display": "none"}),
                    html.Div(embedded_curves.layout, id="embedded-curves-content", style={"display": "none"}),
                    html.Div(minimal_surfaces.layout, id="minimal-surfaces-content", style={"display": "none"}),
                ]
            )
        ),
    ],
    className="px-0"
)


# Keeping the server callback around until I'm fully comfortable with the performance of the
# clientside replacement below
"""# control layout of subject modal
@callback(
    Output("subject-content", "children"), Input("subject-tabs", "active_tab")
)
def tab_content(active_tab = "curves"):
    if active_tab == "surfaces":
        return html.Div(
                [html.Div(curves, style={"display": "none"}),
                html.Div(surfaces, style={"display": "block"}),
                html.Div(embedded_curves, style={"display": "none"})]
            )  # Make the surface tab visible and the others not
    if active_tab == "embedded curves":
        return html.Div(
                [html.Div(curves, style={"display": "none"}),
                html.Div(surfaces, style={"display": "none"}),
                html.Div(embedded_curves, style={"display": "block"})]
            )  # Make the surface tab visible and the others not
    
    # Make the curves tab visible and the others not
    return html.Div(
            [html.Div(curves, style={"display": "block"}),
            html.Div(surfaces, style={"display": "none"}),
            html.Div(embedded_curves, style={"display": "none"})]
        )"""

clientside_callback(
    """
    function(active_tab) {
        let hide = {"display": "none"};
        let show = {"display": "block"};

        let curvesStyle = hide;
        let surfacesStyle = hide;
        let embeddedCurvesStyle = hide;
        let minimalSurfacesStyle = hide;

        if (active_tab === "curves") {
            curvesStyle = show;
        } else if (active_tab === "surfaces") {
            surfacesStyle = show;
        } else if (active_tab === "embedded curves") {
            embeddedCurvesStyle = show;
        } else if (active_tab === "minimal surfaces") {
            minimalSurfacesStyle = show;
        }

        return [curvesStyle, surfacesStyle, embeddedCurvesStyle, minimalSurfacesStyle];
    }
    """,
    Output("curves-content", "style"),
    Output("surfaces-content", "style"),
    Output("embedded-curves-content", "style"),
    Output("minimal-surfaces-content", "style"),
    Input("subject-tabs", "active_tab"),
)
