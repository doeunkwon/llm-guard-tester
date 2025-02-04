from src.core.enhancer import Enhancer
from src.models.enhancement_technique import EnhancementTechnique
from config.rules import LLAMA_GUARD_RULES


def main():
    technique = EnhancementTechnique.ROLE_PLAYING
    enhancer = Enhancer()

    tests = LLAMA_GUARD_RULES
    for test in tests:
        test_name = test["test_name"]
        enhancer.enhance(technique, test_name)
        print(f"Enhanced {test_name}")

    # test_name = "S1"
    # enhancer.enhance(technique, test_name)


if __name__ == "__main__":
    main()
