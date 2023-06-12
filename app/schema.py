from pydantic import BaseModel, Field

import uuid
from datetime import datetime


class Author(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = None


class Note(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str = Field(default="Default Head")
    text: str
    author: Author
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = None
