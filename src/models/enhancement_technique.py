from enum import Enum, auto


class EnhancementTechnique(Enum):
    MULTILINGUAL = "Multilingual"
    CODING_TASKS = "Coding Tasks"

    @classmethod
    def from_string(cls, technique_name: str) -> "EnhancementTechnique":
        for technique in cls:
            if technique.value.lower() == technique_name.lower():
                return technique
        raise ValueError(f"Unknown enhancement technique: {technique_name}")
