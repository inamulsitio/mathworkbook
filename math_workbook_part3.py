# === Stage 3: Хранилище в памяти ===
# Project: MathWorkbook
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Task:
    condition: str
    topic: str
    difficulty: str
    status: str = "new"
    id: Optional[str] = None

    def set_id(self, task_id: str) -> None:
        self.id = task_id


@dataclass
class TaskStore:
    tasks: Dict[str, Task] = field(default_factory=dict)

    def add_task(self, task: Task) -> Task:
        if task.id is None:
            raise ValueError("Задача должна иметь идентификатор")
        if task.id in self.tasks:
            raise KeyError(f"Задача с идентификатором {task.id} уже существует")
        self.tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def list_tasks(self, topic: Optional[str] = None) -> List[Task]:
        result: List[Task] = list(self.tasks.values())
        if topic is not None:
            result = [task for task in result if task.topic == topic]
        return sorted(result, key=lambda task: task.id)
