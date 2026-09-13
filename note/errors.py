import json

from . import IO
import functools

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
            IO.error("Note not found")
        except InvalidInput:
            IO.error("Invalid input")
        except Exception as e:
            IO.error(str(e))
    return wrapper

def handle_file_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            IO.error("File not found")
        except json.JSONDecodeError:
            IO.error("Error decoding JSON")
        except FileExistsError:
            IO.error("File already exists")
        except PermissionError:
            IO.error("Permission denied")
        except Exception as e:
            IO.error(str(e))
    return wrapper