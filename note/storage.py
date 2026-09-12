from .models import Note
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