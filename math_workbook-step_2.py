# === Stage 2: Проверка полей ===
# Project: MathWorkbook
def normalize_input(value):
    if value is None:
        return ""
    return value.strip().lower()


def normalize_difficulty(value):
    mapping = {
        "легко": "easy",
        "средне": "medium",
        "сложно": "hard",
        "easy": "easy",
        "medium": "medium",
        "hard": "hard",
    }
    return mapping.get(normalize_input(value), "medium")


def normalize_status(value):
    mapping = {
        "новая": "new",
        "в работе": "in_progress",
        "готово": "done",
        "new": "new",
        "in_progress": "in_progress",
        "done": "done",
    }
    return mapping.get(normalize_input(value), "new")


def validate_task(task):
    errors = {}

    condition = task.get("условие")
    if not condition or not str(condition).strip():
        errors["условие"] = "Укажите условие задачи (текст не может быть пустым)."

    topic = task.get("тема")
    if topic is None or str(topic).strip() == "":
        errors["тема"] = "Укажите тему задачи."
    elif normalize_input(topic) not in {"алгебра", "геометрия", "арифметика", "тригонометрия", "анализ"}:
        errors["тема"] = "Неверная тема. Допустимые значения: алгебра, геометрия, арифметика, тригонометрия, анализ."

    difficulty = task.get("сложность")
    if difficulty is None or str(difficulty).strip() == "":
        errors["сложность"] = "Укажите сложность задачи."
    elif normalize_difficulty(difficulty) not in {"easy", "medium", "hard"}:
        errors["сложность"] = "Неверная сложность. Допустимые значения: легко, средне, сложно."

    status = task.get("статус")
    if status is None or str(status).strip() == "":
        errors["статус"] = "Укажите статус задачи."
    elif normalize_status(status) not in {"new", "in_progress", "done"}:
        errors["статус"] = "Неверный статус. Допустимые значения: новая, в работе, готово."

    return errors


def normalize_task(task):
    if not validate_task(task):
        return None

    return {
        "условие": normalize_input(task["условие"]),
        "тема": normalize_input(task["тема"]),
        "сложность": normalize_difficulty(task["сложность"]),
        "статус": normalize_status(task["статус"]),
    }
