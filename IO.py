from Note import Note
from Config import Config
import json

def load_config() -> Config:
    config = Config(id_counter=0)
    try:
        with open("config.json", "r") as c:
            config = Config(**json.load(c))
    except FileNotFoundError:
        pass

    return config

def save_config(config: Config) -> None:
    try:
        with open("config.json", "w") as c:
            json.dump(config.__dict__, c)
            
    except FileNotFoundError:
        pass

def load_notes() -> list[Note]:
    notes: list[Note] = []
    try:
        with open("notes.json", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                notes.append(Note(**json.loads(line)))
    except FileNotFoundError:
        pass
    return notes

# user_input 
def init_message() -> None:
    print("Hello")

def read_input(message: str | None = None) -> str:
    i : str = input((message + ": ") if message else "")
    return i

def read_multiline_input(message: str | None = None) -> str:
    print(message if message else "")
    lines: list[str] = []
    while True:
        try:
            if "END NOTE" in lines:
                lines.remove("END NOTE")
                break
            lines.append(input())
        except EOFError:
            break
    return "\n".join(lines)

# output
def write_note(note: Note):
    with open("notes.json", "a") as f:
        json.dump(note.__dict__, f)
        f.write("\n")

def save_all_notes(notes: list[Note]):
    with open("notes.json", "w") as f:
        for note in notes:
            json.dump(note.__dict__, f)
            f.write("\n")

def note_list_show(notes: list[Note]):
    for note in notes:
        print(f"{note.id}: {note.title}")

def note_show(note: Note):
    print(f"ID: {note.id}")
    print(f"Title: {note.title}")
    print(f"Content: {note.content}")
    print(f"Creation Date: {note.creation_date}")
    print(f"Last Modified Date: {note.last_modified_date}")

def show_message(message: str) -> None:
    print(message)

def error(message: str | None = None) -> None:
    print("error: " + message if message else "Uknown error")

def exit_note_manager(message: str | None = None) -> None:
    print(message if message else "")
    print("Bye :)")