from src.core.enhancer import Enhancer
from src.models.enhancement_technique import EnhancementTechnique


def main():
    # Convert string to enum
    technique = EnhancementTechnique.CODING_TASKS
    test_name = "S1"

    # Create enhancer for this technique
    enhancer = Enhancer()

    enhancer.enhance(technique, test_name)


if __name__ == "__main__":
    main()
