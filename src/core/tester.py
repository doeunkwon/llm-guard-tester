import openai
import os
from typing import List
from ..models.test_models import TestResult
from ..utils.db_manager import TestCaseDB


class Tester:
    def __init__(self):
        self.client = openai.Client(
            api_key=os.getenv("CLOD_API_KEY"),
            base_url="https://api.clod.io/v1",
        )
        self.db = TestCaseDB()

    def get_llm_response(self, prompt: str, defender_model: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=defender_model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error getting LLM response: {str(e)}")
            return "Error: Failed to get response"

    def run_tests(self, test_name: str, success_cases: int, failure_cases: int, defender_model: str) -> List[TestResult]:
        """Run specified number of test pairs"""
        results = []
        test_cases = self.db.get_test_cases(
            test_name, success_cases, failure_cases)

        # Create fresh results table for this test run
        self.db.create_results_table(test_name)

        for test_case in test_cases:
            llm_response = self.get_llm_response(
                test_case.prompt,
                defender_model
            )

            # Store the test result
            self.db.store_test_result(
                test_name=test_name,
                prompt=test_case.prompt,
                should_pass=test_case.should_pass,
                defender_model=defender_model,
                llm_response=llm_response
            )

            result = TestResult(
                prompt=test_case.prompt,
                should_pass=test_case.should_pass,
                llm_response=llm_response,
            )
            results.append(result)

        return results
