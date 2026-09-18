from note.services import NoteManager

_manager: NoteManager | None = None

def get_note_manager() -> NoteManager:
    global _manager

    if _manager is None:
        manager = NoteManager({})
        manager.init()
        _manager = manager

    return _manager