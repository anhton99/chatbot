import openai
import os
from dotenv import load_dotenv
import streamlit as st

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
        
    user_input = st.text_area("Enter your question here: ")
    if moderation(user_input):
        raise Exception("Moderation check: usage policy violated.")
    res = reply(user_input, history)
    st.session_state.questions.append(user_input)
    st.session_state.answers.append(res)  

    if st.session_state['answers']:
        for i in range(1, len(st.session_state['answers'])):
            st.markdown('You: ' + st.session_state['questions'][i])
            st.markdown('ChatGPT: ' + st.session_state['answers'][i])  

if __name__ == '__main__':
    st.markdown('### Hi this is cool')
    chat() 
