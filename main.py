import openai
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv('.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

def reply(user_input):
    if not user_input:
        return "Error: input can't be empty"
    try: 
        res = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-0301",
            messages = [{"role": "user", "content": user_input}]
        ).choices[0].message.content.strip()
        return res
    except Exception as e:
        return "Error: " + str(e)
    

def main():

    st.title("Chatbot with Streamlit")
    st.markdown("Welcome to the Chatbot. Ask me anything!")

    user_input = st.text_input("You:")
    if st.button("Send"):
        response = reply(user_input)
        st.text("Chatbot: " + response)


    print("Welcome to the Chatbot. Ask me anything or type #quit to exit")

if __name__ == '__main__':
    main()