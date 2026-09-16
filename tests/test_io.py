from note import IO


def test_input_functions_delegate_to_console(monkeypatch):
    monkeypatch.setattr(IO.console, "read_input", lambda message: f"input:{message}")
    monkeypatch.setattr(
        IO.console,
        "read_multiline_input",
        lambda message: f"multiline:{message}",
    )

    assert IO.read_input("Title") == "input:Title"
    assert IO.read_multiline_input("Content") == "multiline:Content"


def test_output_functions_delegate_to_console(monkeypatch):
    calls = []
    monkeypatch.setattr(IO.console, "show_message", lambda message: calls.append(("show", message)))
    monkeypatch.setattr(IO.console, "error", lambda message: calls.append(("error", message)))

    IO.show_message("Done")
    IO.error("Failed")

    assert calls == [("show", "Done"), ("error", "Failed")]


def test_confirm_delegates_to_console(monkeypatch):
    monkeypatch.setattr(IO.console, "confirm", lambda message: message == "Continue?")

    assert IO.confirm("Continue?") is True

