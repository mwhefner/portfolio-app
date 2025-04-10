"""

app.py

This is the script that the server machine runs with the specified python environment. It defines and configures the Dash application `app` and its layout `app.layout`. Specifically, the Creator and UI theme buttons and modals are defined. The creator modal contains a contact form the communicates with an external mysql server that should be defined in `database.conf` in the application's root directory. The server machine's WSGI entry point is `app.server`.

M W Hefner, 2025
MIT License

"""

# Needed packages
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, dcc, html, clientside_callback, page_container, no_update
import mysql.connector
import sshtunnel
import socket
import configparser
import sys
import time

# Style sheets for the app
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Initialize application
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX, dbc_css, dbc.icons.FONT_AWESOME],
    title = "M W Hefner's Web Portfolio",
    suppress_callback_exceptions=True,
    update_title = "thinkin' hard...",
    use_pages=True
)

# Bio text string
bio_text = """
I tackle complex problems and transform data, math and science concepts into interactive, pedagogically-informed software solutions.

<br>

I built this app to share my work. You can find the [source code on GitHub.](https://github.com/mwhefner/portfolio-app) Your feedback is strongly encouraged in the form below. It helps me improve. Also feel free to reach out with any questions or if you're interested in a collaboration or commission.

You can [Buy Me a Coffee](https://www.buymeacoffee.com/mwhefner) if you would like to support the applications I build.

"""

# THEME

# Light / Dark toggle callback
clientside_callback(
    """
    function (switchOn) {
       document.documentElement.setAttribute("data-bs-theme", switchOn ? "light" : "dark");
       return window.dash_clientside.no_update
    }
    """,
    Output("theme-switch", "id"),
    Input("theme-switch", "value"),  # Pass the stored mapping
)

# Just organizes the names of the themes and
# associates each one with a theme dictionary url
dbc_themes_url = {
    item: getattr(dbc.themes, item)
    for item in dir(dbc.themes)
    if not item.startswith(("_", "GRID"))
}
url_dbc_themes = dict(map(reversed, dbc_themes_url.items()))
dbc_themes_lowercase = [t.lower() for t in dbc_themes_url.keys()]

def template_from_url(url):
    """ returns the name of the plotly template for the Bootstrap stylesheet url"""
    return url_dbc_themes.get(url, "bootstrap").lower()

# Theme name callback updates the store component with stylesheet data
clientside_callback(
    """
    function(theme_name, themeMap) {
        if (themeMap && theme_name.toUpperCase() in themeMap) {
            return themeMap[theme_name.toUpperCase()];
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("themeStore", "data"),
    Input("themeSelection", "value"),
    State("themeMap", "data"),  # Pass the stored mapping
    prevent_initial_call=True 
)

# Theme url callback updates the theme stylesheet
# This can be improved. It must be changed
# when the css paths are changed.
clientside_callback(
    """
    function(theme_url) {

        if (!theme_url) return window.dash_clientside.no_update;

        // Create a new link element for the theme
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = theme_url;
        link.id = "theme-stylesheet";

        // Remove any existing theme stylesheets
        const oldLink = document.getElementById("theme-stylesheet");
        if (oldLink) {
            document.head.removeChild(oldLink);
        }

        // Append the new theme stylesheet
        document.head.appendChild(link);



        // Now, create a link element to universal CSS
        const customLink = document.createElement('link');
        customLink.rel = 'stylesheet';
        customLink.href = 'assets/css/universal.css';  // **Replace with universal CSS URL**
        customLink.id = "universal-stylesheet";



        // Remove any existing universal stylesheets
        const oldCustomLink = document.getElementById("universal-stylesheet");
        if (oldCustomLink) {
            document.head.removeChild(oldCustomLink);
        }

        // Append the universal stylesheet after the theme
        document.head.appendChild(customLink);

        return window.dash_clientside.no_update;
    }
    """,
    Output("themeTarget", "children"),
    [Input("themeStore", "data")]
)

# Define application layout
app.layout = dbc.Container([
    
    # A target output for the theme stylesheet callback (not strictly necessary)
    html.Div(id="themeTarget", style={"display": "none"}),
    # Default theme is LUX
    dcc.Store(data = dbc_themes_url['LUX'], id="themeStore", storage_type="local"),
    # Store theme URLs so the callback has access to it
    dcc.Store(id="themeMap", data=dbc_themes_url, storage_type="local"),

    dcc.Store(id="feedback-storage"),
    dcc.Store(id="feedback-dummy-target"),

    # This holds whatever page is being displayed
    page_container,

    # The rest of this will retain across all pages or
    # "subapps" of the application, as I think of it

    # Portfolio Modal
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("M W Hefner")),
            dbc.ModalBody(
                [
                    html.H1("Welcome", style={"textAlign": "center"}, className="m-5"),
                    
                    dbc.Carousel(
                        items=[
                            
                            {"key": "1", "src": "/assets/webp/images/webdg9.webp", "caption" : "A Cross Section of a Schwarz Surface"},
                            
                            {"key": "2", "src": "/assets/webp/images/webdg4.webp", "caption" : "A Frenet-Serret Frame on a Torus Knot"},
                            
                            {"key": "3", "src": "/assets/webp/images/webdg3.webp", "caption" : "A Gyroid"},
                            
                            {"key": "5", "src": "/assets/webp/images/Global Time Series - Second Draft.webp", "caption" : "Carbon Emissions Inventory Research"},
                            
                            {"key": "6", "src": "/assets/webp/images/tonetornado_still.webp", "caption" : "The Harmonic Series at C3"},

                        ],
                        controls=True,
                        indicators=False,
                        className="carousel-fade mb-5",
                        interval=3000
                    ),
                
                    dbc.Row(
                        [
                        dbc.Col(
                            dcc.Markdown(bio_text, dangerously_allow_html=True, style={"textAlign": "center"}, className = "px-5"),
                            md=12,  # Adjust as needed
                        ),
                        ], align = "center"
                    ),
                    
                    # Button to link to home
                    dbc.Row(
                        dbc.Col(
                                dbc.Button(
                                    dbc.Row([
                                            dbc.Col(html.Span("Portfolio", className="fw-bold"), width="auto"),
                                            dbc.Col(html.I(className="fa-solid fa-images"), width="auto", className="text-end")
                                        ]),
                                    id="portfolio-btn",
                                    color="primary",
                                    href="/"
                                ),
                                width="auto"
                            ),
                        justify="center", className="m-5"
                    ),
                    html.H4("Thank you for visiting.", style={"textAlign": "center"}, className="m-5"),
                    
                    # Contact form
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Contact", className="card-title", style={"textAlign": "center"}),
                                dbc.Form(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.FormFloating([
                                                        dbc.Input(type="text", id="name", placeholder="Name"),
                                                        dbc.Label("Name, Company or Institution"),
                                                    ]),
                                                    md=6
                                                ),
                                                dbc.Col(
                                                    dbc.FormFloating([
                                                        dbc.Input(type="email", id="email", placeholder="Email"),
                                                        dbc.Label("Reply Email"),
                                                    ]),
                                                    md=6
                                                ),
                                            ], className = "mt-4 mb-4", justify="space-around"
                                        ),
                                        dbc.FormFloating([
                                            dbc.Textarea(id="message", placeholder="Enter your comment or question here", style={"height": "100px"}),
                                            dbc.Label("Message"),
                                        ]),
                                        
                                        # contact form submit button
                                        dbc.Row(
                                            dbc.Col(dbc.Button("Submit Message", id="submit-btn", color="primary", href="/"), width="auto"),
                                            justify="center", className="m-4"
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        className="shadow-sm p-4",
                    ),
                ]


                ),
            dbc.ModalFooter(
                dbc.Button(
                    "Close",
                    id="close-portfolio-modal",
                    className="ms-auto",
                    n_clicks=0,
                )
            ),
        ],
        id="portfolio-modal",
        centered=True,
        size="lg",
        scrollable=True,
    ),

    # Theme Modal
    dbc.Modal(
        [

            dbc.ModalHeader(dbc.ModalTitle("Theme")),
            dbc.ModalBody(
                dbc.Row(
                    [

                        # Theme selection dropdown
                        dbc.Col(
                            dbc.Select(
                                id="themeSelection",
                                options=[{"label": t, "value": t} for t in dbc_themes_lowercase],
                                placeholder="lux",
                                persistence = True
                            ),
                            width="auto",
                            className = "p-4"
                        ),

                        # Dark / Light theme switch
                        dbc.Col(
                            children = [
                                    dbc.Label(className="fa fa-moon fs-3", html_for="theme-switch"),
                                    dbc.Switch(id="theme-switch", value=True, className="p-0 mx-3", persistence=True, style={"transform": "scale(1.5)"}),
                                    dbc.Label(className="fa fa-sun fs-3", html_for="theme-switch"),
                                ],
                            className="p-4 d-flex align-items-center",
                            width="auto"
                        ),

                    ],
                    className="align-items-center justify-content-center g-3",  # Centers vertically and horizontally
                ),
                className="d-block flex-column align-items-center justify-content-center h-100 w-100",  # Centers everything in the modal
            ),
            dbc.ModalFooter(

                dbc.Row([
                    dbc.Col(html.Em("Some themes alternate versions other than light/dark.")),
                    dbc.Button(
                        "Close",
                        id="close-theme-modal",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ], justify="center", style={"textAlign": "center"}, className = "gap-3")

            ),
        ],
        id="theme-modal",
        centered=True,
        size="md"
    ),

    # share popover
    dbc.Popover(
        dbc.PopoverBody(html.Em("share this web app")),
        target="share-button",
        trigger="hover",
    ),

    # theme popover
    dbc.Popover(
        dbc.PopoverBody(html.Em("select a UI color theme")),
        target="theme-button",
        trigger="hover",
    ),

    # me popover
    dbc.Popover(
        dbc.PopoverBody(html.Em("portfolio, info and feedback")),
        target="library-hamburger",
        trigger="hover",
    ),

    # Floating buttons using Affix-like positioning
    dbc.Stack([

        dbc.Button(
            dbc.Row([
                dbc.Col(html.Span("UI Themes", className="fw-bold"), width="auto"),
                dbc.Col(html.I(className="fa-solid fa-palette"), width="auto", className="text-end")
            ], className="d-flex justify-content-between align-items-center", align="center"),
            id="theme-button",
            color="secondary"
        ),
        dbc.Button(
            dbc.Row([
                dbc.Col(html.Span("Creator", className="fw-bold"), width="auto"),
                dbc.Col(html.I(className="fa-solid fa-bars"), width="auto", className="text-end")
            ], className="d-flex justify-content-between align-items-center", align="center"),
            id="library-hamburger",
            color="primary"
        )
    ], gap=3, className = "position-fixed bottom-0 end-0 m-3 justify-content-end")

])

# Portfolio modal callback
@app.callback(
    Output("portfolio-modal", "is_open"),
    [Input("library-hamburger", "n_clicks"), Input("close-portfolio-modal", "n_clicks"), Input('portfolio-btn', 'n_clicks')],
    State("portfolio-modal", "is_open"),
    prevent_initial_call=True,
)
def toggle_portfolio_modal(n_clicks, n_2, n_3, is_open):
    return not is_open

# Theme modal callback
app.clientside_callback(
    """
    function(n_clicks, n_2, is_open) {
        return !is_open;
    }
    """,
    Output("theme-modal", "is_open"),
    [Input("theme-button", "n_clicks"), Input("close-theme-modal", "n_clicks")],
    State("theme-modal", "is_open"),
    prevent_initial_call=True,
)

# get database configuration from `database.conf`
# and submit the form information to the database.
# the print()s in this section will print on the server log -
# my intent is to catch any messages that may fail

def load_db_credentials(conf_file="database.conf"):
    """Reads database and SSH credentials from a .conf file."""
    config = configparser.ConfigParser()
    config.read(conf_file)

    credentials = {
        "db_host": config.get("database", "host"),
        "db_user": config.get("database", "user"),
        "db_password": config.get("database", "password"),
        "db_name": config.get("database", "database"),
        "ssh_host": config.get("ssh", "ssh_host"),
        "ssh_user": config.get("ssh", "ssh_user"),
        "ssh_password": config.get("ssh", "ssh_password"),
    }
    return credentials

def is_running_locally(conf_file="database.conf"):
    config = configparser.ConfigParser()
    config.read(conf_file)
    """Detect if running locally or on PythonAnywhere."""
    hostname = socket.gethostname()
    print(f"Checking environment: Local machine hostname = {hostname}")
    return hostname != config.get("ssh", "ssh_host")  # Replace with your actual PythonAnywhere hostname

def get_db_connection(credentials=load_db_credentials()):
    """Establishes a database connection using SSH tunneling if local."""
    start_time = time.time()
    timeout = 60  # Set a timeout for connection attempt (e.g., 60 seconds)

    if is_running_locally():
        print("Running locally: Connecting via SSH Tunnel...")
        try:
            sshtunnel.SSH_TIMEOUT = 30.0
            sshtunnel.TUNNEL_TIMEOUT = 30.0

            # Create SSH tunnel
            print(f"Creating SSH tunnel to {credentials['ssh_host']}...")
            tunnel = sshtunnel.SSHTunnelForwarder(
                (credentials["ssh_host"]),  # SSH hostname
                ssh_username=credentials["ssh_user"],
                ssh_password=credentials["ssh_password"],
                remote_bind_address=(credentials["db_host"], 3306),
            )

            print("Starting SSH tunnel...")
            tunnel.start()
            print("SSH tunnel established.")

            # Debugging: Ensure the local port binding is successful
            print(f"SSH Tunnel established. Local bind port: {tunnel.local_bind_port}")

            # Connect to MySQL via the local endpoint of the tunnel
            print("Connecting to MySQL via SSH Tunnel...")

            conn = mysql.connector.MySQLConnection(
                user=credentials["db_user"],
                password=credentials["db_password"],
                host="127.0.0.1",  # Local address due to SSH tunnel
                port=tunnel.local_bind_port,
                database=credentials["db_name"],
                connection_timeout=30
            )
            print("MySQL connection established through tunnel.")
        except Exception as e:
            print(f"Error establishing SSH tunnel or MySQL connection: {e}")
            sys.exit(1)
    else:
        print("Running on PythonAnywhere: Direct DB connection...")
        try:
            conn = mysql.connector.MySQLConnection(
                host=credentials["db_host"],
                user=credentials["db_user"],
                password=credentials["db_password"],
                database=credentials["db_name"],
                use_pure=True,
                connection_timeout=30
            )
            print("MySQL connection established directly.")
        except Exception as e:
            print(f"Error connecting to MySQL: {e}")
            sys.exit(1)

    # Check if the connection is taking too long
    if time.time() - start_time > timeout:
        print("Connection attempt timed out.")
        sys.exit(1)

    return conn, tunnel

@app.callback(
    Output("feedback-dummy-target", "data"),
    Input("feedback-storage", "data"),
    State("name", "value"),
    State("email", "value"),
    State("message", "value"),
    prevent_initial_call=True
)
def save_feedback(n_clicks, name, email, message):

        print(f"Attempting to save feedback: name = {name}, email = {email}, message = {message}")
        # Connect to MySQL (local or remote)
        conn, tunnel = get_db_connection()
        cursor= conn.cursor()


        # Insert feedback into the database
        sql = "INSERT INTO feedback (user_name, email, message) VALUES (%s, %s, %s)"
        print(f"Executing SQL: {sql} with values ({name}, {email}, {message})")
        cursor.execute(sql, (name, email, message))
        conn.commit()
        print("Feedback saved successfully.")

        cursor.close()
        conn.close()
        tunnel.stop()

        return f"Message submitted: {name} {email} {message}. |||||| Thank you for your message."

@app.callback(
    Output("submit-btn", "children"),  # Change button text after submission
    Output("submit-btn", "color"),  # Change button color on success/error
    Output("submit-btn", "disabled"),  # Disable button after submission
    Output("feedback-storage", "data"),
    Input("submit-btn", "n_clicks"),
    State("name", "value"),
    State("email", "value"),
    State("message", "value"),
    prevent_initial_call=True
)
def submit_feedback(n_clicks, name, email, message):

    """Main callback to handle feedback submission."""

    if not name or not email or not message:

        print(f"Form data incomplete: name = {name}, email = {email}, message = {message}")

        return "Please fill all fields ❌", "danger", False, no_update

    try:
        print(f"Attempting to save feedback: name = {name}, email = {email}, message = {message}")

        return "Message Sent ✅", "success", True, f"Attempting to save feedback: name = {name}, email = {email}, message = {message}"

    except Exception as e:

        print(f"Error saving feedback: {e}")

        print(f"Message contents:NAME:{name}")
        print(f"Message contents:REPLY EMAIL:{email}")
        print(f"Message contents:MESSAGE{message}")

        return "Error: Try Again ❌", "danger", False, no_update

