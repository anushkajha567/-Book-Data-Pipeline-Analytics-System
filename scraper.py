from __future__ import annotations

import re
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

from database import BookDatabaseManager

BASE_URL = "http://books.toscrape.com/"

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def parse_price(value: str) -> float:
    cleaned = re.sub(r"[^0-9.]", "", value)
    return float(cleaned)


def parse_rating(class_list: List[str]) -> int:
    for item in class_list:
        if item in RATING_MAP:
            return RATING_MAP[item]
    raise ValueError(f"Rating class not found in {class_list}")


def scrape_books(limit: int = 20) -> List[Dict[str, object]]:
    response = requests.get(BASE_URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    book_cards = soup.select("article.product_pod")[:limit]

    books: List[Dict[str, object]] = []
    for card in book_cards:
        title = card.h3.a["title"].strip()
        price_text = card.select_one("p.price_color").get_text(strip=True)
        availability_text = card.select_one("p.instock.availability").get_text(" ", strip=True)
        rating_class = card.select_one("p.star-rating")["class"]

        books.append(
            {
                "title": title,
                "price": parse_price(price_text),
                "in_stock": availability_text,
                "rating": parse_rating(rating_class),
            }
        )

    return books


def save_books_to_database(books: List[Dict[str, object]], db_path: str = "books.db") -> List[int]:
    manager = BookDatabaseManager(db_path)
    manager.clear_books()
    return manager.insert_books(books)


def main() -> None:
    books = scrape_books(limit=20)
    saved_ids = save_books_to_database(books)
    print(f"Scraped {len(books)} books and saved {len(saved_ids)} records to books.db")


if __name__ == "__main__":
    main()