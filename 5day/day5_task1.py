from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

question = input("请输入问题：")
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="gui-plus-2026-02-26",
    messages=[
        {
            "role": "user",
            "content": question
        }
    ]
)

print(response.choices[0].message.content)