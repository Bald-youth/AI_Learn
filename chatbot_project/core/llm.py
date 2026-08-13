from openai import OpenAI

from config.settings import (
    API_KEY,
    BASE_URL,
    MODEL,
)


# =========================================================
# 创建 OpenAI 客户端
# =========================================================

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)


# =========================================================
# 普通聊天
# =========================================================

def chat(messages):
    """
    调用大语言模型。

    参数：
        messages: 聊天消息列表

    返回：
        AI 回复字符串
    """

    if not API_KEY:
        raise ValueError(
            "没有找到 DASHSCOPE_API_KEY，"
            "请检查 .env 文件。"
        )

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    return response.choices[0].message.content