from .models import Note
from Config import Config
from . import errors
import json

@errors.handle_file_errors
def load_config() -> Config:
    config = Config(id_counter=0)
    with open("config.json", "r") as c:
        config = Config(**json.load(c))
    return config

@errors.handle_file_errors
def save_config(config: Config) -> None:
    with open("config.json", "w") as c:
        json.dump(config.__dict__, c)

@errors.handle_file_errors
def load_notes() -> list[Note]:
    notes: list[Note] = []
    with open("notes.json", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            notes.append(Note(**json.loads(line)))
    return notes

# output
@errors.handle_file_errors
def write_note(note: Note):
    with open("notes.json", "a") as f:
        json.dump(note.__dict__, f)
        f.write("\n")

@errors.handle_file_errors  
def save_all_notes(notes: list[Note]):
    with open("notes.json", "w") as f:
        for note in notes:
            json.dump(note.__dict__, f)
            f.write("\n")