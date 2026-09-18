from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

import note.errors
import note.services
from note.errors import InvalidInput
from note.services import NoteManager


def test_create_note(test_note_manager):
    test_note_manager.create_note("Test Note", "This is a test note.")
    notes = test_note_manager.list_notes()
    assert len(notes) == 1
    assert notes[0].title == "Test Note"
    assert notes[0].content == "This is a test note."

def test_delete_note(test_note_manager):
    test_note_manager.create_note("Test Note", "This is a test note.")
    notes = test_note_manager.list_notes()
    test_note_manager.delete_note(notes[0])
    notes_after_deletion = test_note_manager.list_notes()
    assert len(notes_after_deletion) == 0

def test_update_note(test_note_manager, monkeypatch):
    monkeypatch.setattr(test_note_manager, "now", lambda: "2026-09-1")
    test_note_manager.create_note("Test Note", "This is a test note.")
    notes = test_note_manager.list_notes()
    monkeypatch.setattr(test_note_manager, "now", lambda: "2026-09-15")
    test_note_manager.update_note(notes[0], "content", "This is an updated note.")
    updated_notes = test_note_manager.list_notes()
    assert updated_notes[0].title == "Test Note"
    assert updated_notes[0].content == "This is an updated note."
    assert updated_notes[0].last_modified_date == "2026-09-15"
    assert updated_notes[0].creation_date == "2026-09-1"


def test_now_returns_tehran_timezone_aware_iso_timestamp(test_note_manager):
    timestamp = test_note_manager.now()
    parsed_timestamp = datetime.fromisoformat(timestamp)

    assert "T" in timestamp
    assert parsed_timestamp.tzinfo is not None
    assert parsed_timestamp.utcoffset() == datetime.now(
        tz=ZoneInfo("Asia/Tehran")
    ).utcoffset()

def test_cannot_update_note_id(test_note_manager):
    note = test_note_manager.create_note("Title", "Content")
    original_id = note.id

    with pytest.raises(InvalidInput):
        test_note_manager.update_note(note, "id", "changed-id")

    assert note.id == original_id
    assert list(test_note_manager.notes) == [original_id]

def test_list_notes(test_note_manager):
    test_note_manager.create_note("Note 1", "Content 1")
    test_note_manager.create_note("Note 2", "Content 2")
    notes = test_note_manager.list_notes()
    assert len(notes) == 2
    assert notes[0].title == "Note 1"
    assert notes[1].title == "Note 2"

def test_show_note(test_note_manager):
    test_note_manager.create_note("Test Note", "This is a test note.")
    notes = test_note_manager.list_notes()
    detail = test_note_manager.show_note(notes[0])
    note_to_show = test_note_manager.find_note_by_id(notes[0].id)
    assert note_to_show is not None
    assert detail == (f"ID: {note_to_show.id}" + "\n" +
            f"Title: {note_to_show.title}" "\n" +
            f"Content: {note_to_show.content}" "\n" +
            f"Creation Date: {note_to_show.creation_date}" "\n" +
            f"Last Modified Date: {note_to_show.last_modified_date}")
    
def test_search_notes(test_note_manager):
    note1 = test_note_manager.create_note("Note 1", "Content 1")
    note1_searched = test_note_manager.find_note_by_id(note1.id)
    assert note1_searched == note1
    with pytest.raises(note.errors.NoteNotFoundError):
        test_note_manager.find_note_by_id("nonexistent_id")

def test_unique_id_generation(test_note_manager):
    note1 = test_note_manager.create_note("Note 1", "Content 1")
    note2 = test_note_manager.create_note("Note 2", "Content 2")
    test_note_manager.delete_note(note1)
    note3 = test_note_manager.create_note("Note 3", "Content 3")
    assert note3.id != note2.id

def test_load_after_save(test_note_manager):
    test_note_manager.create_note("Note 1", "Content 1")
    test_note_manager.create_note("Note 2", "Content 2")
    notes_before_reload = test_note_manager.list_notes()
    new_manager = NoteManager({})
    new_manager.init()
    notes_after_reload = new_manager.list_notes()
    assert len(notes_after_reload) == len(notes_before_reload) == 2
    for note_before, note_after in zip(notes_before_reload, notes_after_reload):
        assert note_after is not note_before
        assert note_before.id == note_after.id
        assert note_before.title == note_after.title
        assert note_before.content == note_after.content
        assert note_before.creation_date == note_after.creation_date
        assert note_before.last_modified_date == note_after.last_modified_date


def test_create_note_keeps_memory_unchanged_when_save_fails(
    test_note_manager, monkeypatch
):
    def fail_to_save(notes):
        raise PermissionError

    monkeypatch.setattr(note.services.storage, "save_all_notes", fail_to_save)

    with pytest.raises(PermissionError):
        test_note_manager.create_note("Title", "Content")

    assert test_note_manager.list_notes() == []


def test_update_note_keeps_memory_unchanged_when_save_fails(
    test_note_manager, monkeypatch
):
    created_note = test_note_manager.create_note("Original title", "Original content")

    def fail_to_save(notes):
        raise PermissionError

    monkeypatch.setattr(note.services.storage, "save_all_notes", fail_to_save)

    with pytest.raises(PermissionError):
        test_note_manager.update_note(created_note, "title", "Updated title")

    assert created_note.title == "Original title"
    assert test_note_manager.find_note_by_id(created_note.id).title == "Original title"


def test_delete_note_keeps_memory_unchanged_when_save_fails(
    test_note_manager, monkeypatch
):
    created_note = test_note_manager.create_note("Title", "Content")

    def fail_to_save(notes):
        raise PermissionError

    monkeypatch.setattr(note.services.storage, "save_all_notes", fail_to_save)

    with pytest.raises(PermissionError):
        test_note_manager.delete_note(created_note)

    assert test_note_manager.find_note_by_id(created_note.id) is created_note
