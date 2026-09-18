
import json

import pytest

from note import errors
from note.services import NoteManager


def test_invalid_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    notes_file = tmp_path / "notes.json"
    notes_file.write_text("{bad json", encoding="utf-8")
    manager = NoteManager({})
    with pytest.raises(errors.InvalidNote):
        manager.init()

def test_missing_field(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    notes_file = tmp_path / "notes.json"
    notes_file.write_text(
        json.dumps([{"title": "Test Note"}]),
        encoding="utf-8",
    )
    manager = NoteManager({})
    with pytest.raises(errors.InvalidNote, match="Missing note fields"):
        manager.init()

def test_extra_field(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    notes_file = tmp_path / "notes.json"
    notes_file.write_text(
        json.dumps([
            {
                "id": "test_id",
                "title": "Test Note",
                "content": "This is a test note.",
                "creation_date": "2023-01-01",
                "last_modified_date": "2023-01-01",
                "extra_field": "unexpected",
            }
        ]),
        encoding="utf-8",
    )
    manager = NoteManager({})
    with pytest.raises(errors.InvalidNote, match="Unexpected note fields"):
        manager.init()


def test_invalid_field_type(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    notes_file = tmp_path / "notes.json"
    notes_file.write_text(
        json.dumps(
            [
                {
                    "id": 123,
                    "title": "Test Note",
                    "content": "This is a test note.",
                    "creation_date": "2023-01-01",
                    "last_modified_date": "2023-01-01",
                }
            ]
        ),
        encoding="utf-8",
    )
    manager = NoteManager({})

    with pytest.raises(errors.InvalidNote, match="Invalid field types: id"):
        manager.init()


def test_duplicate_note_id(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    notes_file = tmp_path / "notes.json"
    note = {
        "id": "duplicate-id",
        "title": "First note",
        "content": "First content",
        "creation_date": "2023-01-01",
        "last_modified_date": "2023-01-01",
    }
    notes_file.write_text(
        json.dumps([note, {**note, "title": "Second note"}]),
        encoding="utf-8",
    )
    manager = NoteManager({})

    with pytest.raises(errors.InvalidNote, match="Duplicate note id: duplicate-id"):
        manager.init()
