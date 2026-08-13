import json

from config.settings import HISTORY_FILE


# =========================================================
# 保存聊天记录
# =========================================================

def save_history(messages):
    """
    将聊天记录保存为 JSON 文件。

    参数：
        messages: 聊天消息列表
    """

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            messages,
            file,
            ensure_ascii=False,
            indent=4,
        )


# =========================================================
# 加载聊天记录
# =========================================================

def load_history():
    """
    从 JSON 文件加载聊天记录。

    如果文件不存在、为空或者损坏，
    返回空列表。
    """

    if not HISTORY_FILE.exists():
        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            messages = json.load(file)

            if isinstance(messages, list):
                return messages

            return []

    except (
        json.JSONDecodeError,
        OSError,
    ):
        return []


# =========================================================
# 清空聊天记录
# =========================================================

def clear_history():
    """
    清空本地聊天记录。
    """

    save_history([])