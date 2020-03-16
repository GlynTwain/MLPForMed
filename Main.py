import json
import requests
import os

folderName = "tasks"
os.mkdir(folderName)
if os.path.exists(folderName)

todos_json = requests.get("https://json.medrating.org/todos")
user_json = requests.get("https://json.medrating.org/users")

myUserJson = json.loads(user_json.text)



print(myUserJson[1]["name"])