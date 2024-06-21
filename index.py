import streamlit as st
from streamlit import session_state as state
import logging
from langchain_community.chat_models import ChatOllama
from crewai import Agent, Task
from textwrap import dedent


def defineTeamAgents(self, role="", goal="", backstory="", tools=[], temperature = 0.8):
        logging.info(f"Defining team agent with role: {role}")
        return Agent(
            role=role,
            goal=dedent(goal),
            backstory=dedent(backstory),
            tools=tools,
            allow_delegation=False,
            llm=ChatOllama(model="wizardml2", base_url="http://localhost:11434/", temperature=temperature),
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


def main():
    logging.basicConfig(filename='log.txt', level=logging.INFO)

    st.title("Projeto DECI")

    llm = ChatOllama(model="wizardml2", base_url="http://localhost:11434/")

    if 'user_input' not in st.session_state:
        state['user_input'] = ''
    if 'initiate' not in st.session_state:
        state['initiate'] = False
    if 'response' not in st.session_state:
        state['response'] = ''

    state['user_input'] = st.text_input("REVELE SEUS DESEJOS: ")
    state['initiate'] = st.button('Iniciar')

    if state['initiate']:
        logging.info(f'User input: {state["user_input"]} initiated')
        try:

            chat_model_response = llm.invoke(state['user_input'])
            st.success(chat_model_response)

        except Exception as e:
            st.error(e)
            logging.error(f'Error when generating answer: {e}')

if __name__ == "__main__":
    main()
