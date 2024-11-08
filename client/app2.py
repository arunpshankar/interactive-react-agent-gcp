import streamlit as st
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the API URL of your agent service
AGENT_API_URL = 'http://localhost:8080/api/agent'

# Streamlit UI setup
st.set_page_config(page_title="Agent Chat Interface", page_icon="💬", layout="wide")

# Apply custom CSS styles
def apply_custom_styles():
    st.markdown("""
        <style>
        /* Hide Streamlit's default header and footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Set background color */
        body {
            background-color: #f0f2f6;
        }

        /* Style the chat container */
        .chat-container {
            max-width: 800px;
            margin: auto;
            padding: 20px;
        }

        /* Style for user messages */
        .user-message {
            background-color: #cfe9ba;
            border-radius: 15px;
            padding: 10px;
            margin: 5px 0;
            max-width: 70%;
            align-self: flex-end;
            color: black;
            display: inline-block;
            word-wrap: break-word;
        }

        /* Style for agent messages */
        .agent-message {
            background-color: #e5e5ea;
            border-radius: 15px;
            padding: 10px;
            margin: 5px 0;
            max-width: 70%;
            align-self: flex-start;
            color: black;
            display: inline-block;
            word-wrap: break-word;
        }

        /* Style for the message bubble container */
        .message-container {
            display: flex;
            flex-direction: column;
            margin-bottom: 50px;
        }

        /* Style for the sidebar */
        .sidebar .sidebar-content {
            background-color: #ffffff;
        }

        /* Style for trace steps */
        .trace-step {
            background-color: #f9f9f9;
            border-left: 4px solid #6c6c6c;
            padding: 10px;
            margin: 10px 0;
        }

        /* Style for buttons */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
        }

        /* Custom font */
        @import url('https://fonts.googleapis.com/css2?family=Open+Sans&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Open Sans', sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_styles()

# Initialize conversation history in session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Function to send query to the agent API and retrieve the response
def get_agent_response(user_message):
    # Prepare the payload for the agent API request
    payload = {
        'query': user_message,
        'conversation': st.session_state.conversation_history
    }

    # Send request to agent API and handle errors
    try:
        response = requests.post(AGENT_API_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        logging.info("Received response from agent service.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to connect to the agent service: {e}")
        st.error("Failed to connect to the agent service. Please try again later.")
        return None

    return data

# Sidebar for conversation history and clear option
with st.sidebar:
    st.header("Conversation History")
    if st.session_state.conversation_history:
        for i, message in enumerate(st.session_state.conversation_history):
            if message['role'] == 'user':
                st.markdown(f"**You:** {message['content']}")
            elif message['role'] == 'assistant':
                st.markdown(f"**Agent:** {message['content']}")
    else:
        st.write("No conversation history yet.")

    # Add a button to clear the conversation history
    if st.button("Clear Conversation"):
        st.session_state.conversation_history = []
        st.experimental_rerun()

# Main content area
st.markdown("<h1 style='text-align: center;'>💬 Professional Chat Interface with Agent</h1>", unsafe_allow_html=True)
st.write("Welcome! Type your query below and interact with the agent.")

# Container for the chat messages
with st.container():
    # Display the conversation history in the main area
    for message in st.session_state.conversation_history:
        if message['role'] == 'user':
            st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
        elif message['role'] == 'assistant':
            st.markdown(f"<div class='agent-message'>{message['content']}</div>", unsafe_allow_html=True)

# Function to display the agent's thought process
def display_trace(trace):
    if trace:
        st.markdown("<h3 style='margin-top: 40px;'>Agent's Thought Process</h3>", unsafe_allow_html=True)
        for idx, msg in enumerate(trace, start=1):
            # Handle different possible formats of trace messages
            if isinstance(msg, dict):
                content = msg.get('thought') or msg.get('content') or msg.get('text') or str(msg)
            else:
                content = str(msg)
            st.markdown(f"<div class='trace-step'><strong>Step {idx}:</strong> {content}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<h3>Agent's Thought Process</h3>", unsafe_allow_html=True)
        st.info("No additional details available.")

# Get user input using st.form with clear_on_submit=True
with st.form(key='user_input_form', clear_on_submit=True):
    user_message = st.text_input("Type your message here:")
    submit_button = st.form_submit_button(label='Send')

# Process the user input when the form is submitted
if submit_button and user_message:
    # Add user message to the conversation history
    st.session_state.conversation_history.append({'role': 'user', 'content': user_message})

    # Display the user's message
    st.markdown(f"<div class='user-message'>{user_message}</div>", unsafe_allow_html=True)

    # Get the response from the agent
    data = get_agent_response(user_message)
    if data:
        final_answer = data.get('final_answer', 'No answer available.')
        trace = data.get('trace', [])

        # Add agent's response to the conversation history
        st.session_state.conversation_history.append({'role': 'assistant', 'content': final_answer})

        # Display agent's response
        st.markdown(f"<div class='agent-message'>{final_answer}</div>", unsafe_allow_html=True)

        # Display the agent's thought process
        display_trace(trace)
    else:
        # Add error message to conversation history
        error_message = 'Failed to get response from agent.'
        st.session_state.conversation_history.append({'role': 'assistant', 'content': error_message})
        st.markdown(f"<div class='agent-message'>{error_message}</div>", unsafe_allow_html=True)
