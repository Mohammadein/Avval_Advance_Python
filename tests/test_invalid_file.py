
import json

import pytest

from note.services import NoteManager


def test_invalid_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    notes_file = tmp_path / "notes.json"
    notes_file.write_text("{bad json", encoding="utf-8")
    manager = NoteManager({})
    with pytest.raises(json.JSONDecodeError):
        manager.init()

def test_missing_field(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    notes_file = tmp_path / "notes.json"
    notes_file.write_text('{"title": "Test Note"}', encoding="utf-8")
    manager = NoteManager({})
    with pytest.raises(ValueError):
        manager.init()

def test_extra_field(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    notes_file = tmp_path / "notes.json"
    notes_file.write_text('{"title": "Test Note",'
    ' "content": "This is a test note.", "creation_date": "2023-01-01",' \
    ' "last_modified_date": "2023-01-01", "extra_field": "unexpected"}', encoding="utf-8")
    manager = NoteManager({})
    with pytest.raises(ValueError):
        manager.init()