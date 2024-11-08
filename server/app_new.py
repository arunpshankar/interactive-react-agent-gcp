
from vertexai.generative_models import GenerativeModel 
from src.react.agent import Agent, Name 
from src.config.setup import config
from src.tools.wiki import search as wiki_search
from src.tools.serp import search as google_search



query = "What is the age of the oldest tree in the country that has won the most FIFA World Cup titles?"


gemini = GenerativeModel(config.MODEL_NAME)

agent = Agent(model=gemini)
agent.register(Name.WIKIPEDIA, wiki_search)
agent.register(Name.GOOGLE, google_search)

answer = agent.execute(query)









