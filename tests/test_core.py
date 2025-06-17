from core import CsvLoader, Filter, Aggregator, OrderBy, TablePrinter
import tempfile
import os


def test_csv_loader_init():
    loader = CsvLoader("file.csv")
    assert loader.file_path == "file.csv"


def test_csv_loader_load():
    content = "name,brand,price\nA,BrandA,10\nB,BrandB,20\n"
    with tempfile.NamedTemporaryFile(
        "w+", delete=False, encoding="utf-8", newline=""
    ) as f:
        f.write(content)
        f.flush()
        loader = CsvLoader(f.name)
        rows = loader.load()
    os.unlink(f.name)
    assert rows == [
        {"name": "A", "brand": "BrandA", "price": "10"},
        {"name": "B", "brand": "BrandB", "price": "20"},
    ]


def test_filter_init():
    f = Filter("col>5")
    assert f.condition == "col>5"


def test_aggregator_init():
    a = Aggregator("avg")
    assert a.operation == "avg"


def test_order_by_init():
    o = OrderBy("col=desc")
    assert o.order == "col=desc"


def test_table_printer_init():
    p = TablePrinter()
    assert isinstance(p, TablePrinter)


def test_table_printer_print(capsys):
    rows = [
        {"name": "A", "brand": "BrandA", "price": "10"},
        {"name": "B", "brand": "BrandB", "price": "20"},
    ]
    printer = TablePrinter()
    printer.print(rows)
    out = capsys.readouterr().out
    assert "name" in out and "brand" in out and "price" in out
    assert "A" in out and "B" in out


def test_table_printer_print_empty(capsys):
    printer = TablePrinter()
    printer.print([])
    out = capsys.readouterr().out
    assert "Нет данных" in out
