import datetime
import logging
import uuid
from zoneinfo import ZoneInfo

from . import errors, storage
from .models import Note

create_note_command = "create note"
list_notes_command = "list notes"
read_note_by_id_command = "read note"
update_note_by_id_command = "update note"
delete_note_by_id_command = "delete note"

logger = logging.getLogger(__name__)

class NoteManager:
    def __init__(self, notes: dict[str, Note]):
        self.notes = notes

    def init(self) -> None:
        logger.debug("Loading notes into NoteManager")
        self.load_notes()
        logger.info("NoteManager initialized with %d notes", len(self.notes))

    def load_notes(self) -> None:
        self.notes.clear()
        notes_list = storage.load_notes()
        for note in notes_list:
            self.notes[note.id] = note

    # main functconsolens
    def add_note(self, id: str, title: str, content: str,
                    creatconsolen_date: str, last_modified_date: str) -> Note:

        note = Note(id, title, content, creatconsolen_date, last_modified_date)
        self.notes[id] = note
        return note
    
    def create_note(self, title: str, content: str) -> Note:
        note = self.add_note(self.generate_id(), title, content, self.now(), self.now())
        logger.debug("Persisting newly created note with ID: %s", note.id)
        storage.save_all_notes(self.get_notes_list())
        logger.info("Note created with ID: %s", note.id)
        return note
    
    def list_notes(self) -> list[Note]:
        notes_list = self.get_notes_list()
        logger.debug("Returning %d notes to the caller", len(notes_list))
        logger.info("Listing all notes: %d", len(notes_list))
        return notes_list

    def show_note(self, note: Note) -> str:
        logger.info("Displaying note with ID: %s", note.id)
        return(f"ID: {note.id}" + "\n" +
            f"Title: {note.title}" "\n" +
            f"Content: {note.content}" "\n" +
            f"Creation Date: {note.creation_date}" "\n" +
            f"Last Modified Date: {note.last_modified_date}")
            
    def update_note(self, note: Note, parameter: str, new_input: str) -> Note:
        allowed_fields = {"title", "content"}

        if parameter not in allowed_fields:
            raise errors.InvalidInput(f"Cannot update field: {parameter}")

        if not new_input.strip():
            raise errors.InvalidInput(f"{parameter} cannot be empty")

        logger.debug("Updating %s for note with ID: %s", parameter, note.id)
        setattr(note, parameter, new_input.strip())
        note.last_modified_date = self.now()
        storage.save_all_notes(self.get_notes_list())

        logger.info("Note with ID %s updated: %s", note.id, parameter,)
        return note

    def delete_note(self, note: Note):
        self.notes.pop(note.id)
        storage.save_all_notes(self.get_notes_list())
        logger.info("Note with ID: %s deleted", note.id)

        
    # helper functconsolens
    def now(self) -> str:
        return datetime.datetime.now(tz=ZoneInfo("Asia/Tehran")).isoformat()

    def generate_id(self) -> str:
        return str(uuid.uuid4())

    def find_note_by_id(self, id: str) -> Note:
        note = self.notes.get(id)
        if note is None:
            raise errors.NoteNotFoundError
        return note

    def get_notes_list(self) -> list[Note]:
        return list(self.notes.values())