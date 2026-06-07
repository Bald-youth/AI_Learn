from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def chat_with_ai(messages):
    response = client.chat.completions.create(
        model="gui-plus-2026-02-26",
        messages=messages
    )
    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})
    print("AI：", answer)
    return answer

def save_chat_history(question, answer):
    with open("chat_history.txt", "a",encoding="utf-8") as f:
        f.write(f"用户：{question}\n")
        f.write(f"AI：{answer}\n")
        f.write("-" * 50 + "\n")


if __name__ == '__main__':
    print("=== AI ChatBot V3 ===")
    print("输入 exit 或 退出 结束程序")

    messages = []

    while True:
        question = input("请输入问题：")

        if question.lower() == "exit" or question == "退出":
            print("程序结束")
            break

        messages.append({"role": "user", "content": question})

        answer = chat_with_ai(messages)

        save_chat_history(question, answer)





