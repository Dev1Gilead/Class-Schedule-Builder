import sys
import os
import sqlite3

# Adjust the Python path to include the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.database import get_db_connection

def list_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Tables in the database:")
    for table in tables:
        print(table[0])

    conn.close()

def view_table_data(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()

    print(f"\nData in table '{table_name}':")
    for row in rows:
        print(dict(row))

    conn.close()

if __name__ == "__main__":
    list_tables()
    table_name = input("\nEnter the table name to view data: ")
    view_table_data(table_name)
