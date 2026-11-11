# === Stage 4: Редактирование записей ===
# Project: MathWorkbook
from dataclasses import dataclass, field
from typing import Any

ALLOWED_FIELDS = {"условие", "тема", "сложность", "статус"}
VALID_STATUSES = {"готово", "в работе", "не решена"}
VALID_COMPLEXITY = {"легко", "средне", "сложно"}


@dataclass
class Task:
    id: Any
    условие: str
    тема: str
    сложность: str
    статус: str = "не решена"

    def update(self, changes: dict[str, Any]) -> dict[str, Any]:
        """Применяет изменение полей задачи, если только допустимые и валидные.

        Возвращает словарь с применёнными полями. Если ни одно поле не
        прошло проверку, возвращается пустой словарь.
        """
        applied: dict[str, Any] = {}
        for key, value in changes.items():
            if key not in ALLOWED_FIELDS:
                continue
            if key == "статус":
                if value not in VALID_STATUSES:
                    continue
            elif key == "сложность":
                if value not in VALID_COMPLEXITY:
                    continue
            if key == "условие":
                if not isinstance(value, str):
                    continue
            setattr(self, key, value)
            applied[key] = value
        return applied


@dataclass
class TaskEditor:
    tasks: dict[Any, Task] = field(default_factory=dict)

    def get(self, task_id: Any) -> Task | None:
        return self.tasks.get(task_id)

    def edit(
        self, task_id: Any, changes: dict[str, Any]
    ) -> dict[str, Any]:
        task = self.get(task_id)
        if task is None:
            raise KeyError(f"Задача с идентификатором {task_id} не найдена")
        return task.update(changes)

    def add(self, task: Task) -> None:
        self.tasks[task.id] = task

    def list_tasks(self) -> list[Task]:
        return list(self.tasks.values())
