import json
import requests
import os
import platform
import time
import datetime

folderName: str = "tasks"
if not os.path.exists(folderName):
    os.mkdir(folderName)

todos_json = requests.get("https://json.medrating.org/todos")
myTodosJson = json.loads(todos_json.text)
user_json = requests.get("https://json.medrating.org/users")
myUserJson = json.loads(user_json.text)


def creation_date(name_file):
    file_for_rename = open(name_file)
    line = file_for_rename.readline()
    line = line.partition("> ")[2].replace(".","-").replace(":","-")
    line = line[0:16]

    file_for_rename.close()
    return line


def modification_date_for_rename(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t).strftime("%d-%m-%YT %H-%M")


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t).strftime("%d.%m.%Y %H:%M")


def create_file(user):
    """Метод создания файлов"""
    name_file = folderName + "/" + user["username"] + ".txt"

    if os.path.exists(name_file):

        new_name = folderName + "/" + user["username"] + "_" + creation_date(name_file) + ".txt"
        creation_date(name_file)
        os.rename(name_file, new_name)

    if not os.path.exists(name_file):
        filling(user, name_file)


def filling(user, name_file):
    file = open(name_file, mode='w+', encoding='utf-8')
    file.write(user["name"] + " <" + user["email"] + "> " + modification_date(name_file) + '\n')
    file.write(user["company"]["name"] + '\n')
    work_todos(user["id"], file, "Завершенные задачи:", True)
    work_todos(user["id"], file, "Оставшиеся задачи:", False)
    file.close()


def work_todos(user_Id, file, text_print, completed):
    file.write('\n' + text_print + '\n')
    for todos_from_base in myTodosJson:
        if user_Id == todos_from_base["userId"] and todos_from_base["completed"] == completed:
            task = todos_from_base["title"]
            if len(task) >= 51:
                file.write(task[0: 50] + "..." + '\n')
            else:
                file.write(task + '\n')



for user_from_base in myUserJson:
    create_file(user_from_base)
