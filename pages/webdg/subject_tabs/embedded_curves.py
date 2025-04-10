"""

embedded_curves.py

This subject tab is just a stub for now.

M W Hefner, 2025
MIT License

"""

import dash_bootstrap_components as dbc
from dash import html, Output, Input, dcc,clientside_callback,State, ClientsideFunction

layout = html.Div([
    
    dcc.Markdown(
        r"""
        #### Curves on Surfaces  

        Consider as the subject of study a **curve** $\alpha$ **on a surface** $S$ defined by:

        $$
        \alpha(t) = \big( u(t), v(t) \big)
        $$

        ($u(t)$ and $v(t)$ are functions of $t$ that represent the UV-coordinates of $\alpha$ on $S$.)

        The surface $S$ is given by:

        $$
        S(u,v) = \big( X(u,v), Y(u,v), Z(u,v) \big)
        $$

        The parameters $t$, $u$, and $v$ range over the intervals:

        $$
        t \in \left[ t_{\text{start}}, t_{\text{end}} \right], \quad 
        v \in \left[ v_{\text{start}}, v_{\text{end}} \right], \quad
        u \in \left[ u_{\text{start}}, u_{\text{end}} \right].
        $$

        ***

        #### Directions

        WebDG will create a mesh numerical approximation of your curve and surface using $n_t$ equally spaced intervals of the total $t$ interval, $n_u$ equally spaced intervals of the total $u$ interval, and $n_v$ equally spaced intervals of the total $v$ interval.

        - Use the forms below to define these functions and values. 

        - Use "Parse" to have WebDG process, understand, and validate an input. 

        - Once all inputs have valid parses, use "Render Subject" at the bottom to begin computing the mesh approximation of your surface from the parsed inputs.

        ***

        #### Presets

        Using a preset means overwriting the form inputs below with the definitions for the selected preset curve and surface combination. **Selecting 'Use' will erase any information currently in these forms.** Preset inputs must be parsed like any other.

        """, id="s_define", mathjax=True
    ),
])
