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

    def get_test_cases(self, test_name: str = None, success_cases: int = None, failure_cases: int = None) -> List[TestCase]:
        """Retrieve test cases from the database

        Args:
            test_name: Optional filter by test name
            success_cases: Optional maximum number of success cases to return
            failure_cases: Optional maximum number of failure cases to return
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Build base conditions
                conditions = []
                params = []
                if test_name:
                    conditions.append("test_name = ?")
                    params.append(test_name)

                # Get success cases
                success_query = f'''
                    SELECT * FROM test_cases 
                    WHERE should_pass = TRUE
                    {f"AND {' AND '.join(conditions)}" if conditions else ""}
                    ORDER BY RANDOM()
                    {f"LIMIT {success_cases}" if success_cases else ""}
                '''

                # Get failure cases
                failure_query = f'''
                    SELECT * FROM test_cases 
                    WHERE should_pass = FALSE
                    {f"AND {' AND '.join(conditions)}" if conditions else ""}
                    ORDER BY RANDOM()
                    {f"LIMIT {failure_cases}" if failure_cases else ""}
                '''

                # Execute both queries and combine results
                cursor.execute(success_query, params)
                success_rows = cursor.fetchall()

                cursor.execute(failure_query, params)
                failure_rows = cursor.fetchall()

                # Get column names
                columns = [description[0]
                           for description in cursor.description]

                # Convert rows to TestCase objects
                all_cases = []
                all_cases.extend([TestCase(**dict(zip(columns, row)))
                                 for row in success_rows])
                all_cases.extend([TestCase(**dict(zip(columns, row)))
                                 for row in failure_rows])

                return all_cases

        except Exception as e:
            print(f"Error retrieving test cases: {str(e)}")
            return []
