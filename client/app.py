import chainlit as cl
import requests


# Set the URL of your deployed agent service
AGENT_API_URL = 'https://react-agent-service-xxxxxxxxxx-uc.a.run.app/api/agent'

@cl.on_message
async def main(message: str):
    # Retrieve conversation history from session state
    conversation_history = cl.user_session.get('history', [])
    # Add the latest user message to the conversation history
    conversation_history.append({'role': 'user', 'content': message})

    # Send the query to the agent API
    try:
        response = requests.post(
            AGENT_API_URL,
            json={
                'query': message,
                'conversation': conversation_history
            },
            timeout=30  # Set a timeout for the request
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        await cl.Message(content="Failed to connect to the agent service. Please try again later.").send()
        return

    data = response.json()
    final_answer = data.get('final_answer', '')
    trace = data.get('trace', [])

    # Display the agent's final answer
    await cl.Message(content=final_answer).send()

    # Save the assistant's response in the conversation history
    conversation_history.append({'role': 'assistant', 'content': final_answer})

    # Update the session state with the new conversation history
    cl.user_session['history'] = conversation_history

    # Optionally, display the agent's thought process
    thought_messages = []
    for msg in trace:
        role = msg['role']
        content = msg['content']
        thought_messages.append(f"**{role.capitalize()}**: {content}")

    thought_process = "\n\n".join(thought_messages)
    await cl.Message(content=thought_process, author="Agent's Thought Process").send()
