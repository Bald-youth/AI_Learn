# Json反向转化
import json
json_str = '{"name":"David","age":29}'

user = json.loads(json_str)
print(user)
print(user["name"])