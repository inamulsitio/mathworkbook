# === Stage 1: Каркас модуля ===
# Project: MathWorkbook
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SOLVED = "solved"


@dataclass
class Task:
    condition: str
    topic: str
    difficulty: int
    status: TaskStatus = TaskStatus.PENDING

    @property
    def difficulty_label(self) -> str:
        return {
            1: "легко",
            2: "средне",
            3: "сложно",
        }.get(self.difficulty, "неизвестно")


def make_demo_tasks() -> list[Task]:
    return [
        Task(
            condition="Реши уравнение 2x + 6 = 0",
            topic="Линейные уравнения",
            difficulty=1,
            status=TaskStatus.PENDING,
        ),
        Task(
            condition="Найди площадь круга радиусом 5",
            topic="Геометрия",
            difficulty=2,
            status=TaskStatus.IN_PROGRESS,
        ),
        Task(
            condition="Вычисли интеграл ∫x² dx",
            topic="Интегральное исчисление",
            difficulty=3,
            status=TaskStatus.SOLVED,
        ),
    ]


def main() -> None:
    tasks = make_demo_tasks()
    for task in tasks:
        print(task.condition)
        print(f"  тема: {task.topic}")
        print(f"  сложность: {task.difficulty} ({task.difficulty_label})")
        print(f"  статус: {task.status.value}")
        print()


if __name__ == "__main__":
    main()
