import functools
import json
import logging

import typer

from . import cli_io

logger = logging.getLogger(__name__)


class NoteNotFoundError(Exception):
    pass


class InvalidInput(Exception):
    pass

class InvalidNote(Exception):
    pass


def handle_note_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoteNotFoundError:
            logger.error("Note not found")
            cli_io.error("Note not found")
        except InvalidInput:
            logger.error("Invalid input")
            cli_io.error("Invalid input")
        except (
            PermissionError,
            FileNotFoundError,
            FileExistsError,
            json.JSONDecodeError,
            ValueError,
            InvalidNote
        ):
            cli_io.error("Storage operation failed")
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
        except json.JSONDecodeError as exc:
            logger.exception("Invalid notes.json")
            raise InvalidNote(
                "notes.json contains invalid JSON"
            ) from exc
        except FileExistsError:
            logger.exception("File already exists")
            raise
        except PermissionError:
            logger.exception("Permission denied")
            raise
        except ValueError:
            logger.exception("Value error")
            raise
        except InvalidNote:
            logger.exception("Invalid saved note parameter")
            raise
    return wrapper