import functools
import json
import logging

import typer

from . import IO

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
        except (
            PermissionError,
            FileNotFoundError,
            FileExistsError,
            json.JSONDecodeError,
        ):
            IO.error("Storage operation failed")
            raise typer.Exit(code=1)
    return wrapper


def handle_file_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            logger.exception("File not found")
            raise
        except json.JSONDecodeError:
            logger.exception("Error decoding JSON")
            raise
        except FileExistsError:
            logger.exception("File already exists")
            raise
        except PermissionError:
            logger.exception("Permission denied")
            raise
    return wrapper