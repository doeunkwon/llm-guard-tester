from typing import List
from ..models.test_models import TestResult


def display_results(results: List[TestResult]):

    print("\n=== Detailed Test Results ===")
    for i, result in enumerate(results, 1):
        print(f"\nTest #{i}")
        print(f"Prompt: {result.prompt}")
        print(f"Should Pass: {result.should_pass}")
        print(f"LLM Response: {result.llm_response}")
        print("-" * 80)
