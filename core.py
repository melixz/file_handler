from typing import List, Dict, Any, Optional
import csv
from tabulate import tabulate
import operator


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
    """Фильтрует данные по условию вида column>value, column<value, column=value."""

    OPERATORS = {
        ">": operator.gt,
        "<": operator.lt,
        "=": operator.eq,
    }

    def __init__(self, condition: Optional[str] = None) -> None:
        self.condition = condition
        self.column = None
        self.op = None
        self.value = None
        if condition:
            self._parse_condition(condition)

    def _parse_condition(self, condition: str) -> None:
        found = []
        for op_symbol in self.OPERATORS:
            idx = condition.find(op_symbol)
            if idx != -1:
                before = condition[idx - 1] if idx > 0 else ""
                after = condition[idx + 1] if idx + 1 < len(condition) else ""
                if (
                    before in self.OPERATORS
                    or before == "!"
                    or after in self.OPERATORS
                    or after == "="
                    or before == "="
                ):
                    continue
                found.append((idx, op_symbol))
        if len(found) != 1:
            raise ValueError(
                f"Поддерживаются только операторы: {list(self.OPERATORS.keys())} и только один оператор в условии"
            )
        idx, op_symbol = found[0]
        parts = condition.split(op_symbol, 1)
        if len(parts) != 2:
            raise ValueError(f"Некорректное условие фильтрации: {condition}")
        self.column = parts[0].strip()
        self.op = self.OPERATORS[op_symbol]
        self.value = parts[1].strip()

    def apply(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not self.condition:
            return rows
        if self.column is None or self.op is None or self.value is None:
            raise ValueError("Фильтр не инициализирован")
        filtered = []
        for row in rows:
            cell = row.get(self.column)
            if cell is None:
                continue
            try:
                cell_val = float(cell)
                value_val = float(self.value)
            except ValueError:
                cell_val = cell
                value_val = self.value
            if self.op(cell_val, value_val):
                filtered.append(row)
        return filtered


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
