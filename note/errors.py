import json
import logging
from . import IO
import functools

logger = logging.getLogger(__name__)

class NoteNotFoundError(Exception):
    pass
class InvalidInput(Exception):
    pass

def handle_note_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoteNotFoundError:
            logger.error("Note not found")
            IO.error("Note not found")
        except InvalidInput:
            logger.error("Invalid input")
            IO.error("Invalid input")
    return wrapper

def handle_file_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            logger.error("File not found")
            IO.error("File not found")
        except json.JSONDecodeError:
            logger.error("Error decoding JSON")
            IO.error("Error decoding JSON")
        except FileExistsError:
            logger.error("File already exists")
            IO.error("File already exists")
        except PermissionError:
            logger.error("Permission denied")
            IO.error("Permission denied")
    return wrapper