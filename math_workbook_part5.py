# === Stage 5: Удаление и восстановление ===
# Project: MathWorkbook
"""Модуль MathWorkbook: мягкое удаление задачи с возможностью восстановления.

Реализует функцию удаления задачи (soft delete) и восстановление удалённой задачи.
Использует только стандартную библиотеку. Предполагается, что объект задачи
представляет собой словарь или объект со свойствами: id, condition, topic,
difficulty, status. При удалении устанавливается флаг deleted=True и в status
добавляется метка deleted_at со временем удаления.
"""

import time
from datetime import datetime


def soft_delete_task(task):
    """Устанавливает для задачи статус удалённой с возможностью восстановления.

    Возвращает обновлённую копию задачи. Флаг deleted=True помечает запись как
    удалённую, а в словаре status добавляется метка deleted_at с меткой времени.
    """
    new_task = dict(task)
    new_task["deleted"] = True
    new_task["deleted_at"] = datetime.now().isoformat()
    if isinstance(new_task.get("status"), str):
        new_task["status"] = "deleted_at_" + new_task["status"]
    return new_task


def restore_task(task):
    """Восстанавливает ранее удалённую задачу (soft delete).

    Возвращает обновлённую копию задачи. Убирает флаг deleted и метку времени
    удаления, а из статуса убирает префикс deleted_at_, если он присутствует.
    """
    new_task = dict(task)
    new_task.pop("deleted", None)
    new_task.pop("deleted_at", None)
    status = new_task.get("status")
    if isinstance(status, str) and status.startswith("deleted_at_"):
        new_task["status"] = status[len("deleted_at_"):]
    return new_task


def list_deleted_tasks(tasks):
    """Возвращает список задач, помеченных как удалённые (deleted=True)."""
    return [t for t in tasks if t.get("deleted")]


def find_task_by_id(tasks, task_id):
    """Возвращает первую задачу в списке с заданным идентификатором."""
    for task in tasks:
        if task.get("id") == task_id:
            return task
    return None


def remove_task(tasks, task_id):
    """Удаляет задачу по id, возвращая обновлённый список задач.

    При нахождении задачи вызывается soft_delete_task. Если задача не найдена,
    список остаётся без изменений.
    """
    for index, task in enumerate(tasks):
        if task.get("id") == task_id:
            tasks[index] = soft_delete_task(task)
            return tasks
    return tasks


def restore_task_by_id(tasks, task_id):
    """Восстанавливает ранее удалённую задачу по id, возвращая обновлённый список."""
    for index, task in enumerate(tasks):
        if task.get("id") == task_id and task.get("deleted"):
            tasks[index] = restore_task(task)
            return tasks
    return tasks
