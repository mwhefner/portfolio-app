import dash
from dash import html

dash.register_page(
    __name__, 
    path="/cdiac", 
    name="CDIAC at AppState", 
    title="CDIAC at AppState", 
    description="I re-wrote the codebase for and produced The Carbon Dioxide Information Analysis Center's Global, Regional, and National Fossil-Fuel CO₂ Emissions for the last three years, contributing to the **Global Carbon Budget** in 2022, 2023 and 2024, respectively.", 
    image="assets/as_webp/cdiac.webp"
)

layout = html.Div([

])