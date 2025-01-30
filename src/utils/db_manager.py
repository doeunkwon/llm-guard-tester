import sqlite3
import os
from typing import List
from ..models.test_models import TestCase


class TestCaseDB:
    def __init__(self):
        self.test_cases_path = os.getenv('DB_PATH') + 'test_cases.db'
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database and create table if it doesn't exist"""
        try:
            with sqlite3.connect(self.test_cases_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS test_cases (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        test_name TEXT NOT NULL,
                        prompt TEXT NOT NULL,
                        should_pass BOOLEAN NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"Error initializing database: {str(e)}")

    def store_test_cases(self, test_name: str, test_cases: List[TestCase]):
        """Store test cases in the SQLite database"""
        try:
            with sqlite3.connect(self.test_cases_path) as conn:
                cursor = conn.cursor()
                for test_case in test_cases:
                    cursor.execute('''
                        INSERT INTO test_cases (test_name, prompt, should_pass)
                        VALUES (?, ?, ?)
                    ''', (test_name, test_case.prompt, test_case.should_pass))
                conn.commit()
        except Exception as e:
            print(f"Error storing test cases: {str(e)}")

    def get_test_cases(self, test_name: str = None) -> List[dict]:
        """Retrieve test cases from the database"""
        try:
            with sqlite3.connect(self.test_cases_path) as conn:
                cursor = conn.cursor()
                if test_name:
                    cursor.execute('''
                        SELECT * FROM test_cases WHERE test_name = ?
                    ''', (test_name,))
                else:
                    cursor.execute('SELECT * FROM test_cases')

                columns = [description[0]
                           for description in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error retrieving test cases: {str(e)}")
            return []
