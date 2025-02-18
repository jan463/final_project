from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd


layout = html.Div([
    html.H4('Analysis of Iris data using scatter matrix'),
    dcc.Dropdown(
        id="dropdown",
        options=['calories', 'fatcontent', 'carbohydratecontent', 'proteincontent'],
        value=['calories', 'fatcontent'],
        multi=True
    ),
    dcc.Graph(id="graph"),
])


@callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))

def update_bar_chart(dims):
    df = pd.read_csv("../data/master.csv") # replace with your own data source
    fig = px.scatter_matrix(
        df, dimensions=dims)
    return fig