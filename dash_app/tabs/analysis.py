from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
from itertools import chain
import plotly.colors as pc
import ast
import dash_bootstrap_components as dbc

#df = pd.read_csv("../data/master.csv")
file_url = "https://drive.google.com/file/d/11gv-CdPllRVLrt6QRTE5MwNNN1gBj5l2/view?usp=sharing"
df = pd.read_csv(file_url)

ast.literal_eval(df["nations"][2])

def convert_list(x):
    return ast.literal_eval(x)

df["nations"] = df["nations"].apply(convert_list)

# flatten df
nations_flat = list(chain.from_iterable(df["nations"]))
counts = pd.Series(nations_flat).value_counts().head(10)
counts_df = pd.DataFrame({"Country": counts.index, "Number of Recipes": counts.values})

# plotly bar plot
dark_green_palette = pc.sequential.Greens[::-1][:6]

fig = px.bar(
    counts_df, 
    x="Country", 
    y="Number of Recipes", 
    title="Number of Recipes from Countries",
    color="Number of Recipes", 
    color_continuous_scale=dark_green_palette, 
    labels={"Country": "Country", "Number of Recipes": "Number of Recipes"}
)

fig.update_layout(
    xaxis_tickangle=-45, 
    title_font=dict(size=25, family="Arial", weight="bold"),
    xaxis_title_font=dict(size=16, weight="bold"),
    yaxis_title_font=dict(size=16, weight="bold"),
    plot_bgcolor="white", 
    xaxis=dict(showgrid=False), 
    yaxis=dict(showgrid=True, gridcolor="lightgray"), 
    margin=dict(t=40, b=120, l=50, r=50), 
    width=1200, 
    height=600
)


melted = df.melt(value_vars=["calories", "fatcontent", "carbohydratecontent", "proteincontent"], var_name="nutrition_values", value_name="value")
fig2 = px.box(
    melted, 
    x="nutrition_values", 
    y="value", 
    color="nutrition_values", 
    title="Nutrition Values"
    )

fig2.update_layout(
    title_font=dict(size=25, family="Arial", weight="bold"),
    xaxis_title_font=dict(size=16, weight="bold"),
    yaxis_title_font=dict(size=16, weight="bold"),
    xaxis_title="Dispersion of Nutrition Values", 
    yaxis_title="Value", 
    width=1200, 
    height=600
)

layout = html.Div([
    dbc.Row(style={'height': '30px'}),
    dcc.Graph(figure=fig), 
    dcc.Graph(figure=fig2)
])