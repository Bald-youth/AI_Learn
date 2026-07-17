
from config import client

def chat_with_ai(messages):
    responses = client.chat.completions.create(
        model="qwen-plus",
        messages=messages
    )
    return responses.choices[0].message.content

