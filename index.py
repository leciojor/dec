import streamlit as st
from streamlit import session_state as state
import logging
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

def messageRegister(llm):
    logging.info(f'User input: {state["user_input"]} initiated')
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


def beggining():
    state['initiate'] = False

def restart():
    for key, value in state.items():
        state.pop(key)
    st.rerun() 

def main():

    logging.info('Rerun')

    st.title("Projeto DECI")

    if 'user_input' not in state:
        state['user_input'] = ''
    if 'llm' not in state:
        state['llm'] = Ollama(model="wizardlm2:latest")
    if 'initiate' not in state:
        state['initiate'] = True
    if 'response' not in state:
        state['response'] = ''
    if 'resumo' not in state:
        state['resumo'] = False
    if 'math' not in state:
        state['math'] = False
    if 'arquivo' not in state:
        state['arquivo'] = False
    if 'image' not in state:
        state['image'] = False


    if state['initiate']:
        col1, col2, col3, col4 = st.columns(4)
        state['resumo'] = col1.button('RESUMO DA INTERNET', on_click = beggining)
        state['math'] = col2.button('MODELO PARA MATEMATICA', on_click = beggining)
        state['arquivo'] = col3.button('GERADOR DE ARQUIVO', on_click = beggining)
        state['image'] = col4.button('LEITOR DE IMAGEM', on_click = beggining)

        try:
            chattingBox(state['llm'])
        except Exception as e:
            st.error(f'Error when generating chatbox: {e}')
            logging.error(f'Error when generating chatbox: {e}')
    
    nextStatesCheck()




def nextStatesCheck():
    st.button('VOLTAR', on_click = restart) 
    if state['resumo']:
        resumo()
    if state['math']:
        math()
    if state['arquivo']:
        arquivo()
    if state['image']:
        imagem()


def resumo():
    pass

def math():
    pass

def arquivo():
    pass

def imagem():
    pass
    

if __name__ == "__main__":
    main()
