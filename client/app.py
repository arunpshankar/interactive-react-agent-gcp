import streamlit as st
import requests
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the API URL of your agent service
# AGENT_API_URL = 'https://react-agent-service-390991481152.us-central1.run.app/api/agent'
AGENT_API_URL = 'http://localhost:8080/api/agent'

# Streamlit UI setup
st.set_page_config(page_title="Agent Chat Interface", page_icon="💬", layout="wide")

# Apply custom CSS styles
def apply_custom_styles():
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Set background color */
        body {
            background-color: #f0f2f6;
        }

        .user-message {
            background-color: #cfe9ba;
            border-radius: 15px;
            padding: 10px;
            margin: 10px 0;
            max-width: 70%;
            align-self: flex-end;
            color: black;
            display: inline-block;
            word-wrap: break-word;
        }

        .agent-message {
            background-color: #e5e5ea;
            border-radius: 15px;
            padding: 10px;
            margin: 10px 0;
            max-width: 70%;
            align-self: flex-start;
            color: black;
            display: inline-block;
            word-wrap: break-word;
        }

        .message-container {
            display: flex;
            flex-direction: column;
            margin-bottom: 50px;
        }

        .sidebar .sidebar-content {
            background-color: #ffffff;
        }

        .trace-step {
            background-color: #f9f9f9;
            border-left: 4px solid #6c6c6c;
            padding: 10px;
            margin: 10px 0;
        }

        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
        }

        @import url('https://fonts.googleapis.com/css2?family=Open+Sans&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Open Sans', sans-serif;
        }

        .history-entry {
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 10px;
            background-color: #fff;
            border-radius: 5px;
            font-size: 12px;
        }
        .history-entry h4 {
            margin: 0 0 5px 0;
            font-size: 13px;
        }
        .history-entry p {
            margin: 0;
            color: #333;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_styles()

# Initialize conversation history in session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
    st.session_state.latest_user_message = None
    st.session_state.latest_agent_response = None
    st.session_state.latest_trace = None

# Function to send query to the agent API and retrieve the response
def get_agent_response(user_message):
    payload = {'query': user_message, 'conversation': st.session_state.conversation_history}

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

# Function to remove "Final Answer:" prefix from response
def clean_final_answer(answer):
    return answer.replace("Final Answer: ", "")

# Function to display the agent's thought process
def display_trace(trace):
    if trace:
        st.markdown("<h3 style='margin-top: 40px;'>Agent's Thought Process</h3>", unsafe_allow_html=True)
        for idx, msg in enumerate(trace, start=1):
            content = msg.get('thought') or msg.get('content') or msg.get('text') or str(msg)
            st.markdown(f"<div class='trace-step'><strong>Step {idx}:</strong> {content}</div>", unsafe_allow_html=True)

# Sidebar for conversation history and clear option
with st.sidebar:
    st.header("Conversation History")
    if st.session_state.conversation_history:
        exchanges = []
        exchange = {}
        for message in st.session_state.conversation_history:
            if message['role'] == 'user':
                if 'user' in exchange:
                    exchanges.append(exchange)
                    exchange = {}
                exchange['user'] = message['content']
            elif message['role'] == 'assistant':
                exchange['assistant'] = message['content']
                exchanges.append(exchange)
                exchange = {}
        if exchange:
            exchanges.append(exchange)

        for idx, ex in enumerate(exchanges):
            st.markdown(f"""
            <div class='history-entry'>
                <h4>Exchange {idx + 1}</h4>
                <p><strong>You:</strong> {ex.get('user', '')}</p>
                <p><strong>Agent:</strong> {ex.get('assistant', '')}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No conversation history yet.")

    if st.button("Clear Conversation"):
        st.session_state.conversation_history = []
        st.session_state.latest_user_message = None
        st.session_state.latest_agent_response = None
        st.session_state.latest_trace = None
        st.experimental_rerun()

# Main content area
st.markdown("<h1 style='text-align: center;'>💬 Talk to Agent</h1>", unsafe_allow_html=True)
st.write("Welcome! Type your query below and interact with the agent.")

# Get user input using st.form with clear_on_submit=True
with st.form(key='user_input_form', clear_on_submit=True):
    user_message = st.text_input("Type your message here:")
    submit_button = st.form_submit_button(label='Send')

# Process the user input when the form is submitted
if submit_button and user_message:
    st.session_state.conversation_history.append({'role': 'user', 'content': user_message})
    
    st.markdown(f"<div class='user-message'>{user_message}</div>", unsafe_allow_html=True)

    # Show loading animation
    with st.spinner("Processing your query..."):
        data = get_agent_response(user_message)
        time.sleep(1)  # Optional delay to emphasize the animation

    if data:
        final_answer = clean_final_answer(data.get('final_answer', 'No answer available.'))
        trace = data.get('trace', [])

        st.session_state.conversation_history.append({'role': 'assistant', 'content': final_answer})

        st.markdown(f"<div class='agent-message'>{final_answer}</div>", unsafe_allow_html=True)
        display_trace(trace)
    else:
        error_message = 'Failed to get response from agent.'
        st.session_state.conversation_history.append({'role': 'assistant', 'content': error_message})
        st.markdown(f"<div class='agent-message'>{error_message}</div>", unsafe_allow_html=True)
