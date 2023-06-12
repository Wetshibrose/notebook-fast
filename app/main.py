from fastapi import FastAPI, status, HTTPException



# data
from .data import notes
from .schema import Note
from .db_raw import (
    instantiate_db,
    get_notes_db,
    add_note_db,
    get_note_db,
    delete_note_db,
    change_note_db
)

app = FastAPI()

# instantiate db and tables
instantiate_db()


@app.get("/", status_code=status.HTTP_200_OK)
def get_notes():
    all_notes = get_notes_db()
    return {"data": all_notes}


@app.get("/notes", status_code=status.HTTP_200_OK)
def get_notes():
    all_notes = get_notes_db()
    return {"data": all_notes}


@app.post("/notes", status_code=status.HTTP_200_OK)
def add_note(note: Note):
    if not note:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="note body required")
    new_note = add_note_db(note=note)
    if isinstance(new_note, str) or new_note is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{new_note}")

    return {"data": new_note}


@app.get("/notes/{note_id}", status_code=status.HTTP_200_OK)
def get_note(note_id: str):
    if not note_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="note id is required",)

    note: Note = get_note_db(id=note_id)
    if isinstance(note, str) or note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{note}",)

    return {"data": note}


@app.put("/notes/{note_id}", status_code=status.HTTP_200_OK)
def change_note(note_id: str, note: Note):
    if not note:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="bad format of the body")
    note = change_note_db(note=note)
    if isinstance(note, str):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{note}",)

    return {"note": note}


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: str):
    if not note_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="note id is missing")

    note = delete_note_db(id=note_id)
    if isinstance(note, str):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{note}")
