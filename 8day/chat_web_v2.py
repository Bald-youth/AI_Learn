# 导入 Streamlit，用来开发网页界面
import streamlit as st

# 从 .env 文件读取环境变量
from dotenv import load_dotenv

# OpenAI SDK（阿里百炼兼容 OpenAI SDK）
from openai import OpenAI

# Python内置模块，用来读取环境变量
import os


# ==========================
# 系统角色（Prompt）
# ==========================
# 告诉 AI 自己是谁、应该如何回答
SYSTEM_PROMPT = """
你是一名资深 Python 和 AI 应用开发导师，
请用简洁、清晰、鼓励但不啰嗦的方式回答用户。
"""


# ==========================
# 加载 .env 配置文件
# ==========================
load_dotenv()


# ==========================
# 创建 AI 客户端
# ==========================
client = OpenAI(
    # 从 .env 中读取 API Key
    api_key=os.getenv("DASHSCOPE_API_KEY"),

    # 阿里百炼兼容 OpenAI 接口
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


# ==========================
# 调用 AI
# ==========================
def chat_with_ai(messages):
    """
    发送消息给 AI
    返回 AI 的回答
    """

    response = client.chat.completions.create(

        # 使用的模型
        model="qwen-plus",

        # 历史聊天记录
        messages=messages
    )

    # 返回 AI 回答内容
    return response.choices[0].message.content


# ==========================
# 生成聊天记录文本
# ==========================
def build_chat_history_text(messages):
    """
    把聊天记录转换成文本
    用于下载 txt 文件
    """

    history = ""

    for message in messages:

        # 跳过系统角色
        if message["role"] == "system":
            continue

        # 用户消息
        if message["role"] == "user":
            history += f"用户：{message['content']}\n"

        # AI消息
        elif message["role"] == "assistant":
            history += f"AI：{message['content']}\n"

        history += "-" * 50 + "\n"

    return history


# ==========================
# 页面标题
# ==========================
st.title("AI ChatBot V2")


# ==========================
# 初始化聊天记录
# ==========================
# 第一次进入页面时执行
if "messages" not in st.session_state:

    st.session_state.messages = [

        {
            "role": "system",

            # 给 AI 设置身份
            "content": SYSTEM_PROMPT
        }
    ]


# ==========================
# 左侧边栏
# ==========================
st.sidebar.title("统计信息")


# ==========================
# 统计消息数量
# ==========================
chat_message_count = len(

    [
        message
        for message in st.session_state.messages

        # 不统计 system
        if message["role"] != "system"
    ]
)


# ==========================
# 统计会话轮数
# ==========================
# user + assistant = 一轮
chat_round_count = chat_message_count // 2


st.sidebar.write(
    f"消息数：{chat_message_count}"
)

st.sidebar.write(
    f"会话轮数：{chat_round_count}"
)


# ==========================
# 下载聊天记录
# ==========================
chat_history_text = build_chat_history_text(
    st.session_state.messages
)

st.sidebar.download_button(

    # 按钮名称
    label="下载聊天记录",

    # 下载内容
    data=chat_history_text,

    # 文件名
    file_name="chat_history.txt",

    # 文件类型
    mime="text/plain"
)


# ==========================
# 清空聊天按钮
# ==========================
if st.sidebar.button("清除"):

    # 重置聊天记录
    st.session_state.messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # 刷新页面
    st.rerun()


# ==========================
# 显示聊天记录
# ==========================
for message in st.session_state.messages:

    # 不显示系统消息
    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):

        # markdown支持代码高亮
        st.markdown(message["content"])


# ==========================
# 输入框
# ==========================
prompt = st.chat_input("请输入问题")


# ==========================
# 用户发送消息
# ==========================
if prompt:

    # 保存用户消息
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # 调用 AI
    answer = chat_with_ai(
        st.session_state.messages
    )

    # 保存 AI 回复
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # 刷新页面
    st.rerun()