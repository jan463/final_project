
import dash
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_core_components as dcc
import dash_html_components as html


markdown_text = """



# Final project: Recipe Finder Application

## Project Overview 🥒
This project involves analyzing a dataset of 500,000 recipes using learned data analytics techniques. The goal is to extract insights from the dataset, perform exploratory data analysis (EDA), apply inferential statistics, use SQL for Insights and develop interactive applications for users to make exploring fun.
The project includes two interactive applications:
- Streamlit App: A web-based interface for exploring recipe data.
- Dash App: A dashboard which features also an analytics section and an integrated chatbot.

## Data Analysis 🍎
### Exploratory Data Analysis (EDA)
- Data cleaning and preprocessing
- Visualization of key statistics using Seaborn, Matplotlib and Plotly
- Inferential Statistics

## Interactive Applications 🍇
### Streamlit App
- User-friendly interface for browsing recipes
- Different filters to choose

### Dash App
- Fast browsing and filtering for recipes
- Interactive analytics dashboard
- AI-powered chatbot for answering nutrition-related and general queries

## Instructions for use 🌶️
- Install requirements.txt for running code
- Use own OPENAI API key, otherwise Chatbot will be disabled
- Streamlit app (link available soon)
- Dash app (link available soon)

## Future Improvements 🍉
- Expand UI Dash app
- Add RAG for Chatbot
- Enhance Analytics
"""

layout = html.Div([
    dcc.Markdown(markdown_text, style={'white-space': 'pre-wrap', 'font-family': 'monospace'})
])


