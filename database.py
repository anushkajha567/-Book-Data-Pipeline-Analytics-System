from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


class BookDatabaseManager:
    def __init__(self, db_path: str = "books.db") -> None:
        self.db_path = Path(db_path)
        self._ensure_parent_directory()
        self._initialize_database()

    def _ensure_parent_directory(self) -> None:
        if self.db_path.parent and self.db_path.parent != Path(""):
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    price REAL NOT NULL,
                    in_stock TEXT NOT NULL,
                    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5)
                )
                """
            )
            connection.commit()

    def clear_books(self) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM books")
            connection.commit()

    def insert_book(self, book: Dict[str, Any]) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO books (title, price, in_stock, rating)
                VALUES (?, ?, ?, ?)
                """,
                (book["title"], float(book["price"]), book["in_stock"], int(book["rating"])),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def insert_books(self, books: List[Dict[str, Any]]) -> List[int]:
        inserted_ids: List[int] = []
        with self._connect() as connection:
            for book in books:
                cursor = connection.execute(
                    """
                    INSERT INTO books (title, price, in_stock, rating)
                    VALUES (?, ?, ?, ?)
                    """,
                    (book["title"], float(book["price"]), book["in_stock"], int(book["rating"])),
                )
                inserted_ids.append(int(cursor.lastrowid))
            connection.commit()
        return inserted_ids

    def get_all_books(self) -> List[Dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute("SELECT id, title, price, in_stock, rating FROM books ORDER BY id").fetchall()
        return [dict(row) for row in rows]

    def get_book_by_id(self, book_id: int) -> Optional[Dict[str, Any]]:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT id, title, price, in_stock, rating FROM books WHERE id = ?",
                (book_id,),
            ).fetchone()
        return dict(row) if row else None

    def update_book(self, book_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        current = self.get_book_by_id(book_id)
        if current is None:
            return None

        updated = {
            "title": updates.get("title", current["title"]),
            "price": float(updates.get("price", current["price"])),
            "in_stock": updates.get("in_stock", current["in_stock"]),
            "rating": int(updates.get("rating", current["rating"])),
        }

        with self._connect() as connection:
            connection.execute(
                """
                UPDATE books
                SET title = ?, price = ?, in_stock = ?, rating = ?
                WHERE id = ?
                """,
                (updated["title"], updated["price"], updated["in_stock"], updated["rating"], book_id),
            )
            connection.commit()

        return self.get_book_by_id(book_id)

    def delete_book(self, book_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM books WHERE id = ?", (book_id,))
            connection.commit()
        return cursor.rowcount > 0