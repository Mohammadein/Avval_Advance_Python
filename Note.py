class Note:
    def __init__(self, id: int, title: str, content: str,
                    creation_date: str, last_modified_date: str) -> None:

        self.id = id
        self.title = title
        self.content = content
        self.creation_date = creation_date
        self.last_modified_date = last_modified_date