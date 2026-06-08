import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import os

SYSTEM_PROMPT = "你是一名资深 Python 和 AI 应用开发导师，请用简洁、清晰、鼓励但不啰嗦的方式回答用户。"
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def chat_with_ai(messages):

    response = client.chat.completions.create(
        model="qwen-plus",
        messages=messages
    )

    return response.choices[0].message.content

def build_chat_history_text(messages):
    history = ""
    for messages in messages:
        if messages['role'] == "system":
           continue
        if messages['role'] == "user":
            history += f"用户：{messages['content']}\n"
        elif messages['role'] == "assistant":
            history += f"AI：{messages['content']}\n"
        history+="-" *50 + "\n"

    return history

st.title("AI ChatBot V2")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

st.sidebar.title("统计信息")
chat_count = len([
    m for m in st.session_state.messages
    if m["role"] != "system"
])
st.sidebar.write(f"会话轮数：{chat_count}")
chat_history_text = build_chat_history_text(st.session_state.messages)

st.sidebar.download_button(
    label="下载聊天记录",
    data=chat_history_text,
    file_name="chat_history.txt",
    mime="text/plain"
)

if st.sidebar.button("清除"):
    st.session_state.messages = [{
        "role": "system",
        "content": "你是一名资深 Python 和 AI 应用开发导师，请用简洁、清晰、鼓励但不啰嗦的方式回答用户。"
    }]
    st.rerun()



for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("请输入问题")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    answer = chat_with_ai(st.session_state.messages)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()


