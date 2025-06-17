from typing import List, Dict, Any, Optional
import csv
from tabulate import tabulate


class CsvLoader:
    """Загружает данные из CSV-файла."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def load(self) -> List[Dict[str, Any]]:
        """Читает CSV-файл и возвращает список словарей."""
        with open(self.file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]


class Filter:
    """Фильтрует данные по условию."""

    def __init__(self, condition: Optional[str] = None) -> None:
        self.condition = condition

    def apply(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Заглушка: фильтрует строки по условию."""
        pass


class Aggregator:
    """Выполняет агрегацию по числовой колонке."""

    def __init__(self, operation: Optional[str] = None) -> None:
        self.operation = operation

    def apply(self, rows: List[Dict[str, Any]], column: str) -> Any:
        """Заглушка: агрегирует значения колонки."""
        pass


class OrderBy:
    """Сортирует данные по колонке."""

    def __init__(self, order: Optional[str] = None) -> None:
        self.order = order

    def apply(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Заглушка: сортирует строки по колонке."""
        pass


class TablePrinter:
    """Печатает таблицу в консоль с помощью tabulate."""

    def print(self, rows: List[Dict[str, Any]]) -> None:
        if not rows:
            print("Нет данных для отображения.")
            return
        print(tabulate(rows, headers="keys", tablefmt="grid", showindex=False))
