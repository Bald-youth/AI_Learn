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
