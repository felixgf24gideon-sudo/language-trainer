import json
import random
from pathlib import Path
from app.models.task import Task
from app.services.task_builders.base import BaseTaskBuilder

DATA_DIR = Path(__file__).parent.parent.parent.parent.parent / "data" / "phrases"

def load_phrases(level: int) -> list:
    fpath = DATA_DIR / "common_phrases.json"
    if not fpath.exists():
        return []
    with open(fpath) as f:
        phrases = json.load(f)
    return [p for p in phrases if p.get("difficulty", 2) <= level]

class PhraseTranslationTaskBuilder(BaseTaskBuilder):
    @property
    def task_type(self) -> str:
        return "phrase_translation"

    def build(self) -> Task:
        phrases = load_phrases(self.level)
        if not phrases:
            phrases = [{"indonesian": "lari cepat", "english": "run quickly", "alternatives": ["run fast"], "difficulty": 2}]
        
        phrase = random.choice(phrases)
        instruction = f"Terjemahkan frasa berikut ke bahasa Inggris: '{phrase['indonesian']}'"
        
        return Task(
            task_type=self.task_type,
            instruction=instruction,
            level=self.level,
            expected_answer=phrase["english"],
            phrase_item=phrase
        )
