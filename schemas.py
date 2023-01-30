from __future__ import annotations

from pydantic import BaseModel


class Image(BaseModel):
    name = str
    image_size = int
    file_extension = str
    updated_at = str

    class Config:
        orm_mode = True
