from src.core.enhancer import Enhancer
from src.models.enhancement_technique import EnhancementTechnique
from config.rules import LLAMA_GUARD_RULES


def main():

    # This is the Llama Guard category number. This is the only value you need to adjust.
    s_num = 10

    technique = EnhancementTechnique.STORYLINE
    enhancer_model = "gpt-4o-mini"
    enhancer = Enhancer(model=enhancer_model)
    test_name = LLAMA_GUARD_RULES[s_num - 1]["test_name"]
    enhancer.enhance(technique, test_name)


if __name__ == "__main__":
    main()
