from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from database import BookDatabaseManager

app = FastAPI(title="Book Data Pipeline API")
db = BookDatabaseManager("books.db")


class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)
    in_stock: str = Field(..., min_length=1)
    rating: int = Field(..., ge=1, le=5)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    price: Optional[float] = Field(default=None, ge=0)
    in_stock: Optional[str] = Field(default=None, min_length=1)
    rating: Optional[int] = Field(default=None, ge=1, le=5)


@app.get("/books")
def get_books() -> list[dict]:
    return db.get_all_books()


@app.get("/books/{book_id}")
def get_book(book_id: int) -> dict:
    book = db.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate) -> dict:
    book_id = db.insert_book(book.model_dump())
    created = db.get_book_by_id(book_id)
    return created if created is not None else {"id": book_id, **book.model_dump()}


@app.put("/books/{book_id}")
def update_book(book_id: int, updates: BookUpdate) -> dict:
    updated_book = db.update_book(book_id, updates.model_dump(exclude_unset=True))
    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return updated_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int) -> dict:
    deleted = db.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return {"message": "Book deleted successfully"}