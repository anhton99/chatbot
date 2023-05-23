import openai
import os
from dotenv import load_dotenv
import streamlit as st
from streamlit_chat import message

load_dotenv('.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

# Source: https://github.com/JamesTheHacker/profanity-bash/blob/master/banned_words.txt 
banned = {}
with open("profanity.txt") as f:
    for line in f:
        banned[line] = ''

def chat():

    def profanity_check(user_input):
        lst = user_input.split(" ")
        for word in lst: 
            if word in banned: 
                return False 
        return True 

    def reply(user_input):
        if profanity_check(user_input):
            raise Exception("Profanity detected. Please be kind :)")
        try: 
            res = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo-0301",
                messages = [{"role": "user", "content": user_input}]
            ).choices[0].message.content.strip()
            return res
        except Exception as e:
            return "Error: " + str(e)

    if 'answers' not in st.session_state:
        st.session_state['answers'] = []
    if 'questions' not in st.session_state:
        st.session_state['questions'] = []
    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = ''

    user_input = st.text_input("Enter your question here", key = 'input1')
    if user_input:
        res = reply(user_input)
        st.session_state.questions.append(user_input)
        st.session_state.answers.append(res)  


    if st.session_state['answers']:
        for i in range(len(st.session_state.answers)):
            message(st.session_state.questions[i], is_user=True, key=str(i) + '_user')
            message(st.session_state.answers[i], key=str(i))  


if __name__ == '__main__':
    st.title("Chatbot with Streamlit")
    st.markdown("Welcome to the Chatbot. Ask me anything and Hit 'Enter' to submit.") 

    chat() 