from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from tabs import finder, chatbot  # Import the tab layouts

from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import json
from functions import seeker
import re
import dash
import tabs.chatbot as chatbot

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


app.layout = dbc.Container([
    dcc.Location(id='url', refresh=True),
    dbc.Row([
        dbc.Col(html.H1("Menu Browser"), width=12, md=4, className="text-center"),
        dbc.Col(html.Img(src="/assets/Bowser.png", style={'width': '100px'}), width=12, md=2)
    ], justify="center"),
    dbc.Row(style={'height': '50px'}),  # Creates a taller blank space

    dcc.Tabs(
        id="tabs",
        value="finder",
        children=[
            dcc.Tab(label="Finder", value="finder"),
            dcc.Tab(label="Chatbot", value="chatbot"),
            dcc.Tab(label="Analysis", value="analysis"),
            dcc.Tab(label="About", value="about"),
        ]
    ),
    html.Div(id="tabs-content")  # This will display the content of the selected tab
])
        












# Callback function to update the tab content dynamically
@app.callback(
    Output("tabs-content", "children"),  # Update the content of this div
    Input("tabs", "value")  # Trigger the callback based on selected tab
)
def render_content(tab_name):
    if tab_name == "finder":
        return finder.layout  # Return content for Tab 1
    elif tab_name == "chatbot":
        return chatbot.layout  # Return content for Tab 2
    return html.Div("Invalid Tab", style={"color": "red"})  # Default error message if needed







# Run the app server
if __name__ == "__main__":
    app.run_server(debug=True)
