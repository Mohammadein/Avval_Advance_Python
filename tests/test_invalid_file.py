
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