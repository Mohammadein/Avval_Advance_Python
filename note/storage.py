from .models import Note
from . import errors
import json
import logging

logger = logging.getLogger(__name__)

def load_notes() -> list[Note]:
    notes: list[Note] = []
    try:
        with open("notes.json", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                notes.append(Note(**json.loads(line)))
        logger.info("Loaded %d notes", len(notes))
    except FileNotFoundError:
        logger.info("No existing notes file found.")
        return notes
    return notes

# output
@errors.handle_file_errors
def write_note(note: Note):
    with open("notes.json", "a") as f:
        json.dump(note.__dict__, f)
        f.write("\n")
    logger.info("Note written to file: %s", note.id)

@errors.handle_file_errors  
def save_all_notes(notes: list[Note]):
    with open("notes.json", "w") as f:
        for note in notes:
            json.dump(note.__dict__, f)
            f.write("\n")
    logger.info("All notes saved to file")