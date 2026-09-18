from pathlib import Path

from note import web_app


def test_templates_directory_is_package_relative():
    expected_directory = Path(web_app.__file__).resolve().parent / "templates"

    assert web_app.TEMPLATES_DIR == expected_directory
    assert web_app.TEMPLATES_DIR.is_dir()
    assert web_app.template.env.get_template("base.html") is not None
