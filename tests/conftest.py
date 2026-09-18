import pytest

from note.services import NoteManager


@pytest.fixture
def test_note_manager(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return NoteManager({})
