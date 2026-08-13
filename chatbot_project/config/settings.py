from pathlib import Path
import os

from dotenv import load_dotenv


# =========================================================
# 项目路径
# =========================================================

# 当前文件：
# chatbot_project/config/settings.py

# config 目录
CONFIG_DIR = Path(__file__).resolve().parent

# chatbot_project 目录
PROJECT_DIR = CONFIG_DIR.parent

# AI_Learn 项目根目录
ROOT_DIR = PROJECT_DIR.parent


# =========================================================
# 加载 .env
# =========================================================

ENV_FILE = ROOT_DIR / ".env"

load_dotenv(ENV_FILE)


# =========================================================
# AI 模型配置
# =========================================================

API_KEY = os.getenv("DASHSCOPE_API_KEY")

BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

MODEL = "qwen3.7-flash"


# =========================================================
# 数据目录
# =========================================================

DATA_DIR = PROJECT_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

HISTORY_FILE = DATA_DIR / "history.json"


# =========================================================
# 检查 API KEY
# =========================================================

if not API_KEY:
    print(
        "警告：没有读取到 DASHSCOPE_API_KEY，"
        "请检查项目根目录下的 .env 文件。"
    )