import logging

from note.services import NoteManager


def test_new_manager_has_no_notes():
    manager = NoteManager({})
    notes = manager.list_notes()
    assert notes == []


def test_list_notes_logs_debug_message(test_note_manager, caplog):
    with caplog.at_level(logging.DEBUG, logger="note.services"):
        test_note_manager.list_notes()

    assert "Returning 0 notes to the caller" in caplog.messages


def test_load_notes_when_file_missing(test_note_manager, tmp_path):
    assert not (tmp_path / "notes.json").exists()

    test_note_manager.init()

    assert test_note_manager.list_notes() == []
