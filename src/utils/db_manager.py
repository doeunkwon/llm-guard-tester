import sqlite3
import os
from typing import List
from ..models.baseline import Baseline


class TestsDB:
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
            self.create_results_table()
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            raise

    def create_cases_table(self):
        """Create the baseline table if it doesn't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS baseline (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        test_name TEXT NOT NULL,
                        prompt TEXT NOT NULL,
                        should_pass BOOLEAN NOT NULL,
                        offender_model TEXT NOT NULL,
                        set_id TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"Error creating baseline table: {str(e)}")
            raise

    def create_results_table(self):
        """Create the results table if it doesn't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        test_name TEXT NOT NULL,
                        prompt TEXT NOT NULL,
                        should_pass BOOLEAN NOT NULL,
                        defender_model TEXT NOT NULL,
                        llm_response TEXT NOT NULL,
                        set_id TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"Error creating results table: {str(e)}")
            raise

    def store_test_result(self, test_name: str, prompt: str, should_pass: bool,
                          defender_model: str, llm_response: str, set_id: str):
        """Store a single test result"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO results
                    (test_name, prompt, should_pass, defender_model, llm_response, set_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (test_name, prompt, should_pass, defender_model, llm_response, set_id))
        except Exception as e:
            print(f"Error storing test result: {str(e)}")

    def get_test_results(self, test_name: str) -> List[dict]:
        """Get all results for a specific test"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    'SELECT * FROM results WHERE test_name = ? ORDER BY timestamp',
                    (test_name,))
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error retrieving test results: {str(e)}")
            return []

    def store_test_cases(self, test_name: str, test_cases: List[Baseline], set_id: str, offender_model: str):
        """Store test cases in the SQLite database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for test_case in test_cases:
                    cursor.execute('''
                        INSERT INTO baseline (test_name, prompt, should_pass, set_id, offender_model)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (test_name, test_case.prompt, test_case.should_pass, set_id, offender_model))
                conn.commit()
        except Exception as e:
            print(f"Error storing test cases: {str(e)}")

    def get_test_cases(self, test_name: str = None, max_success_cases: int = None, max_failure_cases: int = None) -> List[Baseline]:
        """Retrieve test cases from the database

        Args:
            test_name: Optional filter by test name
            max_success_cases: Optional maximum number of success cases to return
            max_failure_cases: Optional maximum number of failure cases to return
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
                    SELECT * FROM baseline 
                    WHERE should_pass = TRUE
                    {f"AND {' AND '.join(conditions)}" if conditions else ""}
                    ORDER BY RANDOM()
                    {f"LIMIT {max_success_cases}" if max_success_cases else ""}
                '''

                # Get failure cases
                failure_query = f'''
                    SELECT * FROM baseline 
                    WHERE should_pass = FALSE
                    {f"AND {' AND '.join(conditions)}" if conditions else ""}
                    ORDER BY RANDOM()
                    {f"LIMIT {max_failure_cases}" if max_failure_cases else ""}
                '''

                # Execute both queries and combine results
                cursor.execute(success_query, params)
                success_rows = cursor.fetchall()

                cursor.execute(failure_query, params)
                failure_rows = cursor.fetchall()

                # Get column names
                columns = [description[0]
                           for description in cursor.description]

                # Convert rows to Baseline objects
                all_cases = []
                all_cases.extend([Baseline(**dict(zip(columns, row)))
                                 for row in success_rows])
                all_cases.extend([Baseline(**dict(zip(columns, row)))
                                 for row in failure_rows])

                return all_cases

        except Exception as e:
            print(f"Error retrieving test cases: {str(e)}")
            return []
