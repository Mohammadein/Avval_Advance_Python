from enum import Enum
from Note import Note
from datetime import date
import IO

class input_type(Enum):
    one_line = 0
    multi_line = 1

create_note_command = "create note"
list_notes_command = "list notes"
read_note_by_id_command = "read note"
note_parameters = {
    "title": input_type.one_line,
    "content": input_type.multi_line
    }

class NoteManager:
    def __init__(self, notes: list[Note]) -> None:
        self.notes = notes

    def init(self) -> None:
        self.load_notes()
        IO.init_message()
        while True:
            user_input : str = IO.read_input()
            self.pars_input(user_input)

    def load_notes(self) -> None:
        self.notes = IO.load_notes()

    def pars_input(self , user_input : str) -> None:
        if create_note_command in user_input: self.handle_create_note(user_input)
        elif list_notes_command in user_input: self.handle_list_note(user_input)
        elif read_note_by_id_command in user_input: self.handle_show_note(user_input)
        else : IO.error("command note found")

    # handlers
    def handle_create_note(self, user_input: str) -> None:
        values = {}

        for parameter in note_parameters:
            if (note_parameters[parameter] is input_type.one_line):
                values[parameter] = IO.read_input(parameter)
            else:
                values[parameter] = IO.read_multiline_input(parameter)
                
        note = self.create_note(
            id=len(self.notes) + 1,
            title=values["title"],
            content=values["content"],
            creation_date=self.today(),
            last_modified_date= self.today()
        )

        IO.show_message("note created with ID: " + str(note.id))

    def handle_list_note(self, user_input: str) -> None:
        IO.note_list_show(self.notes)

    def handle_show_note(self, user_input: str) -> None:
        word_list = user_input.split()
        note_id : int

        try:
            note_id = int(word_list[2])
        except:
            IO.error("incorrect input")

        note = self.find_note_by_id(note_id)
        IO.note_show(note) if note else IO.error("note wasn't found")


    # main functions
    def add_note(self, id: int, title: str, content: str,
                    creation_date: str, last_modified_date: str) -> Note:

        note = Note(id, title, content, creation_date, last_modified_date)
        self.notes.append(note)
        return note
    
    def create_note(self, id: int, title: str, content: str,
                    creation_date: str, last_modified_date: str) -> Note:

        note = self.add_note(id, title, content, creation_date, last_modified_date)
        IO.write_note(note)
        return note
    
    def list_notes(self) -> list[Note]:
        IO.note_list_show(self.notes)
        return self.notes

    def read_note_by_id(self, id: int) -> Note:
        IO.note_show(self.notes[id])
        return self.notes[id]


    # helper functions
    def today(self) -> str:
        return date.today().isoformat()

    def find_note_by_id(self, id: int) -> Note | None:
        return next((note for note in self.notes if note.id == id), None)