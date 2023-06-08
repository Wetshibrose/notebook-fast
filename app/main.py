from fastapi import FastAPI, status, HTTPException

# data
from .data import notes
from .schema import Note

app = FastAPI()


@app.get("/")
def root():
    data = {
        "message": "hello world",
    }
    return data


@app.get("/notes", status_code=status.HTTP_200_OK)
def get_notes():
    all_notes: list[Note] = notes
    return {"notes": all_notes}


@app.post("/notes", status_code=status.HTTP_200_OK)
def add_note(note: Note):
    if not note:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="note body required")
    notes.append(note)
    return {"note": note}


@app.get("/notes/{note_id}", status_code=status.HTTP_200_OK)
def get_note(note_id: str):
    if not note_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="note id is required",)
    note_id = note_id.replace("-", "")
    print(note_id)
    note: Note = None
    for note_v in notes:
        print(note_v.id.hex)
        if note_v.id.hex == note_id:
            note = note_v
            break

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="note not found",)

    return {"note": note}


@app.put("/notes/{note_id}", status_code=status.HTTP_200_OK)
def change_note(note_id: str, note: Note):
    if not note:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="bad format of the body")
    notes.append(note)
    return {"note": note}


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: str):
    if not note_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="note id is missing")

    note_id = note_id.replace("-", "")
    note_index: int = None
    for index, note in enumerate(notes):
        if note.id.hex == note_id:
            note_index = index
            break

    if not note_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"note with the given id {note_id} is not found")
    notes.pop(note_index)
