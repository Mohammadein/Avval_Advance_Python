from .services import NoteManager
from . import errors
from . import IO
import typer
from .logging_config import setup_logging


setup_logging()
app = typer.Typer()

note_manager = NoteManager({})

@app.callback()
@errors.handle_note_errors
def initialize():
    note_manager.init()

@app.command()
@errors.handle_note_errors
def create():
    """Update a new note interactively."""
    
    title = IO.read_input()
    content = IO.read_multiline_input("content (end with END NOTE):")
    note = note_manager.create_note(title, content)

    IO.show_message("یادداشت ساخته شد با شناسه: " + note.id)

@app.command()
@errors.handle_note_errors
def list():
    """List all notes with title"""

    notes = note_manager.list_notes()
    for note in notes:
        IO.show_message(f"ID: {note.id} | Title: {note.title}")

@app.command()
@errors.handle_note_errors
def update(note_id: str):
    """Update a new note interactively."""

    note = note_manager.find_note_by_id(note_id)

    parameter = IO.read_input("Enter parameter to update (title or content):")
    if parameter != "title" and parameter != "content":
        raise errors.InvalidInput
    
    user_imput = IO.read_input("Enter new " + parameter)
    note_manager.update_note(note, parameter, user_imput)

@app.command()
@errors.handle_note_errors
def delete(note_id: str):
    """Delete a note by id."""
    
    note = note_manager.find_note_by_id(note_id)
    if IO.confirm("Do u really want to delete note with id:" + note_id):
        note_manager.delete_note(note)

@app.command()
@errors.handle_note_errors
def show(note_id: str):
    """Show a note by id."""

    note = note_manager.find_note_by_id(note_id)
    IO.show_message(note_manager.show_note(note))


if __name__ == "__main__":
    app()
