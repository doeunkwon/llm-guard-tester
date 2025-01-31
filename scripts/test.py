from src.core.tester import Tester
from src.utils.display import display_results


def main():
    test_name = "S2"
    max_valid_cases = 2
    max_enhanced_cases = 2
    defender = "gemini-1.5-flash"

    tester = Tester()
    results = tester.run_tests(
        test_name,
        max_valid_cases,
        max_enhanced_cases,
        defender
    )
    display_results(results)


if __name__ == "__main__":
    main()
