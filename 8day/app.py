import streamlit as st
from config import SYSTEM_PROMPT
from ai import chat_with_ai
from utils import build_chat_history_text


# ==========================
# 页面配置
# ==========================
st.set_page_config(
    page_title="AI ChatBot",
    page_icon="🤖"
)

st.title("🤖 AI ChatBot")

# ==========================
# 初始化聊天记录
# ==========================
DEFAULT_MESSAGES = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]
if "messages" not in st.session_state:
    st.session_state.messages = DEFAULT_MESSAGES.copy()

# ==========================
# 侧边栏
# ==========================
with st.sidebar:

    st.header("📊 统计信息")

    chat_message_count = len(
        [
            message
            for message in st.session_state.messages
            if message["role"] != "system"
        ]
    )

    st.write(f"消息数：{chat_message_count}")
    st.write(f"对话轮数：{chat_message_count // 2}")

    history_text = build_chat_history_text(st.session_state.messages)

    st.download_button(
        "📥 下载聊天记录",
        history_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )

    if st.button("🗑️ 清空聊天记录"):

        st.session_state.messages = DEFAULT_MESSAGES.copy()

        st.rerun()

# ==========================
# 显示聊天记录
# ==========================
for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================
# 用户输入
# ==========================
question = st.chat_input("请输入问题...")

if question:

    # 保存用户消息
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
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

    st.rerun()