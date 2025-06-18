from core import CsvLoader, Filter, Aggregator, OrderBy, TablePrinter
import tempfile
import os
import pytest


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


def test_filter_numeric_gt():
    rows = [
        {"price": "10"},
        {"price": "20"},
        {"price": "5"},
    ]
    filtered = Filter("price>10").apply(rows)
    assert filtered == [{"price": "20"}]


def test_filter_numeric_lt():
    rows = [
        {"price": "10"},
        {"price": "20"},
        {"price": "5"},
    ]
    filtered = Filter("price<10").apply(rows)
    assert filtered == [{"price": "5"}]


def test_filter_numeric_eq():
    rows = [
        {"price": "10"},
        {"price": "20"},
        {"price": "5"},
    ]
    filtered = Filter("price=10").apply(rows)
    assert filtered == [{"price": "10"}]


def test_filter_string_eq():
    rows = [
        {"brand": "apple"},
        {"brand": "samsung"},
        {"brand": "xiaomi"},
    ]
    filtered = Filter("brand=apple").apply(rows)
    assert filtered == [{"brand": "apple"}]


def test_filter_nonexistent_column():
    rows = [{"a": "1"}]
    filtered = Filter("b=1").apply(rows)
    assert filtered == []


def test_filter_invalid_condition():
    with pytest.raises(ValueError):
        Filter("price!=10")


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


def test_aggregator_avg():
    rows = [
        {"price": "10"},
        {"price": "20"},
        {"price": "30"},
    ]
    result = Aggregator("avg").apply(rows, "price")
    assert result == 20


def test_aggregator_min():
    rows = [
        {"price": "10"},
        {"price": "20"},
        {"price": "30"},
    ]
    result = Aggregator("min").apply(rows, "price")
    assert result == 10


def test_aggregator_max():
    rows = [
        {"price": "10"},
        {"price": "20"},
        {"price": "30"},
    ]
    result = Aggregator("max").apply(rows, "price")
    assert result == 30


def test_aggregator_non_numeric():
    rows = [
        {"price": "10"},
        {"price": "abc"},
    ]
    with pytest.raises(ValueError):
        Aggregator("avg").apply(rows, "price")


def test_aggregator_empty():
    rows = []
    with pytest.raises(ValueError):
        Aggregator("avg").apply(rows, "price")


def test_aggregator_unknown_op():
    rows = [{"price": "10"}]
    with pytest.raises(ValueError):
        Aggregator("sum").apply(rows, "price")


def test_order_by_numeric_asc():
    rows = [
        {"price": "20"},
        {"price": "10"},
        {"price": "30"},
    ]
    sorted_rows = OrderBy("price=asc").apply(rows)
    assert [r["price"] for r in sorted_rows] == ["10", "20", "30"]


def test_order_by_numeric_desc():
    rows = [
        {"price": "20"},
        {"price": "10"},
        {"price": "30"},
    ]
    sorted_rows = OrderBy("price=desc").apply(rows)
    assert [r["price"] for r in sorted_rows] == ["30", "20", "10"]


def test_order_by_string_asc():
    rows = [
        {"brand": "xiaomi"},
        {"brand": "apple"},
        {"brand": "samsung"},
    ]
    sorted_rows = OrderBy("brand=asc").apply(rows)
    assert [r["brand"] for r in sorted_rows] == ["apple", "samsung", "xiaomi"]


def test_order_by_string_desc():
    rows = [
        {"brand": "xiaomi"},
        {"brand": "apple"},
        {"brand": "samsung"},
    ]
    sorted_rows = OrderBy("brand=desc").apply(rows)
    assert [r["brand"] for r in sorted_rows] == ["xiaomi", "samsung", "apple"]


def test_order_by_invalid_format():
    with pytest.raises(ValueError):
        OrderBy("price").apply([])


def test_order_by_invalid_direction():
    with pytest.raises(ValueError):
        OrderBy("price=up").apply([])
