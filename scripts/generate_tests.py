from src.core.llm_tester import LLMTester
from config.rules import LLAMA_GUARD_RULES


def main():
    tests = LLAMA_GUARD_RULES
    num_success_cases = 3
    num_failure_cases = 3
    offender_model = "gpt-4o"

    tester = LLMTester()

    for test in tests:
        test_name = test["test_name"]
        rule = test["rule"]
        tester.generate_success_cases(
            test_name, rule, num_success_cases, offender_model)
        print(f"Generated {num_success_cases} success cases for {test_name}")
        tester.generate_failure_cases(
            test_name, rule, num_failure_cases, offender_model)
        print(f"Generated {num_failure_cases} failure cases for {test_name}")


if __name__ == "__main__":
    main()
