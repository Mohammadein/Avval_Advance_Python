from note import cli_io


def test_input_functions_delegate_to_console(monkeypatch):
    monkeypatch.setattr(cli_io.console, "read_input", lambda message: f"input:{message}")
    monkeypatch.setattr(
        cli_io.console,
        "read_multiline_input",
        lambda message: f"multiline:{message}",
    )

    assert cli_io.read_input("Title") == "input:Title"
    assert cli_io.read_multiline_input("Content") == "multiline:Content"


def test_output_functions_delegate_to_console(monkeypatch):
    calls = []
    monkeypatch.setattr(cli_io.console, "show_message", lambda message: calls.append(("show", message)))
    monkeypatch.setattr(cli_io.console, "error", lambda message: calls.append(("error", message)))

    cli_io.show_message("Done")
    cli_io.error("Failed")

    assert calls == [("show", "Done"), ("error", "Failed")]


def test_confirm_delegates_to_console(monkeypatch):
    monkeypatch.setattr(cli_io.console, "confirm", lambda message: message == "Continue?")

    assert cli_io.confirm("Continue?") is True

