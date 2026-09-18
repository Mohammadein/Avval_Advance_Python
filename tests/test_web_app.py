from pathlib import Path

from fastapi import Request

from note import errors, web_app


def test_templates_directory_is_package_relative():
    expected_directory = Path(web_app.__file__).resolve().parent / "templates"

    assert web_app.TEMPLATES_DIR == expected_directory
    assert web_app.TEMPLATES_DIR.is_dir()
    assert web_app.template.env.get_template("base.html") is not None


def test_invalid_input_handler_returns_bad_request():
    request = Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/notes/example/edit",
            "headers": [],
        }
    )

    response = web_app.invalid_input_handler(request, errors.InvalidInput())

    assert response.status_code == 400
    assert response.body == b"Invalid input"
