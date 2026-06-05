from http.client import responses

from openai import OpenAI, base_url

client = OpenAI(
    api_key="sk-xxxxx",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
)
question = input("你：")
response = client.chat.completions.create(
    model="gui-plus-2026-02-26",
    messages=[
        {
            "role":"user",
            "content":question
        }
    ]
)
print(response.choices[0].message.content)
