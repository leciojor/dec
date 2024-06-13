import streamlit as st
from streamlit import session_state as state
import logging
from langchain_community.chat_models import ChatOllama

def main():
    logging.basicConfig(filename='log.txt', level=logging.INFO)

    st.title("D.E.C.")
    llm = ChatOllama(model="wizardml2", base_url="http://localhost:11434/")

    if 'user_input' not in st.session_state:
        state['user_input'] = ''
    if 'initiate' not in st.session_state:
        state['initiate'] = False
    if 'response' not in st.session_state:
        state['response'] = ''

        
    state['user_input'] = st.text_input("PERGUNTE O QUE QUISER: ")
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
