from sympy.abc import delta

from config import client

def chat_with_ai_stream(messages,model_name, temperature,max_tokens):
    responses = client.chat.completions.create(
        # model="qwen3.7-max-2026-05-20",
        model=model_name,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True
    )
    # return responses.choices[0].message.content
    for chunk in responses:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


