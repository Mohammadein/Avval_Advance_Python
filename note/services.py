from enum import Enum
import uuid
from .models import Note
from Config import Config
from datetime import date
from . import storage
from . import console

class input_type(Enum):
    one_line = 0
    multi_line = 1

create_note_command = "create note"
list_notes_command = "list notes"
read_note_by_id_command = "read note"
update_note_by_id_command = "update note"
delete_note_by_id_command = "delete note"
note_parameters = {
    "title": input_type.one_line,
    "content": input_type.multi_line
    }

class NoteManager:
    def __init__(self, notes: dict[str, Note], config: Config | None = None) -> None:
        self.notes = notes
        self.config = config

    def init(self) -> None:
        self.load_notes()
        self.config = storage.load_config()
        console.init_message()
        while True:
            try:
                user_input : str = console.read_input()
                self.pars_input(user_input)
            except EOFError:
                console.exit_note_manager()
                break

    def load_notes(self) -> None:
        notes_list = storage.load_notes()
        for note in notes_list:
            self.notes[note.id] = note

    def pars_input(self , user_input : str) -> None:
        if create_note_command in user_input: self.handle_create_note(user_input)
        elif list_notes_command in user_input: self.handle_list_note(user_input)
        elif read_note_by_id_command in user_input: self.handle_show_note(user_input)
        elif update_note_by_id_command in user_input: self.handle_update_note(user_input)
        elif delete_note_by_id_command in user_input: self.handle_delete_note(user_input)
        else : console.error("command note found")

    # handlers
    def handle_create_note(self, user_input: str) -> None:
        values = {}

        for parameter in note_parameters:
            if (note_parameters[parameter] is input_type.one_line):
                values[parameter] = console.read_input(parameter)
            else:
                values[parameter] = console.read_multiline_input(parameter)

        note = self.create_note(
            id=self.generate_id(),
            title=values["title"],
            content=values["content"],
            creatconsolen_date=self.today(),
            last_modified_date= self.today()
        )

        console.show_message("note created with ID: " + str(note.id))

    def handle_list_note(self, user_input: str) -> None:
        self.list_notes()

    def handle_show_note(self, user_input: str) -> None:
        try:
            note_id = self.extract_note_id(user_input, 2)
        except ValueError as e:
            console.error(str(e))
            return
        self.show_note_by_id(note_id)

    def handle_update_note(self, user_input: str) -> None:
        try:
            note_id = self.extract_note_id(user_input, 2)
        except ValueError as e:
            console.error(str(e))
            return
        
        note = self.show_note_by_id(note_id)
        if note is None:
            return

        i = console.read_input("which one do you want to change? " + self.note_parameters_str())
        for parameter in note_parameters:
            if i == parameter:
                self.update_note(note, parameter)
                break
        else:
            console.error("invalid input")

    def handle_delete_note(self, user_input: str) -> None:
        try:
            note_id = self.extract_note_id(user_input, 2)
        except ValueError as e:
            console.error(str(e))
            return
        note = self.find_note_by_id(note_id)
        if note is None:
            console.error("note not found")
            return None

        if (self.last_check("Are u sure u want to delete note with id " + note_id)):
            self.delete_note(note)
            console.show_message("note deleted with ID: " + str(note.id))

    # main functconsolens
    def add_note(self, id: str, title: str, content: str,
                    creatconsolen_date: str, last_modified_date: str) -> Note:

        note = Note(id, title, content, creatconsolen_date, last_modified_date)
        self.notes[id] = note
        return note
    
    def create_note(self, id: str, title: str, content: str,
                    creatconsolen_date: str, last_modified_date: str) -> Note:

        note = self.add_note(id, title, content, creatconsolen_date, last_modified_date)
        storage.write_note(note)
        return note
    
    def list_notes(self) -> list[Note]:
        notes_list = self.get_notes_list()

        console.note_list_show(notes_list)
        return notes_list

    def show_note_by_id(self, id: str) -> Note | None:
        note = self.find_note_by_id(id)
        if note is None:
            console.error("note not found")
            return None

        console.note_show(note)
        return note

    def update_note(self, note: Note, parameter: str) -> Note | None:
        i = console.read_input("enter new " + parameter)
        setattr(note, parameter, i)
        note.last_modified_date = self.today()
        self.notes[note.id] = note
        storage.save_all_notes(self.get_notes_list())
        return note

    def delete_note(self, note: Note):
        self.notes.pop(note.id)
        storage.save_all_notes(self.get_notes_list())

        
    # helper functconsolens
    def today(self) -> str:
        return date.today().isoformat()

    def generate_id(self) -> str:
        return str(uuid.uuid4())
        

    def extract_note_id(self, user_input: str , index: int) -> str:
        word_list = user_input.split()

        try:
            return word_list[index]
        except:
            raise ValueError ("invalid id")

    def note_parameters_str(self) -> str:
        parameters: list[str] = []
        for parameter in note_parameters:
            parameters.append(parameter)

        return ", ".join(parameters)

    def find_note_by_id(self, id: str) -> Note | None:
        return self.notes.get(id)      

    def get_notes_list(self) -> list[Note]:
        return list(self.notes.values())

    def last_check(self, message: str = "are u sure?") -> bool:
        i = console.read_input(message)
        if i == "y" or i == "Y" or i == "yes" or i == "Yes":
            return True
        elif i == "n" or i == "N" or i == "no" or i == "No":
            return False
        else:
            console.error("invalid input")
            return False