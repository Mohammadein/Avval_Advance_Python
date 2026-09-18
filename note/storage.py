import inspect
import json
import logging

from . import errors
from .models import Note

logger = logging.getLogger(__name__)
required_note_fields= set(inspect.signature(Note).parameters)

@errors.handle_file_errors
def load_notes() -> list[Note]:
    notes: list[Note] = []
    notes_list: list[dict] = []
    note_ids: set[str] = set()
    try:
        logger.debug("Opening notes.json for loading")
        with open("notes.json", "r") as f:
            notes_list = json.load(f)
        if not isinstance(notes_list, list):
            raise errors.InvalidNote("notes.json must contain a list")

        for n in notes_list:
            if not isinstance(n, dict):
                raise errors.InvalidNote("a note must be an object")

            missing_fields = required_note_fields - n.keys()
            if missing_fields:
                raise errors.InvalidNote(f"Missing note fields: {missing_fields}")
            
            extra_fields = n.keys() - required_note_fields
            if extra_fields:
                raise errors.InvalidNote(f"Unexpected note fields: {extra_fields}")

            invalid_fields = sorted(
                field for field in required_note_fields if not isinstance(n[field], str)
            )
            if invalid_fields:
                raise errors.InvalidNote(
                    f"Invalid field types: {', '.join(invalid_fields)}"
                )

            note_id = n["id"]
            if not note_id.strip():
                raise errors.InvalidNote("Note id cannot be empty")
            if note_id in note_ids:
                raise errors.InvalidNote(f"Duplicate note id: {note_id}")
            note_ids.add(note_id)

            notes.append(Note.from_dict(n))

        logger.info("Loaded %d notes", len(notes))

    except FileNotFoundError:
        logger.info("No existing notes file found.")
        return notes
    return notes

# output
@errors.handle_file_errors  
def save_all_notes(notes: list[Note]):
    notes_dicts: list[dict] = []
    logger.debug("Serializing %d notes for storage", len(notes))
    for note in notes:
        notes_dicts.append(note.to_dict())

    with open("notes.json", "w") as f:
        json.dump(notes_dicts, f)
    logger.info("All notes saved to file")
