import sqlite3
import os
from typing import List
from ..models.test_case import TestCase


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
            self.create_baseline_table()
            self.create_valid_table()
            self.create_results_table()
            self.create_enhanced_table()
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            raise

    def create_baseline_table(self):
        """Create the baseline table for failure cases"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS baseline (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        test_name TEXT NOT NULL,
                        prompt TEXT NOT NULL,
                        offender_model TEXT NOT NULL,
                        set_id TEXT NOT NULL,
                        enhanced BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"Error creating baseline table: {str(e)}")
            raise

    def create_valid_table(self):
        """Create the valid table for success cases"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS valid (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        test_name TEXT NOT NULL,
                        prompt TEXT NOT NULL,
                        offender_model TEXT NOT NULL,
                        set_id TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"Error creating valid table: {str(e)}")
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

    def create_enhanced_table(self):
        """Create the enhanced table for enhanced attack cases"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS enhanced (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        test_name TEXT NOT NULL,
                        prompt TEXT NOT NULL,
                        offender_model TEXT NOT NULL,
                        set_id TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"Error creating enhanced table: {str(e)}")
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

    def store_valid_cases(self, test_name: str, prompts: List[str], set_id: str, offender_model: str):
        """Store test cases in the valid table"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for prompt in prompts:
                    cursor.execute('''
                        INSERT INTO valid (test_name, prompt, set_id, offender_model)
                        VALUES (?, ?, ?, ?)
                    ''', (test_name, prompt, set_id, offender_model))
                conn.commit()
        except Exception as e:
            print(f"Error storing valid cases: {str(e)}")

    def store_baseline_cases(self, test_name: str, prompts: List[str], set_id: str, offender_model: str):
        """Store test cases in the baseline table"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for prompt in prompts:
                    cursor.execute('''
                        INSERT INTO baseline (test_name, prompt, set_id, offender_model, enhanced)
                        VALUES (?, ?, ?, ?, FALSE)
                    ''', (test_name, prompt, set_id, offender_model))
                conn.commit()
        except Exception as e:
            print(f"Error storing baseline cases: {str(e)}")

    def store_enhanced_cases(self, test_name: str, prompts: List[str], set_id: str, offender_model: str):
        """Store enhanced test cases in the enhanced table"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for prompt in prompts:
                    cursor.execute('''
                        INSERT INTO enhanced (test_name, prompt, set_id, offender_model)
                        VALUES (?, ?, ?, ?)
                    ''', (test_name, prompt, set_id, offender_model))
                conn.commit()
        except Exception as e:
            print(f"Error storing enhanced cases: {str(e)}")

    def get_valid_cases(self, test_name: str = None, limit: int = None) -> List[TestCase]:
        """Retrieve test cases from valid table"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                conditions = []
                params = []
                if test_name:
                    conditions.append("test_name = ?")
                    params.append(test_name)

                query = f'''
                    SELECT *, TRUE as should_pass FROM valid 
                    {f"WHERE {' AND '.join(conditions)}" if conditions else ""}
                    ORDER BY RANDOM()
                    {f"LIMIT {limit}" if limit else ""}
                '''

                cursor.execute(query, params)
                rows = cursor.fetchall()
                columns = [description[0]
                           for description in cursor.description]

                return [TestCase(**dict(zip(columns, row))) for row in rows]

        except Exception as e:
            print(f"Error retrieving valid cases: {str(e)}")
            return []

    def get_baseline_cases(self, test_name: str = None, limit: int = None, enhanced: bool = None) -> List[TestCase]:
        """Retrieve test cases from baseline table"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                conditions = []
                params = []
                if test_name:
                    conditions.append("test_name = ?")
                    params.append(test_name)
                if enhanced is not None:
                    conditions.append("enhanced = ?")
                    params.append(enhanced)

                query = f'''
                    SELECT *, FALSE as should_pass FROM baseline 
                    {f"WHERE {' AND '.join(conditions)}" if conditions else ""}
                    ORDER BY RANDOM()
                    {f"LIMIT {limit}" if limit else ""}
                '''

                cursor.execute(query, params)
                rows = cursor.fetchall()
                columns = [description[0]
                           for description in cursor.description]

                return [TestCase(**dict(zip(columns, row))) for row in rows]

        except Exception as e:
            print(f"Error retrieving baseline cases: {str(e)}")
            return []

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

    def mark_baseline_as_enhanced(self, case_id: int):
        """Mark a baseline case as enhanced"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE baseline 
                    SET enhanced = TRUE 
                    WHERE id = ?
                ''', (case_id,))
                conn.commit()
        except Exception as e:
            print(f"Error marking baseline as enhanced: {str(e)}")
