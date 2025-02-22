import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from tabs import finder, chatbot, analysis, about

from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import json
from functions import seeker
import re
import tabs.chatbot as chatbot
import tabs.analysis as analysis
import tabs.about as about

# initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=True),
    dbc.Row(style={'height': '20px'}),

    dbc.Row([
        dbc.Col(html.H1("Menu Browser"), width=12, md=4, className="text-center", style={"font-family": "Aptos"}),
        dbc.Col(html.Img(src="/assets/food_pic.jpg", style={'width': '100px'}), width=12, md=2)
    ], justify="center"),
    dbc.Row(style={'height': '20px'}),

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
    html.Div(id="tabs-content")  # display tab content
])

@app.callback(
    Output("tabs-content", "children"), 
    Input("tabs", "value")
)
def render_content(tab_name):
    if tab_name == "finder":
        return finder.layout 
    elif tab_name == "chatbot":
        return chatbot.layout 
    elif tab_name == "analysis":
        return analysis.layout 
    elif tab_name == "about":
        return about.layout
    return html.Div("Invalid Tab", style={"color": "red"})


if __name__ == "__main__":
    app.run_server(debug=True)
