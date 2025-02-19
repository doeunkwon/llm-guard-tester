from src.core.generator import Generator
from config.rules import LLAMA_GUARD_RULES, CUSTOM_RULES, EU_AI_ACT_RULES
import argparse


def main():

    rules = EU_AI_ACT_RULES

    parser = argparse.ArgumentParser(
        description='Generate test cases for Llama Guard rules')
    parser.add_argument('category', type=int,
                        help='Llama Guard category number (1-based index)')
    parser.add_argument('--model', type=str, default='gpt-4o',
                        help='Model to use for generation (default: gpt-4o)')
    parser.add_argument('--num-valid-cases', type=int, default=0,
                        help='Number of valid test cases to generate (default: 0)')
    parser.add_argument('--num-baseline-cases', type=int, default=1,
                        help='Number of baseline test cases to generate (default: 1)')

    args = parser.parse_args()

    # Validate category number
    if args.category < 1 or args.category > len(rules):
        raise ValueError(f"Category number must be between 1 and {
                         len(rules)}")

    generator = Generator(model=args.model)

    generator.generate_valid_cases(
        rules[args.category - 1]["test_name"],
        rules[args.category - 1]["rule"],
        args.num_valid_cases
    )

    generator.generate_baseline_cases(
        rules[args.category - 1]["test_name"],
        rules[args.category - 1]["rule"],
        args.num_baseline_cases
    )


if __name__ == "__main__":
    main()
