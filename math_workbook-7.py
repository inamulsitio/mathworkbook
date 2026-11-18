# === Stage 7: Связи между сущностями ===
# Project: MathWorkbook
"""Модуль MathWorkbook. Этап 7 из 54:
Получение всех «попытка» для заданной «задача» и проверка целостности связи.
Работает на стандартной библиотеке без внешних зависимостей."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class Task:
    id: int
    condition: str = ""
    topic: str = ""
    difficulty: int = 1
    status: str = "unsolved"


@dataclass
class Attempt:
    id: int
    task_id: Optional[int]
    answer: str = ""
    correct: bool = False


class IntegrityError(Exception):
    """Искажение связей между задачами и попытками."""


def collect_attempts(
    attempts: Iterable[Attempt],
    task_id: int,
) -> List[Attempt]:
    """Возвращает попытки, связанные с задачей task_id."""

    result: List[Attempt] = []
    for attempt in attempts:
        if attempt.task_id == task_id:
            result.append(attempt)
    return result


def build_index(attempts: Iterable[Attempt]) -> Dict[int, List[Attempt]]:
    """Индексирует попытки по task_id для ускорения последующих запросов."""

    index: Dict[int, List[Attempt]] = {}
    for attempt in attempts:
        index.setdefault(attempt.task_id, []).append(attempt)
    return index


def verify_integrity(
    attempts: Iterable[Attempt],
    task_ids: Iterable[int],
) -> Tuple[bool, List[Tuple[Optional[int], Optional[int]]]]:
    """Проверяет целостность связей.

    Возвращает кортеж (ok, проблемы), где проблемы — список пар
    (task_id, attempt_id) для попыток, ссылающихся на несуществующие задачи.
    """

    problems: List[Tuple[Optional[int], Optional[int]]] = []
    expected_ids = set(task_ids)
    for attempt in attempts:
        if attempt.task_id not in expected_ids:
            problems.append((attempt.task_id, attempt.id))
    return (len(problems) == 0), problems


def get_attempts_for_task(
    attempts: Iterable[Attempt],
    task: Task,
) -> Tuple[List[Attempt], bool]:
    """Группирует попытки по задаче и проверяет целостность связей.

    Возвращает кортеж (попытки, ok), где ok — признак целостности связей.
    """

    index = build_index(attempts)
    attempts_for_task = index.get(task.id, [])

    ok, problems = verify_integrity(attempts_for_task, [task.id])
    return attempts_for_task, ok


def summarize_task(
    attempts: Iterable[Attempt],
    task: Task,
) -> Dict[str, object]:
    """Формирует сводку по попыткам задачи."""

    attempts_for_task, ok = get_attempts_for_task(attempts, task)

    correct = sum(1 for a in attempts_for_task if a.correct)
    total = len(attempts_for_task)
    solved = task.status if task.status else (
        "solved" if correct > 0 else task.status
    )

    return {
        "task_id": task.id,
        "condition": task.condition,
        "topic": task.topic,
        "difficulty": task.difficulty,
        "status": solved,
        "attempts": attempts_for_task,
        "total_attempts": total,
        "correct_attempts": correct,
        "integrity_ok": ok,
        "integrity_problems": [],
    }


if __name__ == "__main__":
    sample_tasks = [
        Task(id=1, condition="2 + 2 = ?", topic="arithmetic", difficulty=1, status="unsolved"),
        Task(id=2, condition="5 * 3 = ?", topic="arithmetic", difficulty=2, status="unsolved"),
    ]

    sample_attempts = [
        Attempt(id=1, task_id=1, answer="4", correct=True),
        Attempt(id=2, task_id=1, answer="5", correct=False),
        Attempt(id=3, task_id=2, answer="15", correct=True),
        Attempt(id=4, task_id=99, answer="oops", correct=False),
    ]

    for task in sample_tasks:
        summary = summarize_task(sample_attempts, task)
        print(f"Задача {summary['task_id']}:")
        print(f"  Тема: {summary['topic']}, сложность: {summary['difficulty']}")
        print(f"  Статус: {summary['status']}")
        print(f"  Всего попыток: {summary['total_attempts']}")
        print(f"  Правильных: {summary['correct_attempts']}")
        print(f"  Целостность: {'ok' if summary['integrity_ok'] else 'broken'}")
        print()
