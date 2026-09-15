from .models import Note
from . import errors
import json
import logging
import inspect

logger = logging.getLogger(__name__)
required_note_fields= set(inspect.signature(Note).parameters)

@errors.handle_file_errors
def load_notes() -> list[Note]:
    notes: list[Note] = []
    notes_list: list[dict] = []
    try:
        with open("notes.json", "r") as f:
            notes_list = json.load(f)
        if not isinstance(notes_list, list):
            raise ValueError("notes.json must contain a list")

        for n in notes_list:
            if not isinstance(n, dict):
                raise ValueError("a note must be an object")

            missing = required_note_fields - n.keys()
            if missing:
                raise ValueError(f"Missing note fields: {missing}")
            notes.append(Note(**n))

        logger.info("Loaded %d notes", len(notes))

    except FileNotFoundError:
        logger.info("No existing notes file found.")
        return notes
    return notes

# output
@errors.handle_file_errors  
def save_all_notes(notes: list[Note]):
    notes_dicts: list[dict] = []
    for note in notes:
        notes_dicts.append(note.__dict__)

    with open("notes.json", "w") as f:
        json.dump(notes_dicts, f)
    logger.info("All notes saved to file")