import json

from sympy import false

user = {
    "name":"David",
    "age":29,
    "job":"AI开发工程师"
}

json_str = json.dumps(user,ensure_ascii=false)
print(json_str)