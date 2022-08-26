from contextlib import ContextDecorator
from datetime import datetime


class LogFile(ContextDecorator):
    """Class to log runtime information of wrapped function to file.

    Args:
      path: A path-like object to store logs

    """
    __slots__ = ('path', 'log_file', 'start_time')

    def __init__(self, path):
        self.path = path
        self.log_file = None
        self.start_time = None

    def __enter__(self):
        self.start_time = datetime.now()
        self.log_file = open(self.path, 'a+')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            running_time = datetime.now() - self.start_time
            self.log_file.write(
                f'Start: {self.start_time} |'
                f' Run: {running_time} |'
                f' An error occurred: {exc_value}\n'
            )
        except Exception:
            raise exc_type
        finally:
            self.log_file.close()
