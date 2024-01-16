import sqlite3
from langchain.tools import Tool
from langchain import SQLDatabase

conn = sqlite3.connect('db.sqlite')

def list_tables():
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)

def run_sqlite_query(query):
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.OperationalError as err:
        return f"the following error occurred: {str(err)}"

db = SQLDatabase.from_uri("sqlite:///db.sqlite")
run_query_tool = Tool(
    name="run_sqlite_query",
    description="Run a sqlite query.",
    func=run_sqlite_query
)
