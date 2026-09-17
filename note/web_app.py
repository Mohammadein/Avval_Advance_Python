from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from note import dependencies


app = FastAPI()
template = Jinja2Templates(directory="note/templates")


@app.get("/notes" , response_class=HTMLResponse)
def list_notes(request: Request):
    note_manager = dependencies.get_note_manager()
    notes = note_manager.list_notes()
    return template.TemplateResponse(
        request=request,
        name="list_notes.html",
        context={"notes": notes},
        )

