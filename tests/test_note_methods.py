from note import models


def test_to_dict():
    note = models.Note(id= "test_id",
                        title="Test Note", content="This is a test note.",
                        creation_date="22/4/2026", last_modified_date="22/4/2026")
    expected_dict = {
        "id": "test_id",
        "title": "Test Note",
        "content": "This is a test note.",
        "creation_date": "22/4/2026",
        "last_modified_date": "22/4/2026"
    }
    assert note.to_dict() == expected_dict

def test_from_dict():
    data = {
        "id": "test_id",
        "title": "Test Note",
        "content": "This is a test note.",
        "creation_date": "22/4/2026",
        "last_modified_date": "22/4/2026"
    }
    note = models.Note.from_dict(data)
    assert note.id == "test_id"
    assert note.title == "Test Note"
    assert note.content == "This is a test note."
    assert note.creation_date == "22/4/2026"
    assert note.last_modified_date == "22/4/2026"

def test_note_equality():
    note1 = models.Note(id="test_id", title="Test Note 1", content="Content 1",
                        creation_date="22/4/2026", last_modified_date="22/4/2026")
    note2 = models.Note(id="test_id", title="Test Note 2", content="Content 2",
                        creation_date="22/4/2026", last_modified_date="22/4/2026")
    note3 = models.Note(id="different_id", title="Test Note 3", content="Content 3",
                        creation_date="22/4/2026", last_modified_date="22/4/2026")

    assert note1 == note2  # Same id, should be equal
    assert note1 != note3  # Different id, should not be equal