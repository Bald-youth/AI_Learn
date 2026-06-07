import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def chat_with_ai(question):
    response = client.chat.completions.create(
        model="gui-plus-2026-02-26",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )
    answer = response.choices[0].message.content
    return answer
if __name__ == '__main__':
    st.title("AI ChatBot")
    question = st.text_input("请输入问题：")
    if question:
       answer = chat_with_ai(question)
       st.write("AI：", answer)