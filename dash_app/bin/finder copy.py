from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import json
from functions import seeker
import re
import dash
import tabs.chatbot as chatbot

# Layout
layout = dbc.Container([
    dbc.Row([  # Wrap filters in a row
        dbc.Col([
            html.Label("Preparation Time:"),
            dcc.Slider(id='prep-time', min=0, max=180, value=0,
                        marks={i: str(i) for i in range(0, 181, 30)}),

            html.Label("Cook Time:"),
            dcc.Slider(id='cook-time', min=0, max=180, value=0,
                        marks={i: str(i) for i in range(0, 181, 30)}),

            html.Label("Total Time:"),
            dcc.Slider(id='total-time', min=0, max=240, value=0,
                        marks={i: str(i) for i in range(0, 241, 60)})
        ], width=4),

        dbc.Col([
            html.Label("Dish Type:"),
            dcc.RadioItems(id='dish-type', options=[
                {'label': 'All', 'value': 'All'},
                {'label': 'Appetizer', 'value': 'Appetizer'},
                {'label': 'Salad', 'value': 'Salad'},
                {'label': 'Soup', 'value': 'Soup'},
                {'label': 'Main Dish', 'value': 'Main Dish'},
                {'label': 'Side', 'value': 'Side'},
                {'label': 'Dessert', 'value': 'Dessert'}
            ], value='All'),

            dbc.Row([html.Label("Search Word:"),
            dcc.Input(id='search-word', type='text', placeholder='Enter a search word')]),

            dbc.Row([html.Label("Name:"),
            dcc.Input(id='recipe-name-input', type='text', placeholder='Enter a search word')]),

            dbc.Row([html.Label("Ingredients:"),
            dcc.Input(id='ingredient-input', type='text', placeholder='Enter ingredients')])
        ], width=4),

        dbc.Col([
            html.Label("Calories per serving:"),
            dcc.Slider(id='calories', min=0, max=1000, value=0,
                        marks={i: str(i) for i in range(0, 1001, 200)}),

            html.Label("Carbohydrates (g) per serving:"),
            dcc.Slider(id='carbs', min=0, max=200, value=0,
                        marks={i: str(i) for i in range(0, 201, 50)}),

            html.Label("Protein (g) per serving:"),
            dcc.Slider(id='protein', min=0, max=100, value=0,
                        marks={i: str(i) for i in range(0, 101, 25)})
        ], width=4)
    ], justify="center", className="mb-4"),  # Ensure columns are aligned
    dbc.Row([
        dbc.Col(html.Button("Reset", id="home-button", n_clicks=0, className="btn btn-primary"), width=2, className="text-center")
    ], justify="center"),

    html.Hr(),

    # Recipe results (initially empty until filters change)
    dbc.Row(id='recipe-results', className="mt-4"),

    # Pagination and results (conditionally rendered)
    dbc.Row([
        dbc.Col(html.Button("Previous", id="prev-button", n_clicks=0, className="btn btn-secondary")),
        dbc.Col(html.Div(id="pagination-info", className="text-center mt-2")),
        dbc.Col(html.Button("Next", id="next-button", n_clicks=0, className="btn btn-secondary"))
    ], justify="center", className="mt-3", id="pagination-row", style={'display': 'none'}),  # Hidden initially

    dbc.Row([
        dcc.Store(id='page-store', data={'page': 0, 'total_pages': 1})
    ], justify="center", className="mt-3")
])
