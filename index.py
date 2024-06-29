import streamlit as st
from streamlit import session_state as state
import logging
from langchain_community.llms import Ollama
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


def messageRegister(llm):
    state['messages'].append({"role": "user", "content": state['user_input']})
    with st.chat_message("user"):
        st.markdown(state['user_input'])
    with st.chat_message("assistant"):
        state['response'] = llm.invoke(state['user_input'])
        st.markdown(state['response'])
        logging.info(f'Model response: {state["response"]} for input: {state["user_input"]}')
    state['messages'].append({"role": "assistant", "content": state['response']})


def chattingBox(llm):
    if "messages" not in state:
        state['messages'] = []

    for message in state['messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if input := st.chat_input("REVELE SEUS DESEJOS: "):
        state['user_input'] = input
        messageRegister(llm)



def main():
    logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
    datefmt='%Y-%m-%d %H:%M:%S', 
    handlers=[
        logging.FileHandler("log.txt"),  
        logging.StreamHandler()  
    ]
    )

    logging.info('Rerun')

    st.title("Projeto DECI")

    if 'user_input' not in state:
        state['user_input'] = ''
    if 'llm' not in state:
        state['llm'] =Ollama(model="wizardlm2:latest")
    if 'initiate' not in state:
        state['initiate'] = False
    if 'response' not in state:
        state['response'] = ''


    if not state['initiate']:
        state['initiate'] = st.button('INICIAR')


    if state['initiate']:
        logging.info(f'User input: {state["user_input"]} initiated')

        try:
            chattingBox(state['llm'])
        except Exception as e:
            st.error(f'Error when generating chatbox: {e}')
            logging.error(f'Error when generating chatbox: {e}')

if __name__ == "__main__":
    main()
