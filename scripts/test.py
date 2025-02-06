from src.core.tester import Tester
from src.utils.display import display_results
from config.rules import LLAMA_GUARD_RULES
import argparse


def main():

    parser = argparse.ArgumentParser(
        description='Test Llama Guard rules')
    parser.add_argument('category', type=int,
                        help='Llama Guard category number (1-based index)')
    parser.add_argument('--max-valid-cases', type=int, default=0,
                        help='Number of valid test cases to generate (default: 0)')
    parser.add_argument('--max-enhanced-cases', type=int, default=3,
                        help='Number of enhanced test cases to generate (default: 3)')
    parser.add_argument('--defender-model', type=str, default='gemini-1.5-flash',
                        help='Model to use for testing (default: gemini-1.5-flash)')

    args = parser.parse_args()

    # Validate category number
    if args.category < 1 or args.category > len(LLAMA_GUARD_RULES):
        raise ValueError(f"Category number must be between 1 and {
                         len(LLAMA_GUARD_RULES)}")

    if args.max_valid_cases < 0 or args.max_enhanced_cases < 0:
        raise ValueError("Max valid and enhanced cases must be greater than 0")

    tester = Tester()
    results = tester.run_tests(
        LLAMA_GUARD_RULES[args.category - 1]["test_name"],
        args.max_valid_cases,
        args.max_enhanced_cases,
        args.defender_model
    )
    display_results(results)


if __name__ == "__main__":
    main()
