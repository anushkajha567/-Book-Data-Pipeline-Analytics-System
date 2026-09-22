from __future__ import annotations

import sys

import matplotlib.pyplot as plt
import pandas as pd
import requests


API_URL = "http://127.0.0.1:8000/books"


def fetch_books(api_url: str = API_URL) -> list[dict]:
    response = requests.get(api_url, timeout=30)
    response.raise_for_status()
    return response.json()


def export_books(api_url: str = API_URL) -> pd.DataFrame:
    books = fetch_books(api_url)
    dataframe = pd.DataFrame(books)
    print(dataframe.to_string(index=False))
    dataframe.to_csv("exported_books.csv", index=False)
    return dataframe


def create_scatter_plot(dataframe: pd.DataFrame, output_path: str = "price_vs_rating.png") -> None:
    plt.figure(figsize=(8, 6))
    plt.scatter(dataframe["price"], dataframe["rating"], alpha=0.8)
    plt.title("Price vs Rating")
    plt.xlabel("Price")
    plt.ylabel("Rating (1-5)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.savefig("price_vs_rating.svg")
    plt.close()


def main() -> int:
    try:
        dataframe = export_books()
        create_scatter_plot(dataframe)
        print("Exported CSV to exported_books.csv")
        print("Saved scatter plot to price_vs_rating.png")
        print("Saved editable plot copy to price_vs_rating.svg")
        return 0
    except Exception as exc:
        print(f"Client failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())