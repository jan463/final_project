import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import ast
import re
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load and process data
df = pd.read_csv("../data/master.csv")
df["nations"] = df["nations"].apply(ast.literal_eval)

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Menu Browser"), width=12, md=4, className="text-center"),
        dbc.Col(html.Img(src="/assets/Bowser.png", style={'width': '100px'}), width=12, md=2)
    ], justify="center"),

    dbc.Row([
        dbc.Col([
            dcc.Tabs([
                dcc.Tab(label='Finder', children=[
                    dbc.Row([html.Div(style={'height': '30px'}), 
                        dbc.Col([
                            dbc.CardBody(html.H3("Time", className="section-header")), 
                            html.Div([
                                html.Label("Preparation Time:"),
                                dcc.Slider(id='prep-time', min=0, max=180, value=0,
                                           marks={i: str(i) for i in range(0, 181, 30)})
                            ], className='mb-4'),

                            html.Div([
                                html.Label("Cook Time:"),
                                dcc.Slider(id='cook-time', min=0, max=180, value=0,
                                           marks={i: str(i) for i in range(0, 181, 30)})
                            ], className='mb-4'),

                            html.Div([
                                html.Label("Total Time:"),
                                dcc.Slider(id='total-time', min=0, max=240, value=0,
                                           marks={i: str(i) for i in range(0, 241, 60)})
                            ])
                        ], width=4),

                        dbc.Col([
                            dbc.CardBody(html.H3("Dish", className="section-header")), 
                            html.Div([
                                html.Label("Dish:"),
                                dcc.RadioItems(id='dish-type', options=[
                                    {'label': 'All', 'value': 'All'},
                                    {'label': 'Appetizer', 'value': 'Appetizer'},
                                    {'label': 'Salad', 'value': 'Salad'},
                                    {'label': 'Soup', 'value': 'Soup'},
                                    {'label': 'Main Dish', 'value': 'Main Dish'},
                                    {'label': 'Side', 'value': 'Side'},
                                    {'label': 'Dessert', 'value': 'Dessert'}
                                ], value='All')
                            ], className='mb-4'),

                            html.Div([
                                html.Label("Search Word:"),
                                dcc.Input(id='search-word', type='text', placeholder='Enter a search word')
                            ])
                        ], width=4), 

                        dbc.Col([
                            dbc.CardBody(html.H3("Nutritional values", className="section-header")), 
                            html.Div([
                                html.Label("Calories per serving:"),
                                dcc.Slider(id='calories', min=0, max=180, value=0,
                                           marks={i: str(i) for i in range(0, 181, 30)})
                            ], className='mb-4'),

                            html.Div([
                                html.Label("Carbohydrates [g] per Serving:"),
                                dcc.Slider(id='carbs', min=0, max=180, value=0,
                                           marks={i: str(i) for i in range(0, 181, 30)})
                            ], className='mb-4'),

                            html.Div([
                                html.Label("Protein [g] per Serving:"),
                                dcc.Slider(id='protein', min=0, max=240, value=0,
                                           marks={i: str(i) for i in range(0, 241, 60)})
                            ])
                        ], width=4)
                    ]),

                    dbc.Col([
                        html.Div([
                            html.Button("Search Recipes", id='search-button', n_clicks=0, className="mt-2 mb-4")
                        ], className="text-center")
                    ]),

                    dbc.Row(id='recipe-results', className="mt-4")
                ]),

                dcc.Tab(label='About', children=[
                    html.Div("About content here")
                ])
            ])
        ])
    ])
])

# Callbacks
@app.callback(
    Output('recipe-results', 'children'),  # Where results are displayed
    Output('current-page', 'data'),
    Input('search-button', 'n_clicks'),  # Triggered on search button click
    State('prep-time', 'value'),
    State('cook-time', 'value'),
    State('total-time', 'value'),
    State('dish-type', 'value'),
    State('search-word', 'value'),
    State('calorie-slider', 'value'),
    State('carb-slider', 'value'),
    State('protein-slider', 'value'),
    prevent_initial_call=True, 
    allow_duplicate=True
)

def search_recipes(n_clicks, preptime, cooktime, totaltime, dish, searchword, calories, carbs, protein):
    if n_clicks > 0:
        filtered_df = seeker(df, "x", "x", cooktime, preptime, totaltime, dish, searchword, calories, carbs, protein)
    else:
        filtered_df = df

    items_per_page = 10
    current_page = 0

    return update_page_content(filtered_df, current_page, items_per_page), current_page


@app.callback(
    Output('current-page-content', 'children'),  # Update page content
    Output('current-page', 'data'),
    [Input('prev-button', 'n_clicks'), Input('next-button', 'n_clicks')],
    [State('current-page', 'data'), State('filtered-df', 'data')], 
    allow_duplicate=True
)
def update_page(prev_clicks, next_clicks, current_page, filtered_df):
    items_per_page = 10
    total_items = len(filtered_df)
    total_pages = (total_items - 1) // items_per_page + 1
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if trigger == 'next-button' and current_page < total_pages - 1:
        current_page += 1
    elif trigger == 'prev-button' and current_page > 0:
        current_page -= 1
    
    return update_page_content(filtered_df, current_page, items_per_page), current_page

def update_page_content(filtered_df, current_page, items_per_page):
    start_index = current_page * items_per_page
    end_index = start_index + items_per_page
    page_df = filtered_df.iloc[start_index:end_index]

    # Return HTML representation of each recipe item
    paginated_content = []
    for index, row in page_df.iterrows():
        paginated_content.append(
            dbc.Card([
                dbc.CardBody([
                    html.H4(row['name']),
                    html.P(f"Rating: {row['aggregatedrating']}"), 
                    html.Img(src=re.findall(r'"([^"]*)"', row["images"])[0], className="card-img-top", style={'width': '200px'}),
                    html.P(f'{row["servings"]} Servings, Serving size: {row["serving_size"]}g'),
                    html.Div([
                        html.Strong("Nutritional values: "),
                        html.P(f'{row["calories"]} calories, {row["cholesterolcontent"]}mg cholesterol, '
                               f'{row["sodiumcontent"]}mg Sodium, {row["fibercontent"]}g Fibers'),
                        html.P(f'{row["fatcontent"]}g fat, {row["saturatedfatcontent"]}g saturated fat, '
                               f'{row["carbohydratecontent"]}g Carbohydrates, {row["sugarcontent"]}g Sugar, '
                               f'{row["proteincontent"]}g Protein')
                    ]),
                    html.P(row['description'], className="card-text"),
                    html.H5("Ingredients"),
                    html.Ul([
                        html.Li(ingredient) for ingredient in row['ingredients_raw_str'].strip('"[]').split('","')
                    ]),
                    html.H5("Steps"),
                    html.Ol([
                        html.Li(step) for step in re.split(r";|', '", row["steps"].strip("[]"))
                    ])
                ])
            ], className="mb-4")
        )
    return paginated_content


            # List all items with pagination
    paginated_content = []
    total_items = len(filtered_df)
    items_per_page = 10
    total_pages = (total_items - 1) // items_per_page + 1
    current_page = 0  # You could track this separately, e.g., using dcc.Store

    # Logic to only show the necessary page items
    start_index = current_page * items_per_page
    end_index = start_index + items_per_page
    page_df = filtered_df.iloc[start_index:end_index]

    for index, row in page_df.iterrows():
        paginated_content.append(
            dbc.Card([
                dbc.CardBody([
                    html.H4(row['name'], className="card-title"),
                    html.P(f"Rating: {row['aggregatedrating']}", className="card-text"),
                    html.Img(src=re.findall(r'"([^"]*)"', row["images"])[0], className="card-img-top", style={'width': '200px'}),
                    html.P(f'{row["servings"]} Servings, Serving size: {row["serving_size"]}g'),
                    html.Div([
                        html.Strong("Nutritional values: "),
                        html.P(f'{row["calories"]} calories, {row["cholesterolcontent"]}mg cholesterol, '
                                f'{row["sodiumcontent"]}mg Sodium, {row["fibercontent"]}g Fibers'),
                        html.P(f'{row["fatcontent"]}g fat, {row["saturatedfatcontent"]}g saturated fat, '
                                f'{row["carbohydratecontent"]}g Carbohydrates, {row["sugarcontent"]}g Sugar, '
                                f'{row["proteincontent"]}g Protein')
                    ]),
                    html.P(row['description'], className="card-text"),
                    html.H5("Ingredients"),
                    html.Ul([
                        html.Li(ingredient) for ingredient in row['ingredients_raw_str'].strip('"[]').split('","')
                    ]),
                    html.H5("Steps"),
                    html.Ol([
                        html.Li(step) for step in re.split(r";|', '", row["steps"].strip("[]"))
                    ])
                ])
            ], className="mb-4")
        )

        return paginated_content

    return "No recipes found."

if __name__ == "__main__":
    app.run_server(debug=True)