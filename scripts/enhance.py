from src.core.enhancer import Enhancer
from src.models.enhancement_technique import EnhancementTechnique


def main():
    # Convert string to enum
    technique = EnhancementTechnique.CODING_TASKS

    # Create enhancer for this technique
    enhancer = Enhancer(technique)

    enhancer.enhance()


if __name__ == "__main__":
    main()
