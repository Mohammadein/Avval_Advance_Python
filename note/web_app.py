from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from note import dependencies


app = FastAPI()
template = Jinja2Templates(directory="note/templates")

@app.get("/")
def home():
    return RedirectResponse(url="/notes")

@app.get("/notes" , response_class=HTMLResponse)
def list_notes(request: Request):
    note_manager = dependencies.get_note_manager()
    notes = note_manager.list_notes()
    return template.TemplateResponse(
        request=request,
        name="list_notes.html",
        context={"notes": notes},
        )

@app.get("/notes/new", response_class=HTMLResponse)
def show_create_note_form(request: Request):
    return template.TemplateResponse(
        request=request,
        name="create_note.html",
        context={},
    )

@app.post("/notes")
def create_note(title: str = Form(), content: str = Form()):
    note_manager = dependencies.get_note_manager()
    note_manager.create_note(title, content)

    return RedirectResponse(url="/notes" , status_code=303)

@app.get("/notes/{note_id}/edit", response_class=HTMLResponse)
def show_edit_note_form(request: Request, note_id: str):
    note_manager = dependencies.get_note_manager()
    try:
        note = note_manager.find_note_by_id(note_id)
    except Exception:
        return RedirectResponse(url="/notes")
    return template.TemplateResponse(
        request=request,
        name="update_note.html",
        context={"note": note},
    )

@app.post("/notes/{note_id}/edit")
def update_note(note_id: str, parameter: str = Form(), new_input: str = Form()):
    note_manager = dependencies.get_note_manager()
    try:
        note = note_manager.find_note_by_id(note_id)
    except Exception:
        return RedirectResponse(url="/notes")
    note_manager.update_note(note, parameter, new_input)
    return RedirectResponse(url="/notes", status_code=303)

@app.get("/notes/{note_id}/delete", response_class=HTMLResponse)
def show_delete_note_confirm(request: Request, note_id: str):
    note_manager = dependencies.get_note_manager()
    try:
        note = note_manager.find_note_by_id(note_id)
    except Exception:
        return RedirectResponse(url="/notes", status_code=303)
    return template.TemplateResponse(
        request=request,
        name="delete_note.html",
        context={"note": note},
    )

@app.post("/notes/{note_id}/delete")
def delete_note(note_id: str):
    note_manager = dependencies.get_note_manager()
    try:
        note = note_manager.find_note_by_id(note_id)
    except Exception:
        return RedirectResponse(url="/notes", status_code=303)
    if note:
        note_manager.delete_note(note)
    return RedirectResponse(url="/notes", status_code=303)

@app.get("/notes/{note_id}", response_class=HTMLResponse)
def show_note(request: Request, note_id: str):
    note_manager = dependencies.get_note_manager()
    try:
        note = note_manager.find_note_by_id(note_id)
    except Exception:
        return RedirectResponse(url="/notes", status_code=303)
    return template.TemplateResponse(
        request=request,
        name="show_note.html",
        context={"note": note},
    )