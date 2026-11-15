# === Stage 6: Связанная сущность ===
# Project: MathWorkbook
"""Модуль сущности «попытка» для учебника MathWorkbook.

Связывает попытку с задачей по идентификатору и предоставляет
функции добавления попыток. Работает на чистой стандартной библиотеке.
"""

import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Attempt:
    """Одна попытка решения задачи.

    Поля:
        task_id: идентификатор задачи, к которой относится попытка.
        answer: введённый пользователем ответ.
        is_correct: результат проверки ответа.
    """

    task_id: str
    answer: str
    is_correct: bool


class AttemptStore:
    """Хранилище попыток, привязанных к задачам по идентификатору."""

    def __init__(self) -> None:
        self._attempts: Dict[str, List[Attempt]] = {}

    def add_attempt(
        self, task_id: str, answer: str, is_correct: bool
    ) -> Attempt:
        """Добавить новую попытку к задаче.

        Если для задачи ещё не существовало записи, она создаётся.
        Возвращается сама созданная попытка.
        """

        if not task_id:
            raise ValueError("task_id не может быть пустым")

        attempt = Attempt(
            task_id=task_id, answer=answer, is_correct=is_correct
        )

        tasks = self._attempts.setdefault(task_id, [])
        tasks.append(attempt)
        return attempt

    def get_attempts(self, task_id: str) -> List[Attempt]:
        """Вернуть все попытки для указанной задачи."""

        return list(self._attempts.get(task_id, []))

    def get_attempt(self, attempt_id: str) -> Optional[Attempt]:
        """Найти попытку по её собственному идентификатору."""

        for attempt in self._attempts.values():
            for candidate in attempt:
                if candidate.id == attempt_id:
                    return candidate
        return None

    def count_attempts(self, task_id: str) -> int:
        """Узнать, сколько попыток уже есть у задачи."""

        return len(self._attempts.get(task_id, []))


def make_attempt_id() -> str:
    """Сгенерировать уникальный идентификатор для попытки."""

    return uuid.uuid4().hex
