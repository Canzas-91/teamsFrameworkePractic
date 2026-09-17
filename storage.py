import json
from pathlib import Path
from typing import TypeVar

JSONData = TypeVar("JSONData", list, dict)


def load_json(filename: Path, default: JSONData) -> JSONData:
    try:
        with filename.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return default.copy()
    except json.JSONDecodeError as error:
        print(f"Некорректный JSON в файле {filename}: {error}")
        return default.copy()

    if not isinstance(data, type(default)):
        print(f"Неверный формат данных в файле {filename}.")
        return default.copy()
    return data


def save_json(filename: Path, data: list[dict] | dict) -> None:
    filename.parent.mkdir(parents=True, exist_ok=True)
    with filename.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
