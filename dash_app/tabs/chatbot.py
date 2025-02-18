from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import os
from openai import OpenAI
from dotenv import load_dotenv
import re

# api keys
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are a kitchen aid and give assistance in finding recipes and answering questions about cooking, food, drinks, and nutrition.
Format lists properly with bullet points or numbering.
"""

############ layout ############
layout = dbc.Container([
    html.H1("Your personal kitchen aid 🥒"),
    
    # chat window
    html.Div(id='chat-output', style={
        'border': '1px solid #ccc', 'padding': '15px', 'height': '400px', 
        'overflowY': 'auto', 'backgroundColor': '#f9f9f9', 'borderRadius': '10px',
        'display': 'flex', 'flexDirection': 'column', 'gap': '15px'
    }),
    
    # input
    dcc.Textarea(id='user-input', placeholder='I am your kitchen aid, let me help you!', 
                 style={'width': '100%', 'height': 80}),
    html.Button('Send', id='submit-btn', n_clicks=0, className='btn btn-primary', style={'marginTop': '10px'}),

    # chat history
    dcc.Store(id='chat-history', data=[])
])

# formatting
def format_text_with_lists(text):
    """Convert text into properly formatted lists when applicable."""
    lines = text.split("\n") 
    formatted_content = []

    ul_items = [] 
    ol_items = [] 
    is_ordered = False 

    for line in lines:
        line = line.strip()

        # detect unordered list items (- or •)
        if re.match(r"^[-•]\s", line):
            ul_items.append(html.Li(line[2:]))  # Remove bullet character
        # detect ordered list items (1., 2., ...)
        elif re.match(r"^\d+\.\s", line):
            ol_items.append(html.Li(line[3:]))  # Remove number
            is_ordered = True
        else:
            if ul_items:
                formatted_content.append(html.Ul(ul_items, className="list-style"))
                ul_items = []
            if ol_items:
                formatted_content.append(html.Ol(ol_items, className="list-style"))
                ol_items = []
                is_ordered = False

            # normal text
            if line:
                formatted_content.append(html.P(line))

    # other lists at the end
    if ul_items:
        formatted_content.append(html.Ul(ul_items, className="list-style"))
    if ol_items:
        formatted_content.append(html.Ol(ol_items, className="list-style"))

    return formatted_content

@callback(
    Output('chat-output', 'children'),
    Output('chat-history', 'data'),
    Input('submit-btn', 'n_clicks'),
    State('user-input', 'value'),
    State('chat-history', 'data'),
    prevent_initial_call=True
)
def get_gpt_response(n_clicks, user_input, chat_history):
    if not user_input:
        return "Please enter a question.", chat_history

    chat_history.append({"role": "user", "content": user_input})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    bot_response = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": bot_response})

    chat_display = []

    # format chat history
    for msg in chat_history:
        formatted_content = format_text_with_lists(msg["content"])  

        if msg["role"] == "user":
            chat_display.append(html.Div([html.B("You: ")] + formatted_content, className="message-container user-message"))
        elif msg["role"] == "assistant":
            chat_display.append(html.Div([html.B("Kitchen Aid: ")] + formatted_content, className="message-container assistant-message"))

    return chat_display, chat_history
