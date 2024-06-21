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


def chattingBox(input, response, llm):
    if "messages" not in state:
        state['messages'] = []

    for message in state['messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(input):
        state['messages'].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            # chat_model_response = llm.invoke(state['user_input'])
            chat_model_response = 'test'
            response = st.markdown(chat_model_response)
    state['messages'].append({"role": "assistant", "content": response})



def main():
    logging.basicConfig(filename='log.txt', level=logging.INFO)

    st.title("Projeto DECI")

    llm = ChatOllama(model="wizardml2", base_url="http://localhost:11434/")

    if 'user_input' not in state:
        state['user_input'] = ''
    if 'initiate' not in state:
        state['initiate'] = False
    if 'response' not in state:
        state['response'] = ''

    if not state['initiate']:
        state['user_input'] = st.text_input("REVELE SEUS DESEJOS: ")
        state['initiate'] = st.button('Iniciar')


    if state['initiate']:
        logging.info(f'User input: {state["user_input"]} initiated')

        try:
            chattingBox(state['user_input'], state['response'], llm)
        except Exception as e:
            st.error(f'Error when generating chatbox: {e}')
            logging.error(f'Error when generating chatbox: {e}')

if __name__ == "__main__":
    main()
