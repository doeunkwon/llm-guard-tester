from typing import List
from ..models.test_models import TestResult


def display_results(results: List[TestResult]):
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r.passed_judgment)

    print("\n=== Test Results Summary ===")
    print(f"Total Tests Run: {total_tests}")
    print(f"Tests Passed: {passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.2f}%")

    print("\n=== Detailed Test Results ===")
    for i, result in enumerate(results, 1):
        print(f"\nTest #{i}")
        print(f"Prompt: {result.prompt}")
        print(f"Should Pass: {result.should_pass}")
        print(f"LLM Response: {result.llm_response}")
        print(f"Passed Judgment: {result.passed_judgment}")
        print("-" * 80)
