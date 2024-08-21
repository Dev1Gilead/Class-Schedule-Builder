import unittest
from data.database import get_db_connection, create_tables

class TestDatabaseConnection(unittest.TestCase):
    def test_connection(self):
        # Test if the connection can be established
        conn = get_db_connection()
        self.assertIsNotNone(conn)
        conn.close()

    def test_create_tables(self):
        # Test if the tables are created correctly
        create_tables()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()

        # Convert the rows to a list of table names
        table_names = [table['name'] for table in tables]

        # Debugging: print out the table names found
        print("Tables found in the database:", table_names)

        # Check that the 'courses' and 'students' tables were created
        self.assertIn('courses', table_names)
        self.assertIn('students', table_names)

if __name__ == '__main__':
    unittest.main()
