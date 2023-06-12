import psycopg2
from psycopg2.extras import RealDictCursor

from typing import Any

import time

# env
from decouple import config

from .schema import Note


def connect_db(host: str, dbname: str, user: str, password: str) -> Any:
    while True:
        try:
            global conn
            conn = psycopg2.connect(host=host, database=dbname, user=user,
                                    password=password, cursor_factory=RealDictCursor,)
            print("Successfully connected to db")

            break
        except Exception as error:
            print("Error occurred while connecting to db ", error)
            time.sleep(2)

####### NOTES TABLE ######


def create_table_note():
    query = """
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    CREATE TABLE IF NOT EXISTS note (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        title VARCHAR(150),
        comment TEXT,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        is_deleted BOOLEAN NOT NULL DEFAULT false
    );
    """
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        print("Note table successfully created")
    except Exception as error:
        print("Error creating note table", error)


def update_column_table_note(col_name: str, desired_name: str, desired_type: str, drop_column: bool = False):
    if drop_column:
        drop_column_table_note(col_name=col_name)
        return

    rename_column_table_note(col_name=col_name, desired_name=desired_name)


def drop_column_table_note(col_name: str):
    query = f"""
    ALTER TABLE note 
    DROP COLUMN {col_name};
    """

    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        print(f"column {col_name} successfully deleted")
        return
    except Exception as error:
        print("Error deleting column")
        return


def rename_column_table_note(col_name: str, desired_name: str):
    query = f"""
    ALTER TABLE note 
    RENAME COLUMN {col_name} TO {desired_name};
    """

    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        print(f"column {col_name} successfully changed")
        return
    except Exception as error:
        print("Error editing column")
        return


def get_notes_db() -> list[tuple] | None:
    query = """
    SELECT * FROM note
    WHERE is_deleted = false
    ORDER BY updated_at 
    DESC;
    """

    cursor = conn.cursor()
    try:
        cursor.execute(query)
        notes = cursor.fetchall()
        print(f"notes: {notes}")
        return notes
    except Exception as error:
        print("Error retrieving notes", error)
        return None


def add_note_db(note: Note) -> tuple | str:
    query = """
    INSERT INTO note (title, comment) VALUES (%s, %s) 
    RETURNING *;
    """
    data = (note.title, note.text)
    cursor = conn.cursor()

    try:
        cursor.execute(query, data)
        print(f"Added a note successfully")
        conn.commit()
        new_note = cursor.fetchone()
        return new_note
    except Exception as error:
        print("Error occured adding a note ", error)
        return f"{error}"


def get_note_db(id: str) -> tuple | str:
    query = """
    SELECT * FROM note
    WHERE id = %s;
    """
    data = (id,)

    cursor = conn.cursor()
    try:
        cursor.execute(query, data)
        conn.commit()
        new_note = cursor.fetchone()
        print(f"Found note of id {id}")
        return new_note
    except Exception as error:
        print("Error occured searching note ", error)
        return f"{error}"


def change_note_db(note: Note) -> tuple | str:
    query = """
    UPDATE note
    SET title = %s, comment = %s
    WHERE id = %s
    RETURNING *;
    """
    data = (note.title, note.text, note.id.hex)

    cursor = conn.cursor()
    try:
        cursor.execute(query, data)
        conn.commit()
        new_note = cursor.fetchone()
        print(f"Found note of id {id}")
        return new_note

    except Exception as error:
        print("Error occured updating note ", error)
        return f"{error}"


def delete_note_db(id: str) -> None | str:
    # query = """
    # DELETE FROM note
    # WHERE id = %s;
    # """
    query = """
    UPDATE note
    SET is_deleted = %s
    WHERE id = %s;
    """
    data = (True, id)

    cursor = conn.cursor()
    try:
        cursor.execute(query, data)
        conn.commit()
        print(f"Deleted note successfully")
        return None
    except Exception as error:
        print("Error occured deleting note ", error)
        return f"{error}"

####### END NOTES TABLE ######


def instantiate_db():
    connect_db(host=config("DB_HOST", cast=str), dbname=config(
        "DB_DATABASE", cast=str), user=config("DB_USER", cast=str), password=config("DB_PASSWORD", cast=str))
    time.sleep(2)
    create_table_note()
