from src.core.generator import Generator
from config.rules import LLAMA_GUARD_RULES


def main():

    # This is the Llama Guard category number. This is the only value you need to adjust.
    s_num = 10

    offender_model = "gpt-4o"
    generator = Generator(model=offender_model)
    test = {
        "test_name": LLAMA_GUARD_RULES[s_num - 1]["test_name"],
        "rule": LLAMA_GUARD_RULES[s_num - 1]["rule"]
    }
    test_name = test["test_name"]
    rule = test["rule"]
    generator.generate_baseline_cases(
        test_name, rule, 1)


if __name__ == "__main__":
    main()
