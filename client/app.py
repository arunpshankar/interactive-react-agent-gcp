import chainlit as cl
import requests

# Set the URL of your deployed agent service
AGENT_API_URL = 'http://localhost:8080/api/agent'

@cl.on_message
async def main(message: cl.Message):
    # Convert `message` to a string using its content attribute
    user_message = message.content if hasattr(message, 'content') else str(message)

    # Retrieve conversation history from session state
    conversation_history = cl.user_session.get('history', [])
    # Add the latest user message to the conversation history
    conversation_history.append({'role': 'user', 'content': user_message})

    # Prepare the JSON data payload
    payload = {
        'query': user_message,
        'conversation': conversation_history
    }
    
    # Debugging: Print the payload to confirm its format
    print("Sending payload:", payload)

    # Send the query to the agent API
    try:
        response = requests.post(
            AGENT_API_URL,
            json=payload,
            timeout=30  # Set a timeout for the request
        )
        response.raise_for_status()  # Check for HTTP request errors
    except requests.exceptions.RequestException as e:
        await cl.Message(content="Failed to connect to the agent service. Please try again later.").send()
        return

    # Parse the response JSON
    data = response.json()
    final_answer = data.get('final_answer', 'No answer available.')
    trace = data.get('trace', [])

    # Display the agent's final answer
    await cl.Message(content=final_answer).send()

    # Save the assistant's response in the conversation history
    conversation_history.append({'role': 'assistant', 'content': final_answer})

    # Update the session state with the new conversation history
    cl.user_session.set('history', conversation_history)

    # Optionally, display the agent's thought process
    if trace:
        thought_messages = []
        for msg in trace:
            role = msg.get('role', 'Agent')
            content = msg.get('content', '')
            thought_messages.append(f"**{role.capitalize()}**: {content}")

        thought_process = "\n\n".join(thought_messages)
        await cl.Message(content=thought_process, author="Agent's Thought Process").send()
