from typing import List, Dict, Any, Optional


class CsvLoader:
    """Загружает данные из CSV-файла."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def load(self) -> List[Dict[str, Any]]:
        """Заглушка: возвращает список строк из CSV."""
        pass


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
    """Печатает таблицу в консоль."""

    def print(self, rows: List[Dict[str, Any]]) -> None:
        """Заглушка: выводит таблицу."""
        pass
