import json
import logging
from . import IO
import functools
import typer

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
        except InvalidInput:
            logger.error("Invalid input")
        except (PermissionError, FileNotFoundError, json.JSONDecodeError):
            IO.error("Storage operation failed")
            raise typer.Exit(code=1)
    return wrapper

def handle_file_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            logger.error("File not found")
            raise
        except json.JSONDecodeError:
            logger.error("Error decoding JSON")
            raise
        except FileExistsError:
            logger.error("File already exists")
            raise
        except PermissionError:
            logger.error("Permission denied")
            raise
    return wrapper