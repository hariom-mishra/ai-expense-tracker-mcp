# AI Expense Tracker (MCP Server)

A simple, Python-based Model Context Protocol (MCP) server for tracking personal expenses, built using `fastmcp` and SQLite.

## Features
- **Database**: Automatic local SQLite database initialization (`expense.db`).
- **Tools**:
  - `add_expense`: Log a new expense (amount, category, date, subcategory, note, description).
  - `fetch_all_expenses`: Fetch expenses with optional filters by ID, category, or date range.
  - `update_expense`: Update properties of a logged expense.
  - `delete_expense`: Remove an expense by ID.
- **Resources**:
  - `expense://categories`: Access the categories hierarchy defined in `categories.json`.

---

## Setup & Running

### 1. Install Dependencies
Make sure you have [uv](https://github.com/astral-sh/uv) installed. Then run:
```bash
uv pip install -r requirements.txt
```

### 2. Run Locally (Development Inspector)
To test the tools inside a web-based MCP Inspector:
```bash
uv run fastmcp dev inspector main.py
```

### 3. Install in Claude Desktop
To install the server directly into your local Claude Desktop application:
```bash
uv run fastmcp install claude-desktop main.py --name "expense-tracker"
```
*Remember to restart Claude Desktop after installing.*
