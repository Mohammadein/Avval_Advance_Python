from . import console

def read_input(message: str | None = "Enter your input") -> str:
    return console.read_input(message)

def read_multiline_input(message: str | None = "Enter your input") -> str:
    return console.read_multiline_input(message)

def show_message(message: str) -> None:
    console.show_message(message)

def confirm(message: str) -> bool:
    return console.confirm(message)