import pytest
from exceptions import CsvHandlerError


def test_csv_handler_error():
    with pytest.raises(CsvHandlerError):
        raise CsvHandlerError("Test error")
