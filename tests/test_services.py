from note.services import NoteManager


def test_new_manager_has_no_notes():
    manager = NoteManager({})
    notes = manager.list_notes()
    assert notes == []


def test_load_notes_when_file_missing(test_note_manager, tmp_path):
    assert not (tmp_path / "notes.json").exists()

    test_note_manager.init()

    assert test_note_manager.list_notes() == []
