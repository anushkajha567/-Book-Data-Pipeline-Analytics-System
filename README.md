# Book Data Pipeline & Analytics System

This project is an end-to-end Python pipeline that:

- Scrapes the first 20 books from [books.toscrape.com](https://books.toscrape.com)
- Stores them in a local SQLite database
- Exposes the data through a FastAPI REST service
- Consumes the API through a client script that exports CSV data and creates a scatter plot

## Project Structure

- `scraper.py` - Scrapes book data and loads it into SQLite
- `database.py` - SQLite database manager with CRUD methods
- `main.py` - FastAPI app with book endpoints
- `client.py` - Fetches API data, prints a DataFrame, exports CSV, and generates the plot
- `requirements.txt` - Python dependencies

## Data Collected

Each book record contains:

- `title` - Full book title
- `price` - Price as a float
- `in_stock` - Availability text
- `rating` - Star rating converted to an integer from 1 to 5

## Setup

### 1. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

## How to Run the Project

### 1. Scrape the data and populate the database

```powershell
python scraper.py
```

This creates or refreshes `books.db` and stores the first 20 books.

### 2. Start the FastAPI server

```powershell
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### 3. Run the client script

In a second terminal, while the API server is running:

```powershell
python client.py
```

The client will:

- Call `GET /books`
- Print the results as a Pandas DataFrame
- Export `exported_books.csv`
- Create `price_vs_rating.png`
- Also create `price_vs_rating.svg` so the chart can be opened as text in the editor

## REST API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/books` | Retrieve all books |
| GET | `/books/{id}` | Retrieve one book by ID |
| POST | `/books` | Create a new book |
| PUT | `/books/{id}` | Update an existing book |
| DELETE | `/books/{id}` | Delete a book |

### Example Book JSON

```json
{
  "title": "A Light in the Attic",
  "price": 51.77,
  "in_stock": "In stock",
  "rating": 3
}
```

## Output Files

After a successful run, you should see these generated files:

- `books.db` - SQLite database
- `exported_books.csv` - Clean CSV export from the API data
- `price_vs_rating.png` - Scatter plot of price vs rating
- `price_vs_rating.svg` - Editable text-based version of the plot

## Expected Result

The scraper should return exactly 20 records from the main page of Books to Scrape. The client should print a DataFrame showing those 20 rows, export the CSV, and save the scatter plot.

## Troubleshooting

- If the client says it cannot reach the API, make sure `uvicorn main:app --reload` is still running.
- If `books.db` is empty, run `python scraper.py` again before starting the API.
- If PowerShell blocks virtual environment activation, run PowerShell as a normal user and allow script execution for the session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Notes

- The scraper only targets the first 20 books, as required by the project scope.
- The database layer uses an object-oriented manager class for CRUD operations.
- The project was validated end to end against the live site.