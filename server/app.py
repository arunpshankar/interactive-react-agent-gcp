from vertexai.generative_models import GenerativeModel
from src.tools.serp import search as google_search
from src.tools.wiki import search as wiki_search
from src.config.logging import logger
from src.config.setup import config
from src.react.agent import Agent
from src.react.agent import Name 
from flask import jsonify
from flask import request
from flask import Flask
import json


app = Flask(__name__)

# Initialize the gemini model globally to avoid reloading it for every request
gemini = GenerativeModel(config.MODEL_NAME)

def parse_thought_content(content):
    """
    Extract JSON-like part from content surrounded by ```json``` and convert it to a dictionary.
    """
    try:
        # Check if content includes ```json``` markers
        if "```json" in content:
            # Strip out 'Thought: ' prefix and extract the JSON string
            json_str = content.split("```json", 1)[1].split("```")[0].strip()
            thought_dict = json.loads(json_str)  # Convert JSON string to dictionary
            return thought_dict
        else:
            # If no ```json``` markers are present, try to parse the content after "Thought: "
            json_str = content.split("Thought: ", 1)[1].strip()
            thought_dict = json.loads(json_str)
            return thought_dict
    except (IndexError, json.JSONDecodeError) as e:
        logger.error(f"Error parsing thought content: {e}")
        return content  # Return the original content if parsing fails


@app.route('/api/agent', methods=['POST'])
def agent_api():
    data = request.get_json()
    query = data.get('query', '')
    logger.info(f'Incoming User Query: {query}')
    if not query:
        return jsonify({'error': 'Query is required'}), 400

    # Initialize the agent for each request to reset its state
    agent = Agent(model=gemini)
    agent.register(Name.WIKIPEDIA, wiki_search)
    agent.register(Name.GOOGLE, google_search)

    # Execute the agent
    final_answer = agent.execute(query)

    # Process the trace
    trace = []
    for message in agent.messages:
        if message.content.startswith('Thought:'):
            thought_content = parse_thought_content(message.content)
            trace.append(thought_content)

    # Prepare the response
    response = {
        'final_answer': final_answer,
        'trace': trace
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
