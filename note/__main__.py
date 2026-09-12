from .models import Note
from .services import NoteManager
from . import errors
from .console import read_multiline_input
import typer

app = typer.Typer()

note_manager = NoteManager({}, None)
note_manager.init()

@app.command()
def create_note():
    """Update a new note interactively."""
    
    title = typer.prompt("title")
    content = read_multiline_input("content (end with END NOTE):")
    note = note_manager.create_note(title, content)

    typer.echo(f"یادداشت ساخته شد با شناسه: {note.id}")

@app.command()
def note_lsit():
    """List all notes with title"""

    notes = note_manager.list_notes()
    for note in notes:
        typer.echo(f"{note.id}: {note.title}")

@app.command()
def note_update(note_id: str):
    """Update a new note interactively."""

    note = note_manager.find_note_by_id(note_id)

    parameter = typer.prompt("U want to update title or content")
    if parameter != "title" and parameter != "content":
        raise errors.InvalidInput
    
    user_imput = typer.prompt("Enter new" + parameter)
    note_manager.update_note(note, parameter, user_imput)

@app.command()
def note_delete(note_id: str):
    """Delete a note by id."""
    
    note = note_manager.find_note_by_id(note_id)
    if typer.confirm("Do u really want to delete note with id:" + note_id):
        note_manager.delete_note(note)

@app.command()
def note_show(note_id: str):
    """Show a note by id."""

    note = note_manager.find_note_by_id(note_id)
    typer.echo(note_manager.show_note(note))
    

@app.command("test")
def test():
    typer.echo("Hello")

if __name__ == "__main__":
    app()
