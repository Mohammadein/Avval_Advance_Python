class Note:
    def __init__(self, id: str, title: str, content: str,
                    creation_date: str, last_modified_date: str) -> None:

        self.id = id
        self.title = title
        self.content = content
        self.creation_date = creation_date
        self.last_modified_date = last_modified_date

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Note):
            return NotImplemented
        return self.id == value.id
     
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "creation_date": self.creation_date,
            "last_modified_date": self.last_modified_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Note':
        return cls(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            creation_date=data["creation_date"],
            last_modified_date=data["last_modified_date"]
        )