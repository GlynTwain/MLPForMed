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


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def modification_date_for_rename(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t).strftime("%d-%m-%YT %I-%M")


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t).strftime("%d.%m.%Y %I:%M")


def create_file(user):
    """Метод создания файлов"""
    name_file = folderName + "/" + user["username"] + ".txt"

    if os.path.exists(name_file):
        new_name = folderName + "/" + user["username"] + "_" + modification_date_for_rename(name_file) + ".txt"
        os.rename(name_file, new_name)

    if not os.path.exists(name_file):
        filling(user, name_file)


def filling(user, name_file):
    file = open(name_file, mode='w+', encoding='utf-8')
    file.write(user["name"] + " <" + user["email"] + "> " + modification_date(name_file) + '\n')
    file.write(user["company"]["name"] + '\n')
    file.write('\n'+"Завершенные задачи:" + '\n')
    for todos_from_base in myTodosJson:
        if user["id"] == todos_from_base["userId"] and todos_from_base["completed"] == True:
            task = todos_from_base["title"]
            if len(task) >= 51:
                file.write(task[0: 50] + "..." + '\n')
            else:
                file.write(task + '\n')
    file.write('\n'+"Оставшиеся задачи:" + '\n')
    for todos_from_base in myTodosJson:
        if user["id"] == todos_from_base["userId"] and todos_from_base["completed"] == False:
            task = todos_from_base["title"]
            if len(task) >= 51:
                file.write(task[0: 50] + "..." + '\n')
            else:
                file.write(task + '\n')
    file.close()


def work_todos(userId, file):
    for todos_from_base in myTodosJson:
        if userId == todos_from_base[userId] and todos_from_base["completed"] == "true":
            task = todos_from_base["title"]
            if len(task) > 50:
                task[0, 50]
                file.write(task + "..." + '\n')
            else:
                file.write(task + '\n')


for user_from_base in myUserJson:
    create_file(user_from_base)
