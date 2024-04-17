import os
import openai
from dotenv import load_dotenv

load_dotenv('.env')
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_response(user_input, conversation_history):
    message = conversation_history + [{"role": "user", "content": user_input}]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message
    )
    # print(completion)
    response = completion.choices[0].message.content
    conversation_history = message + [{"role": "assistant", "content": response}]
    return response, message
