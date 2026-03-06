import json
import random
from pathlib import Path
from app.models.task import Task
from app.services.task_builders.base import BaseTaskBuilder

DATA_DIR = Path(__file__).parent.parent.parent.parent.parent / "data" / "vocabulary"

def load_vocabulary(level: int) -> list:
    vocab = []
    if level <= 3:
        files = ["beginner.json"]
    elif level <= 6:
        files = ["beginner.json", "intermediate.json"]
    else:
        files = ["beginner.json", "intermediate.json", "advanced.json"]
    
    for fname in files:
        fpath = DATA_DIR / fname
        if fpath.exists():
            with open(fpath) as f:
                words = json.load(f)
            vocab.extend([w for w in words if w.get("difficulty", 1) <= level])
    return vocab

class WordTranslationTaskBuilder(BaseTaskBuilder):
    @property
    def task_type(self) -> str:
        return "word_translation"

    def build(self) -> Task:
        vocab = load_vocabulary(self.level)
        if not vocab:
            vocab = [{"indonesian": "berlari", "english": "run", "synonyms": ["jog"], "difficulty": 1}]
        
        word = random.choice(vocab)
        instruction = f"Terjemahkan kata berikut ke bahasa Inggris: '{word['indonesian']}'"
        
        return Task(
            task_type=self.task_type,
            instruction=instruction,
            level=self.level,
            expected_answer=word["english"],
            vocabulary_item=word
        )
