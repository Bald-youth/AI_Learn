def messages_to_text(messages):
    """
    将 messages 转换成适合下载的文本格式。

    参数：
        messages: 聊天消息列表

    返回：
        str
    """

    lines = []

    for message in messages:

        role = message.get(
            "role",
            ""
        )

        content = message.get(
            "content",
            ""
        )

        if role == "user":
            role_name = "用户"

        elif role == "assistant":
            role_name = "AI"

        elif role == "system":
            role_name = "系统"

        else:
            role_name = role

        lines.append(
            f"{role_name}：{content}"
        )

        lines.append(
            "----------------------------------------"
        )

    return "\n".join(lines)