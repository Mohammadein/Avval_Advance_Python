from note.services import NoteManager

manager = NoteManager({})
manager.init()

def get_note_manager() -> NoteManager:
    return manager