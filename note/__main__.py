import typer
import uvicorn

from note import dependencies

from . import cli_io, errors
from .logging_config import setup_logging

setup_logging()
app = typer.Typer()

@app.command()
def web(port: int = 8000):
    """Run the web application."""
    uvicorn.run("note.web_app:app", host="127.0.0.1", port=port)

@app.command()
@errors.handle_note_errors
def create():
    """Update a new note interactively."""
    note_manager = dependencies.get_note_manager()

    title = cli_io.read_input()
    content = cli_io.read_multiline_input("content (end with END NOTE):")
    note = note_manager.create_note(title, content)

    cli_io.show_message("یادداشت ساخته شد با شناسه: " + note.id)

@app.command()
@errors.handle_note_errors
def list():
    """List all notes with title"""
    note_manager = dependencies.get_note_manager()

    notes = note_manager.list_notes()
    for note in notes:
        cli_io.show_message(f"ID: {note.id} | Title: {note.title}")

@app.command()
@errors.handle_note_errors
def update(note_id: str):
    """Update a new note interactively."""
    note_manager = dependencies.get_note_manager()

    note = note_manager.find_note_by_id(note_id)

    parameter = cli_io.read_input("Enter parameter to update (title or content):")
    if parameter != "title" and parameter != "content":
        raise errors.InvalidInput
    
    user_imput = cli_io.read_input("Enter new " + parameter)
    note_manager.update_note(note, parameter, user_imput)

@app.command()
@errors.handle_note_errors
def delete(note_id: str):
    """Delete a note by id."""
    note_manager = dependencies.get_note_manager()
    
    note = note_manager.find_note_by_id(note_id)
    if cli_io.confirm("Do u really want to delete note with id:" + note_id):
        note_manager.delete_note(note)

@app.command()
@errors.handle_note_errors
def show(note_id: str):
    """Show a note by id."""
    note_manager = dependencies.get_note_manager()

    note = note_manager.find_note_by_id(note_id)
    cli_io.show_message(note_manager.show_note(note))


if __name__ == "__main__":
    app()
