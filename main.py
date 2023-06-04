import openai
import os
from dotenv import load_dotenv
import streamlit as st
# import component.src.streamlit_component_x as cp

load_dotenv('.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

SYSTEM_PROMPT = "You are a helpful assistant."

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def chat():
    def moderation(user_input):
        return openai.Moderation.create(input=user_input).results[0].flagged
    
    def reply(user_input, history):

        if history:
            for i in reversed(range(len(history))):
                messages.append({"role": "user", "content": history[i][0]}) 
                messages.append({"role": "assistant", "content": history[i][1]}) 

        messages.append({"role": "user", "content": user_input})
        

        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = messages,
        ).choices[0].message.content

        messages.append({"role": "assistant", "content": res})

        return res
    
    if 'questions' not in st.session_state:
        st.session_state['questions'] = []
    
    if 'answers' not in st.session_state:
        st.session_state['answers'] = []

    history = []
    i = 0 
    while i < len(st.session_state['questions']):
        history.append((st.session_state['questions'][i], 
                        st.session_state['answers'][i]))
        i += 1 

    # --- draft ---
    # components.html(open('./frontend/index.html', 'r', encoding='utf-8').read(), height=800)
    # --- draft ---

    if 'text' not in st.session_state:
        st.session_state['text'] = ''

    if 'text_captured' not in st.session_state:
        st.session_state['text_captured'] = ''

    def submit():
        st.session_state['text_captured'] = st.session_state['text']
        st.session_state['text'] = ''

        
    # st.text_area(label="Enter your question here: ", key="text", on_change=submit)
    user_input = st.session_state['text_captured']
    if moderation(user_input):
        raise Exception("Moderation check: usage policy violated.")
    res = reply(user_input, history)


    st.session_state.questions.append(user_input)
    st.session_state.answers.append(res)  

    if st.session_state['answers']:
        for i in range(1, len(st.session_state['answers'])):
            you = st.session_state['questions'][i]
            chatbot = st.session_state['answers'][i]
            st.write(f"<span style='background-color: #5d5cde; color: #fff; border-radius: 0.5rem; padding: 0.6rem; text-align: right; float: right; max-width: 80%'> {you} </span>", unsafe_allow_html=True)
            st.write(f"<span style='background-color: #f1f2f2; color: #181818; border-radius: 0.5rem; padding: 0.6rem; text-align: left; float: left; max-width: 80%'> {chatbot} </span>", unsafe_allow_html=True)

    st.text_area(label="Enter your question here: ", key="text", on_change=submit)

if __name__ == '__main__':
    # value = cp.streamlit_component_x(label="This is a label!")
    # st.write(value)

    chat() 

# current limit: server and client nhap vao mot cho 
# chua co mo hinh server, authentication, etc. 
# debug w vscode - breakpoint, 

# python3 -m streamlit run main.py

# export PYTHONPATH=/Users/anhton99/chatbot/component
