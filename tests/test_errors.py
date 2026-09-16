import pytest
import typer

from note import errors


def test_note_not_found_error(capsys):
    @errors.handle_note_errors
    def find_note():
        raise errors.NoteNotFoundError

    find_note()

    assert capsys.readouterr().out == "error: Note not found\n"


def test_invalid_input_error(capsys):
    @errors.handle_note_errors
    def update_note():
        raise errors.InvalidInput

    update_note()

    assert capsys.readouterr().out == "error: Invalid input\n"


def test_storage_error(capsys):
    @errors.handle_note_errors
    def save_notes():
        raise ValueError

    with pytest.raises(typer.Exit):
        save_notes()

    assert capsys.readouterr().out == "error: Storage operation failed\n"


def test_file_error_is_raised_again():
    @errors.handle_file_errors
    def load_file():
        raise FileNotFoundError

    with pytest.raises(FileNotFoundError):
        load_file()