from src.core.enhancer import Enhancer
from src.models.enhancement_technique import EnhancementTechnique
from config.rules import LLAMA_GUARD_RULES, CUSTOM_RULES, EU_AI_ACT_RULES
import argparse


def main():

    rules = EU_AI_ACT_RULES

    parser = argparse.ArgumentParser(
        description='Enhance test cases for Llama Guard rules')
    parser.add_argument('category', type=int,
                        help='Llama Guard category number (1-based index)')
    parser.add_argument('--model', type=str, default='gpt-4o-mini',
                        help='Model to use for enhancement (default: gpt-4o-mini)')
    parser.add_argument('--technique', type=str, default='storyline',
                        choices=['storyline', 'coding'],
                        help='Enhancement technique to use (default: storyline)')

    args = parser.parse_args()

    # Validate category number
    if args.category < 1 or args.category > len(rules):
        raise ValueError(f"Category number must be between 1 and {
                         len(rules)}")

    technique = EnhancementTechnique.from_string(args.technique)
    enhancer = Enhancer(model=args.model)
    test_name = rules[args.category - 1]["test_name"]
    enhancer.enhance(technique, test_name)


if __name__ == "__main__":
    main()
