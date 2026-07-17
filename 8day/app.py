import streamlit as st
from ai import chat_with_ai
from utils import build_chat_history_text
from prompts import ROLE_PROMPTS

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
def create_default_messages(system_prompt):
    return [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

# ==========================
# 选择AI角色
# ==========================
role = st.sidebar.selectbox(
    "请选择AI角色",
    list(ROLE_PROMPTS.keys())
)

st.sidebar.success(f"当前角色：{role}")
system_prompt = ROLE_PROMPTS[role]

# ==========================
# 初始化聊天状态
# ==========================

if "current_role" not in st.session_state:
    st.session_state.current_role = role

if "messages" not in st.session_state:
    st.session_state.messages = create_default_messages(system_prompt)

# ==========================
# 检测角色是否发生变化
# ==========================

if st.session_state.current_role != role:
    st.session_state.current_role = role
    # 切换角色后，使用新角色的系统提示词重置聊天
    st.session_state.messages = create_default_messages(system_prompt)
    # 立即重新运行页面，更新聊天界面
    st.rerun()

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

        st.session_state.messages =create_default_messages(system_prompt)

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