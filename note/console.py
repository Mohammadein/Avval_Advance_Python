from .models import Note

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