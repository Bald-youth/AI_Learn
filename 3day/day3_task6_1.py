
import json
data = {
    "answer":"你好"
}

json_str = json.dumps(data["answer"],ensure_ascii=False)
print(json_str)
