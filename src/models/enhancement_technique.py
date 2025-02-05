from enum import Enum, auto


class EnhancementTechnique(Enum):
    STORYLINE = "storyline"

    @classmethod
    def from_string(cls, technique_name: str) -> "EnhancementTechnique":
        for technique in cls:
            if technique.value.lower() == technique_name.lower():
                return technique
        raise ValueError(f"Unknown enhancement technique: {technique_name}")
