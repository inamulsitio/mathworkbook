# === Stage 8: Сортировка записей ===
# Project: MathWorkbook
import datetime


def sort_tasks_by_condition(tasks, reverse=False):
    tasks = list(tasks)
    tasks.sort(key=lambda task: task["условие"].lower(), reverse=reverse)
    return tasks


def sort_tasks_by_created_at(tasks, reverse=False):
    tasks = list(tasks)
    tasks.sort(key=lambda task: task["created_at"], reverse=reverse)
    return tasks


def sort_tasks(tasks, key="условие", reverse=False):
    tasks = list(tasks)
    if key == "условие":
        tasks.sort(key=lambda task: task["условие"].lower(), reverse=reverse)
    elif key == "created_at":
        tasks.sort(key=lambda task: task["created_at"], reverse=reverse)
    else:
        raise ValueError("Недопустимое поле для сортировки: " + str(key))
    return tasks


def add_created_at(tasks):
    now = datetime.datetime.now()
    for task in tasks:
        if "created_at" not in task:
            task["created_at"] = now
    return tasks


def sort_tasks_by_condition_and_date(tasks, reverse=False):
    tasks = list(tasks)
    tasks.sort(
        key=lambda task: (task["created_at"], task["условие"].lower()),
        reverse=reverse,
    )
    return tasks
