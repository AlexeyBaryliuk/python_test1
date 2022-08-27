import pytest
import re
import io
from functools import wraps
from ..main import LogFile
from unittest.mock import patch

LOG_FILE_1 = 'text_log.txt'
LOG_FILE_2 = 'text_log2.txt'
LOG_FILE_3 = 'text_log3.txt'


class MockedFile(io.StringIO):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_faked_closed = False

    def final_close(self) -> None:
        super().close()

    def close(self) -> None:
        pass


def mocked_open(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        with patch('builtins.open') as open_mock:
            mocked_file = MockedFile()
            open_mock.return_value = mocked_file
            kwargs['mocked_file'] = mocked_file
            return fn(*args, **kwargs)

    return wrapper


@LogFile(LOG_FILE_1)
def func1(a: int) -> int:
    return 2 ** a


@LogFile(LOG_FILE_2)
def func_div_by_zero():
    return 2 / 0


@LogFile(LOG_FILE_3)
def func_d2(data):
    if data in range(0 | 1 | 3):
        return 2 / 0


@mocked_open
def test_logfile(**kwargs):
    iter_number = 10
    for i in range(iter_number):
        assert func1(i) == 2 ** i
    # Check log file
    mocked_file = kwargs['mocked_file']
    mocked_file.seek(0)
    pattern = (r"Start:\s+([0-9-\s:.]+)\|\s+Run:\s+([0-9:.]+)"
               r"\s+\|\s+An error occurred:\s+([\w]+)")
    prog = re.compile(pattern)
    lines_number = 0
    for line in mocked_file.readlines():
        assert bool(prog.match(line)) is True
        lines_number += 1
    mocked_file.final_close()
    assert lines_number == iter_number


@mocked_open
def test_logfile_div_by_zero(**kwargs):
    iter_number = 8
    for i in range(iter_number):
        with pytest.raises(ZeroDivisionError):
            func_div_by_zero()
    # Check log file
    mocked_file = kwargs['mocked_file']
    mocked_file.seek(0)
    pattern = (r"Start:\s+([0-9-\s:.]+)\|\s+Run:\s+([0-9:.]+)"
               r"\s+\|\s+An error occurred:\s+([\w ]+)")
    prog = re.compile(pattern)
    lines_number = 0
    for line in mocked_file.readlines():
        match = prog.match(line)
        assert bool(match) is True
        assert match.groups()[-1] == 'division by zero'
        lines_number += 1
    assert lines_number == iter_number


@mocked_open
def test_logfile_d2_by_zero(**kwargs):
    iter_number = 3
    for i in range(iter_number):
        with pytest.raises(ZeroDivisionError):
            func_d2(i)
    # Check log file
    mocked_file = kwargs['mocked_file']
    mocked_file.seek(0)
    pattern = (r"Start:\s+([0-9-\s:.]+)\|\s+Run:\s+([0-9:.]+)"
               r"\s+\|\s+An error occurred:\s+([\w ]+)")
    prog = re.compile(pattern)
    lines_number = 0
    for line in mocked_file.readlines():
        match = prog.match(line)
        assert bool(match) is True
        assert match.groups()[-1] == 'division by zero'
        lines_number += 1
    # assert lines_number == iter_number
