import streamlit as st

from core.llm import chat

from core.memory import (
    load_history,
    save_history,
    clear_history,
)

from utils.file import messages_to_text

from config.settings import MODEL


# =========================================================
# Streamlit 页面配置
# =========================================================

st.set_page_config(
    page_title="AI ChatBot V4",
    page_icon="🤖",
    layout="centered",
)


# =========================================================
# 系统角色
# =========================================================

SYSTEM_ROLES = {

    "Python 教练": (
        "你是一名资深 Python 开发工程师和 Python 教练。"
        "你的任务是帮助用户学习 Python 编程。"
        "回答时尽量循序渐进，并结合代码示例进行解释。"
        "对于初学者问题，不要一下子给出过于复杂的答案。"
    ),

    "AI 应用开发教练": (
        "你是一名资深 AI 应用开发工程师。"
        "擅长 Python、LLM、RAG、Agent、FastAPI、"
        "Streamlit、数据库和大模型 API 开发。"
        "你的任务是指导用户成长为 AI 应用开发工程师。"
        "解释技术问题时，需要说明原理、代码和实际应用场景。"
    ),

    "普通助手": (
        "你是一个专业、友好、准确的 AI 助手。"
        "请清晰回答用户提出的问题。"
    ),

}


# =========================================================
# 初始化 Session State
# =========================================================

if "messages" not in st.session_state:

    history = load_history()

    st.session_state.messages = history


if "role" not in st.session_state:

    st.session_state.role = "AI 应用开发教练"


# =========================================================
# 标题
# =========================================================

st.title("🤖 AI ChatBot V4")

st.caption(
    f"当前模型：{MODEL}"
)


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.header("⚙️ 设置")

    # -----------------------------------------------------
    # 系统角色
    # -----------------------------------------------------

    selected_role = st.selectbox(
        "系统角色",
        options=list(
            SYSTEM_ROLES.keys()
        ),
        index=list(
            SYSTEM_ROLES.keys()
        ).index(
            st.session_state.role
        ),
    )


    # -----------------------------------------------------
    # 角色发生变化
    # -----------------------------------------------------

    if selected_role != st.session_state.role:

        st.session_state.role = selected_role

        st.success(
            f"已切换角色：{selected_role}"
        )


    st.divider()


    # =====================================================
    # 聊天统计
    # =====================================================

    st.subheader("📊 聊天统计")


    user_messages = [
        message
        for message in st.session_state.messages
        if message.get("role") == "user"
    ]


    assistant_messages = [
        message
        for message in st.session_state.messages
        if message.get("role") == "assistant"
    ]


    all_chat_messages = (
        user_messages
        + assistant_messages
    )


    message_count = len(
        all_chat_messages
    )


    total_characters = sum(
        len(
            message.get(
                "content",
                ""
            )
        )
        for message in all_chat_messages
    )


    if message_count > 0:

        average_characters = (
            total_characters
            / message_count
        )

    else:

        average_characters = 0


    st.metric(
        "消息数量",
        message_count,
    )


    st.metric(
        "总字数",
        total_characters,
    )


    st.metric(
        "平均字数",
        f"{average_characters:.1f}",
    )


    st.divider()


    # =====================================================
    # 下载聊天记录
    # =====================================================

    history_text = messages_to_text(
        st.session_state.messages
    )


    st.download_button(
        label="📥 下载聊天记录",
        data=history_text,
        file_name="chat_history.txt",
        mime="text/plain",
        use_container_width=True,
    )


    # =====================================================
    # 清空聊天
    # =====================================================

    if st.button(
        "🗑️ 清空聊天",
        use_container_width=True,
    ):

        st.session_state.messages = []

        clear_history()

        st.rerun()


# =========================================================
# 显示历史消息
# =========================================================

for message in st.session_state.messages:

    role = message.get(
        "role"
    )

    content = message.get(
        "content"
    )


    if role not in [
        "user",
        "assistant",
    ]:
        continue


    with st.chat_message(role):

        st.markdown(
            content
        )


# =========================================================
# 用户输入
# =========================================================

user_input = st.chat_input(
    "请输入你的问题..."
)


# =========================================================
# 处理用户消息
# =========================================================

if user_input:


    # -----------------------------------------------------
    # 1. 保存用户消息
    # -----------------------------------------------------

    user_message = {
        "role": "user",
        "content": user_input,
    }


    st.session_state.messages.append(
        user_message
    )


    # -----------------------------------------------------
    # 2. 显示用户消息
    # -----------------------------------------------------

    with st.chat_message(
        "user"
    ):

        st.markdown(
            user_input
        )


    # -----------------------------------------------------
    # 3. 构造发送给 AI 的 messages
    # -----------------------------------------------------

    system_message = {
        "role": "system",
        "content": SYSTEM_ROLES[
            st.session_state.role
        ],
    }


    api_messages = [
        system_message
    ] + st.session_state.messages


    # -----------------------------------------------------
    # 4. AI 回复
    # -----------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "AI 正在思考..."
        ):

            try:

                answer = chat(
                    api_messages
                )

                st.markdown(
                    answer
                )

            except Exception as error:

                st.error(
                    f"调用 AI 失败：{error}"
                )

                answer = None


    # -----------------------------------------------------
    # 5. 保存 AI 回复
    # -----------------------------------------------------

    if answer:

        assistant_message = {
            "role": "assistant",
            "content": answer,
        }


        st.session_state.messages.append(
            assistant_message
        )


        # -------------------------------------------------
        # 6. 保存到 JSON
        # -------------------------------------------------

        save_history(
            st.session_state.messages
        )