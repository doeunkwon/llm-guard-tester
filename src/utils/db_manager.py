import sqlite3
import os
from typing import List
from ..models.test_models import TestCase


class TestCaseDB:
    def __init__(self):
        self.db_path = os.getenv('DB_PATH')
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database"""
        try:
            # Ensure database exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.create_cases_table()
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            raise

    def create_cases_table(self):
        """Create the test cases table if it doesn't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
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
            print(f"Error creating test cases table: {str(e)}")
            raise

    def create_results_table(self, test_name: str):
        """Create a fresh results table for a specific test run"""
        table_name = f"results_{test_name}"
        try:
            # Ensure database exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Drop the table if it exists
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

                # Create new results table without test_case_id
                cursor.execute(f'''
                    CREATE TABLE {table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        prompt TEXT NOT NULL,
                        should_pass BOOLEAN NOT NULL,
                        defender_model TEXT NOT NULL,
                        llm_response TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"Error creating results table: {str(e)}")
            # Re-raise the exception to notify the caller
            raise

    def store_test_result(self, test_name: str, prompt: str, should_pass: bool,
                          defender_model: str, llm_response: str):
        """Store a single test result"""
        table_name = f"results_{test_name}"
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(f'''
                    INSERT INTO {table_name}
                    (prompt, should_pass, defender_model, llm_response)
                    VALUES (?, ?, ?, ?)
                ''', (prompt, should_pass, defender_model, llm_response))
        except Exception as e:
            print(f"Error storing test result: {str(e)}")

    def get_test_results(self, test_name: str) -> List[dict]:
        """Get all results for a specific test"""
        table_name = f"results_{test_name}"
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    f'SELECT * FROM {table_name} ORDER BY timestamp')
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error retrieving test results: {str(e)}")
            return []

    def store_test_cases(self, test_name: str, test_cases: List[TestCase]):
        """Store test cases in the SQLite database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
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
            with sqlite3.connect(self.db_path) as conn:
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
