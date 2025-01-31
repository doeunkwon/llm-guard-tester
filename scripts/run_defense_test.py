from src.core.llm_tester import LLMTester
from src.utils.display import display_results


def main():
    test_name = "S9"
    max_num_pairs = 2
    defender = "Llama-3.1-8b"

    tester = LLMTester()
    results = tester.run_tests(
        test_name,
        max_num_pairs,
        defender
    )
    display_results(results)


if __name__ == "__main__":
    main()
