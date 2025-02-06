import openai
import os
import uuid
from typing import List
from ..models.result import Result
from ..utils.db_manager import TestsDB


class Tester:
    def __init__(self):
        self.client = openai.Client(
            api_key=os.getenv("CLOD_API_KEY"),
            base_url="https://api.clod.io/v1",
        )
        self.db = TestsDB()

    def get_llm_response(self, prompt: str, defender_model: str) -> str:
        """Get response from the defender model for a given prompt"""
        try:
            response = self.client.chat.completions.create(
                model=defender_model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ Error getting LLM response: {str(e)}")
            return "Error: Failed to get response"

    def run_tests(self, test_name: str, max_valid_cases: int, max_enhanced_cases: int, defender_model: str) -> List[Result]:

        results = []
        valid_cases = self.db.get_valid_cases(test_name, max_valid_cases)
        enhanced_cases = self.db.get_enhanced_cases(
            test_name, max_enhanced_cases)

        # Generate a UUID for this test run
        set_id = str(uuid.uuid4())

        for i, valid_case in enumerate(valid_cases, 1):
            llm_response = self.get_llm_response(
                valid_case.prompt,
                defender_model
            )

            self.db.store_test_result(
                test_name=test_name,
                prompt=valid_case.prompt,
                should_pass=True,
                defender_model=defender_model,
                llm_response=llm_response,
                set_id=set_id
            )

            result = Result(
                prompt=valid_case.prompt,
                should_pass=True,
                llm_response=llm_response,
            )
            results.append(result)

        for i, enhanced_case in enumerate(enhanced_cases, 1):
            llm_response = self.get_llm_response(
                enhanced_case.prompt,
                defender_model
            )

            self.db.store_test_result(
                test_name=test_name,
                prompt=enhanced_case.prompt,
                should_pass=False,
                defender_model=defender_model,
                llm_response=llm_response,
                set_id=set_id
            )

            result = Result(
                prompt=enhanced_case.prompt,
                should_pass=False,
                llm_response=llm_response,
            )
            results.append(result)

        return results
