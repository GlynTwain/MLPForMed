import json
import requests
import os

folderName: str = "tasks"
if not os.path.exists(folderName):
    os.mkdir(folderName)

todos_json = requests.get("https://json.medrating.org/todos")
user_json = requests.get("https://json.medrating.org/users")

myUserJson = json.loads(user_json.text)
print(myUserJson[3]["name"])


def napechate():
    """Сформировать файл"""
    outfilename = myUserJson[1]["name"] + ".txt"
    file = open(myUserJson[1]["name"], mode='w+', encoding='utf-8')
