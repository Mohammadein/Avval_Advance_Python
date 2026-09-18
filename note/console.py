import typer


# user_input 
def init_message() -> None:
    print("Hello")

def read_input(message: str | None = None) -> str:
    return typer.prompt(message if message else "Enter your input: ")

def read_multiline_input(message: str | None = None) -> str:
    print(message if message else "")
    lines: list[str] = []
    while True:
        try:
            if "END NOTE" in lines:
                lines.remove("END NOTE")
                break
            lines.append(typer.prompt(""))
        except EOFError:
            break
    return "\n".join(lines)

# output
def show_message(message: str) -> None:
    typer.echo(message)

def error(message: str | None = None) -> None:
    typer.echo("error: " + message if message else "Uknown error")

def exit_note_manager(message: str | None = None) -> None:
    typer.echo(message if message else "")
    typer.echo("Bye :)")

def confirm(message: str) -> bool:
    return typer.confirm(message)