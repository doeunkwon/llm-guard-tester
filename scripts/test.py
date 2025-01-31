from src.core.tester import Tester
from src.utils.display import display_results


def main():
    test_name = "S2"
    max_success_cases = 2
    max_failure_cases = 2
    defender = "Llama-3.1-8b"

    tester = Tester()
    results = tester.run_tests(
        test_name,
        max_success_cases,
        max_failure_cases,
        defender
    )
    display_results(results)


if __name__ == "__main__":
    main()
