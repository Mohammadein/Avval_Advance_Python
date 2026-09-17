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