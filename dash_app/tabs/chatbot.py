from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# System Prompt
SYSTEM_PROMPT = """
You are a kitchen aid and give assistance in finding recipes and answering questions about cooking, food, drinks, and nutrition.
"""

# Layout
layout = dbc.Container([
    html.H1("Your personal kitchen aid 🥒"),
    
    # Chat window
    html.Div(id='chat-output', style={
        'border': '1px solid #ccc', 'padding': '10px', 'height': '400px', 
        'overflowY': 'auto', 'backgroundColor': '#f9f9f9', 'borderRadius': '10px',
        'display': 'flex', 'flexDirection': 'column', 'gap': '10px'
    }),
    
    # Input and button
    dcc.Textarea(id='user-input', placeholder='Ask me anything...', 
                 style={'width': '100%', 'height': 80}),
    html.Button('Send', id='submit-btn', n_clicks=0, className='btn btn-primary', style={'marginTop': '10px'}),

    # Store chat history
    dcc.Store(id='chat-history', data=[])
])

# Callback to handle user input and maintain chat history
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

    # Append user input to history
    chat_history.append({"role": "user", "content": user_input})

    # Create message history including system prompt
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    # Append AI response to history
    bot_response = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": bot_response})

    # ✅ Initialize chat_display as a list
    chat_display = []

    # Format chat history for display with chat bubbles
    for msg in chat_history:
        if msg["role"] == "user":
            chat_display.append(html.Div([
                html.B("You: "),  # Bold label
                html.Span(msg["content"])  # Normal text
            ], className="user-bubble"))
        elif msg["role"] == "assistant":
            chat_display.append(html.Div([
                html.B("Kitchen Aid: "),  # Bold label
                html.Span(msg["content"])  # Normal text
            ], className="assistant-bubble"))

    return chat_display, chat_history
