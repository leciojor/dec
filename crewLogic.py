import logging
from crewai import Agent, Task
from textwrap import dedent
from langchain_community.llms import Ollama


logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
    datefmt='%Y-%m-%d %H:%M:%S', 
    handlers=[
        logging.FileHandler("log.txt"),  
        logging.StreamHandler()  
    ]
    )



def defineTeamAgents(self, role="", goal="", backstory="", tools=[], temperature = 0.8):
    logging.info(f"Defining team agent with role: {role}")
    return Agent(
        role=role,
        goal=dedent(goal),
        backstory=dedent(backstory),
        tools=tools,
        allow_delegation=False,
        llm=Ollama(model="wizardml2:latest", base_url="http://localhost:11434/", temperature=temperature),
        verbose=True,
    )



def taskDefinition(self, agent, goal = "", expected_output ="", context = ""):
    return Task(description=dedent(f"""\
        Do the following: {goal}.

        """),
        expected_output=expected_output,
        agent=agent,
        context=context
    )