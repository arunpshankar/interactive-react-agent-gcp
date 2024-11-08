
from vertexai.generative_models import GenerativeModel
from src.tools.serp import search as google_search
from src.tools.wiki import search as wiki_search
from src.config.logging import logger
from src.config.setup import config
from flask import jsonify 
from flask import request
from flask import Flask


app = Flask(__name__)

# Initialize the agent globally
gemini = GenerativeModel(config.MODEL_NAME)
agent = Agent(model=gemini)
agent.register(Name.WIKIPEDIA, wiki_search)
agent.register(Name.GOOGLE, google_search)


@app.route('/api/agent', methods=['POST'])
def agent_api():
    data = request.get_json()
    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'Query is required'}), 400

    # Execute the agent
    final_answer = agent.execute(query)

    # Prepare the response, including the trace
    response = {
        'final_answer': final_answer,
        'trace': [message.dict() for message in agent.messages]
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
