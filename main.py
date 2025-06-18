#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
from core import CsvLoader, TablePrinter, Filter


def main() -> None:
    """Точка входа для скрипта."""
    parser = argparse.ArgumentParser(
        description="Обработка CSV-файла с фильтрацией и агрегацией."
    )
    parser.add_argument("--file", required=True, help="Путь к CSV-файлу")
    parser.add_argument(
        "--where", required=False, help="Условие фильтрации, например: price>100"
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
