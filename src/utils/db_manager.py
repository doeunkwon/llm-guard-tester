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

    def get_test_cases(self, test_name: str = None, max_results: int = None) -> List[TestCase]:
        """Retrieve test cases from the database

        Args:
            test_name: Optional filter by test name
            max_results: Optional maximum number of test cases to return for EACH should_pass value.
                        Total returned cases will be up to 2 * max_results (half passing, half failing)
        """
        try:
            with sqlite3.connect(self.test_cases_path) as conn:
                cursor = conn.cursor()

                # Base query with test_name filter if provided
                test_name_condition = "WHERE test_name = ?" if test_name else ""
                params = (test_name,) if test_name else ()

                # Get both passing and failing cases separately
                query = f'''
                    SELECT * FROM (
                        SELECT * FROM test_cases 
                        {test_name_condition}
                        {"WHERE" if not test_name else "AND"} should_pass = TRUE
                        ORDER BY RANDOM()
                        {f"LIMIT {max_results}" if max_results else ""}
                    )
                    UNION ALL
                    SELECT * FROM (
                        SELECT * FROM test_cases 
                        {test_name_condition}
                        {"WHERE" if not test_name else "AND"} should_pass = FALSE
                        ORDER BY RANDOM()
                        {f"LIMIT {max_results}" if max_results else ""}
                    )
                '''

                cursor.execute(query, params * 2 if test_name else ())
                columns = [description[0]
                           for description in cursor.description]
                return [TestCase(**dict(zip(columns, row))) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error retrieving test cases: {str(e)}")
            return []
