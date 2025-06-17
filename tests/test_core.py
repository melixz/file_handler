from core import CsvLoader, Filter, Aggregator, OrderBy, TablePrinter


def test_csv_loader_init():
    loader = CsvLoader("file.csv")
    assert loader.file_path == "file.csv"


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
