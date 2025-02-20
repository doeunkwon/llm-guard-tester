import openai
import os
from ..utils.db_manager import TestsDB
from ..models.enhancement_technique import EnhancementTechnique
from .enhancer_helper import storyline, coding


class Enhancer:
    def __init__(self, model: str):
        self.client = openai.Client(
            api_key=os.getenv("CLOD_API_KEY"),
            base_url="https://api.clod.io/v1",
        )
        self.db = TestsDB()
        self.model = model

    def enhance(self, technique: EnhancementTechnique, test_name: str):
        """Process baseline attacks for a specific test and apply enhancement"""
        print(f"\n🚀 Starting enhancement process for test: {test_name}")
        baseline_cases = self.db.get_baseline_cases(test_name=test_name)
        print(f"📑 Found {len(baseline_cases)} baseline cases to enhance")

        for i, case in enumerate(baseline_cases, 1):
            print("="*80)
            print(f"\n📌 Processing case {i}/{len(baseline_cases)}")

            # Apply the specified enhancement technique
            match technique:
                case EnhancementTechnique.STORYLINE:
                    storyline.process_storyline(case, self.db)
                case EnhancementTechnique.CODING:
                    coding.process_coding(case, self.db)

        print("\n✨ Enhancement process completed!")
