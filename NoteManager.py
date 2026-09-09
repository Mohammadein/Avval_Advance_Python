from Note import Note
from datetime import date
import IO

add_note_command = "add note"
create_note_command = "create note"
list_notes_command = "list notes"
read_note_by_id_command = "read note"
note_parameters = ["title", "content"]

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
        if user_input == add_note_command: self.handle_create_note()
        elif user_input == list_notes_command: self.handle_list_note()
        else : IO.error()

    def handle_create_note(self) -> None:
        values = {}

        for parameter in note_parameters:
            values[parameter] = IO.read_input(parameter)
        
        note = self.create_note(
            id=len(self.notes) + 1,
            title=values["title"],
            content=values["content"],
            creation_date=self.today(),
            last_modified_date= self.today()
        )

    def handle_list_note(self) -> None:
        IO.note_list_show(self.notes)
        
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


    def today(self) -> str:
        return date.today().isoformat()