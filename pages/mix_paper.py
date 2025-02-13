import dash
from dash import html

dash.register_page(
    __name__, 
    path="/mix_paper", 
    name="The changing mix of fossil fuels used and the related evolution of CO₂ emissions", 
    title="The changing mix of fossil fuels used and the related evolution of CO₂ emissions", 
    description="Published in Springer's Mitigation and Adaptation Strategies for Global Change journal.", 
    image="assets/mix_paper.png"
)

layout = html.Div([

])