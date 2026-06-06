from fastmcp import FastMCP
import sqlite3
import os
import contextlib

db_path = os.path.join(os.path.dirname(__file__), "expense.db")
categories_path = os.path.join(os.path.dirname(__file__), "categories.json")

@contextlib.contextmanager
def get_db():
    conn = sqlite3.connect(db_path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def initdb():
    with get_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            description TEXT, 
            amount REAL, 
            date TEXT NOT NULL, 
            category TEXT NOT NULL,
            subcategory TEXT DEFAULT '',
            note TEXT DEFAULT ''
            )""")

initdb()

mcp = FastMCP("ExpenseTracker")

@mcp.tool
def add_expense(amount: float, category: str, date: str, description: str = "", subcategory: str = "", note: str = "") -> int:
    """Add an expense. Returns the ID of the newly created expense."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses(amount, category, date, description, subcategory, note) VALUES (?, ?, ?, ?, ?, ?)",
            (amount, category, date, description, subcategory, note)
        )
        return cursor.lastrowid

@mcp.tool
def fetch_all_expenses(id: int = None, category: str = None, start_date: str = None, end_date: str = None) -> list:
    """Fetch expenses, optionally filtered by ID or category."""
    with get_db() as conn:
        cursor = conn.cursor()
    
        if id is not None:
            cursor.execute("SELECT * FROM expenses WHERE id = ?", (id,))
            return cursor.fetchall()
        elif category is not None and start_date is not None and end_date is not None:
            cursor.execute("SELECT * FROM expenses WHERE category = ? AND date BETWEEN ? AND ?", (category, start_date, end_date))
            return cursor.fetchall()
        elif category is not None:
            cursor.execute("SELECT * FROM expenses WHERE category = ?", (category,))
            return cursor.fetchall()
        elif start_date is not None and end_date is not None:
            cursor.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ?", (start_date, end_date))
            return cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM expenses")
            return cursor.fetchall()

@mcp.tool
def update_expense(id: int, column: str, value: str) -> bool:
    """Update a specific column of an expense by ID."""
    valid_columns = {"description", "amount", "date", "category", "subcategory", "note"}
    if column not in valid_columns:
        raise ValueError(f"Invalid column name: {column}. Must be one of {valid_columns}")
        
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE expenses SET {column} = ? WHERE id = ?", (value, id))
        return cursor.rowcount > 0

@mcp.tool
def delete_expense(id: int) -> bool:
    """Delete an expense by ID."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
        return cursor.rowcount > 0

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    with open(categories_path, "r") as f:
        return f.read()
    
if __name__ == "__main__":
    mcp.run()