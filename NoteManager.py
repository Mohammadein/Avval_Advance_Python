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
update_note_by_id_command = "update note"
note_parameters = {
    "title": input_type.one_line,
    "content": input_type.multi_line
    }

class NoteManager:
    def __init__(self, notes: dict[int, Note]) -> None:
        self.notes = notes

    def init(self) -> None:
        self.load_notes()
        IO.init_message()
        while True:
            user_input : str = IO.read_input()
            self.pars_input(user_input)

    def load_notes(self) -> None:
        notes_list = IO.load_notes()
        for note in notes_list:
            self.notes[note.id] = note

    def pars_input(self , user_input : str) -> None:
        if create_note_command in user_input: self.handle_create_note(user_input)
        elif list_notes_command in user_input: self.handle_list_note(user_input)
        elif read_note_by_id_command in user_input: self.handle_show_note(user_input)
        elif update_note_by_id_command in user_input: self.handle_update_note(user_input)
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
        self.list_notes()

    def handle_show_note(self, user_input: str) -> None:
        note_id = self.extract_note_id(user_input, 2)
        self.show_note_by_id(note_id)

    def handle_update_note(self, user_input: str) -> None:
        note_id = self.extract_note_id(user_input, 2)
        if self.show_note_by_id(note_id) is None:
            return

        i = IO.read_input("which one do you want to change? " + self.note_parameters_str())
        for parameter in note_parameters:
            if i == parameter:
                self.update_note_by_id(note_id, parameter)
                break
        else:
            IO.error("invalid input")

    # main functions
    def add_note(self, id: int, title: str, content: str,
                    creation_date: str, last_modified_date: str) -> Note:

        note = Note(id, title, content, creation_date, last_modified_date)
        self.notes[id] = note
        return note
    
    def create_note(self, id: int, title: str, content: str,
                    creation_date: str, last_modified_date: str) -> Note:

        note = self.add_note(id, title, content, creation_date, last_modified_date)
        IO.write_note(note)
        return note
    
    def list_notes(self) -> list[Note]:
        notes_list = list(self.notes.values())

        IO.note_list_show(notes_list)
        return notes_list

    def show_note_by_id(self, id: int) -> Note | None:
        note = self.find_note_by_id(id)
        if note is None:
            IO.error("note not found")
            return None

        IO.note_show(note)
        return note

    def update_note_by_id(self, note_id: int, parameter: str) -> Note | None:
        note = self.find_note_by_id(note_id)
        if note is None:
            IO.error("note not found")
            return None

        i = IO.read_input("enter new " + parameter)
        setattr(note, parameter, i)
        note.last_modified_date = self.today()
        self.notes[note_id] = note
        return note

    # helper functions
    def today(self) -> str:
        return date.today().isoformat()

    def extract_note_id(self, user_input: str , index: int) -> int:
        word_list = user_input.split()

        try:
            return int(word_list[index])
        except:
            IO.error("incorrect input")
            return -1

    def note_parameters_str(self) -> str:
        parameters: list[str] = []
        for parameter in note_parameters:
            parameters.append(parameter)

        return ", ".join(parameters)

    def find_note_by_id(self, id: int) -> Note | None:
        return self.notes.get(id)       