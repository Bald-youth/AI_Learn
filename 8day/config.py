# 从 .env 文件读取环境变量
from dotenv import load_dotenv

# OpenAI SDK（阿里百炼兼容 OpenAI SDK）
from openai import OpenAI

# Python内置模块，用来读取环境变量
import os

# ==========================
# 加载 .env 配置文件
# ==========================
load_dotenv()

SYSTEM_PROMPT = """
你是一名资深 Python 和 AI 应用开发导师，
请用简洁、清晰、鼓励但不啰嗦的方式回答用户。
"""

client = OpenAI(
    # 从 .env 中读取 API Key
    api_key=os.getenv("DASHSCOPE_API_KEY"),

    # 阿里百炼兼容 OpenAI 接口
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
