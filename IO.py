from Note import Note
import json

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

# output
def write_note(note: Note):
    with open("notes.json", "a") as f:
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

def error(message: str | None = None) -> None:
    print("error: " + message if message else "Uknown error")