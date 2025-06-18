#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
from core import CsvLoader, TablePrinter, Filter, Aggregator, OrderBy


def main() -> None:
    """Точка входа для скрипта."""
    parser = argparse.ArgumentParser(
        description="Обработка CSV-файла с фильтрацией и агрегацией."
    )
    parser.add_argument("--file", required=True, help="Путь к CSV-файлу")
    parser.add_argument(
        "--where", required=False, help="Условие фильтрации, например: price>100"
    )
    parser.add_argument(
        "--aggregate",
        required=False,
        help="Агрегация: <операция>:<колонка>, например avg:price",
    )
    parser.add_argument(
        "--order-by",
        required=False,
        help="Сортировка: <column>=asc|desc, например price=desc",
    )
    args = parser.parse_args()

    try:
        loader = CsvLoader(args.file)
        rows = loader.load()
        if args.where:
            try:
                rows = Filter(args.where).apply(rows)
            except Exception as e:
                print(f"Ошибка фильтрации: {e}", file=sys.stderr)
                sys.exit(1)
        if args.order_by:
            try:
                rows = OrderBy(args.order_by).apply(rows)
            except Exception as e:
                print(f"Ошибка сортировки: {e}", file=sys.stderr)
                sys.exit(1)
        if args.aggregate:
            try:
                if ":" not in args.aggregate:
                    raise ValueError(
                        "Формат агрегации: <операция>:<колонка>, например avg:price"
                    )
                op, col = args.aggregate.split(":", 1)
                result = Aggregator(op).apply(rows, col)
                print(f"{op}({col}) = {result}")
                return
            except Exception as e:
                print(f"Ошибка агрегации: {e}", file=sys.stderr)
                sys.exit(1)
        printer = TablePrinter()
        printer.print(rows)
    except FileNotFoundError:
        print(f"Ошибка: файл '{args.file}' не найден.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
