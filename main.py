import openai
import os
from dotenv import load_dotenv

load_dotenv('.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

def reply(user_input):
    if not user_input:
        return "Please provide a valid input."
    try: 
        res = openai.Completion.create(
            model = "text-davinci-003",
            prompt = user_input,
            max_tokens = 100,
            temperature = 0.01
        ).choices[0].text.strip()
        return res
    except Exception as e:
        return "An error occurred: " + str(e)
    

def main():

    print("Welcome to the Chatbot. Ask me anything or type #quit to exit")
    
    while True:
        user_input = input("You: ")
        if user_input == '#quit':
            break
        
        print("Chatbot:", reply(user_input))

if __name__ == '__main__':
    main()


