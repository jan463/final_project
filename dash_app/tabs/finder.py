from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import json
from functions import seeker
import re
import dash
import tabs.chatbot as chatbot


df = pd.read_csv("../data/master.csv")


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




@callback(
    Output('url', 'href'),  # Update the 'href' of dcc.Location to trigger a page refresh
    Input('home-button', 'n_clicks')
)
def go_home(n_clicks):
    if n_clicks > 0:
        return '/'  # This will refresh the page
    return dash.no_update



# Callback to update recipes live
@callback(
    Output('recipe-results', 'children'),
    Output('page-store', 'data'),
    Output('pagination-info', 'children'),
    Output('pagination-row', 'style'),  # Add this output to conditionally show pagination
    Input('prep-time', 'value'),
    Input('cook-time', 'value'),
    Input('total-time', 'value'),
    Input('search-word', 'value'),
    Input('dish-type', 'value'),
    Input('calories', 'value'),
    Input('carbs', 'value'),
    Input('protein', 'value'),
    Input('ingredient-input', 'value'),
    Input('recipe-name-input', 'value'),
    State('page-store', 'data'),
    Input('prev-button', 'n_clicks'),
    Input('next-button', 'n_clicks')
)
def update_recipes(preptime, cooktime, totaltime, searchword, dish, calories, carbs, protein, ingredients, name, page_data, prev_clicks, next_clicks):
    # Default to empty string if None is provided for searchword
    searchword = searchword or ""
    ingredients = ingredients or ""
    name = name or ""
    dish = dish or "All"
    preptime = preptime or 0
    cooktime = cooktime or 0
    totaltime = totaltime or 0
    calories = calories or 0
    carbs = carbs or 0
    protein = protein or 0

    # Ensure page_data is a dictionary with 'page' and 'total_pages'
    if not isinstance(page_data, dict):
        page_data = {'page': 0, 'total_pages': 1}

    # Get the current page and total pages from the store
    current_page = page_data['page']

    # Filter the DataFrame based on input values
    filtered_df = seeker(df, ingredients, name, cooktime, preptime, totaltime, dish, searchword, calories, carbs, protein)

    # Calculate total pages
    items_per_page = 5
    total_items = len(filtered_df)
    total_pages = max(1, (total_items - 1) // items_per_page + 1)

    # Handle "Previous" and "Next" button logic
    if prev_clicks > 0 and current_page > 0:
        current_page -= 1
        prev_clicks = 0

    elif next_clicks > 0 and current_page < total_pages - 1:
        current_page += 1
        next_clicks = 0

    # Update the page store data
    page_data['page'] = current_page
    page_data['total_pages'] = total_pages

    # Get the slice of data for the current page
    start_index = current_page * items_per_page
    end_index = start_index + items_per_page
    page_df = filtered_df.iloc[start_index:end_index]

    if filtered_df.empty:
        return [], page_data, "Page 0 of 0", {'display': 'none'}  # No recipes and hide pagination

    # Create cards for the current page
# Create cards for the current page
    cards = [
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    # Image column (left)
                    dbc.Col([
                        html.Img(
                            src=re.findall(r'"([^"]*)"', row["images"])[0] if re.findall(r'"([^"]*)"', row["images"]) else "/assets/default.png", 
                            className="card-img-left", 
                            style={'width': '200px'}
                        ),
                        # Text content under the image
                        html.P(f"Rating: {row['aggregatedrating']}"), 
                        html.P(f'{row["servings"]} Servings, Serving size: {row["serving_size"]}g'),
                        html.Div([
                            html.Strong("Nutritional values: "),
                            html.P(f'{row["calories"]} calories, {row["cholesterolcontent"]}mg cholesterol, '
                                f'{row["sodiumcontent"]}mg Sodium, {row["fibercontent"]}g Fibers'),
                            html.P(f'{row["fatcontent"]}g fat, {row["saturatedfatcontent"]}g saturated fat, '
                                f'{row["carbohydratecontent"]}g Carbohydrates, {row["sugarcontent"]}g Sugar, '
                                f'{row["proteincontent"]}g Protein')
                        ]),
                    ], width=3, className="d-flex flex-column align-items-start"),  # Stack image and text vertically

                    # Text content column (right)
                    dbc.Col([
                        html.H4(row['name']),
                        html.P(row['description'], className="card-text"),
                        html.H5("Ingredients"),
                        html.Ul([
                            html.Li(ingredient) for ingredient in row['ingredients_raw_str'].strip('"[]').split('","')
                        ]),
                        html.H5("Steps"),
                        html.Ol([
                            html.Li(step) for step in re.split(r";|', '", row["steps"].strip("[]"))
                        ])
                    ], width=9),  # Text content on the right
                ])
            ])
        ], className="mb-4") for _, row in page_df.iterrows()
    ]




    # Page info display
    page_info = f"Page {current_page + 1} of {total_pages}"

    return cards, page_data, page_info, {'display': 'block'}  # Show pagination after search

def process_image_url(images_str):
    if not isinstance(images_str, str) or pd.isna(images_str):
        return "/assets/default.png"
    
    urls = re.findall(r'"([^"]*)"', images_str)
    return urls[0] if urls else "/assets/default.png"
