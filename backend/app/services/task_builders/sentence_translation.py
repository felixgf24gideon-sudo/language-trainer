import json
import random
from pathlib import Path
from app.models.task import Task
from app.services.task_builders.base import BaseTaskBuilder

DATA_DIR = Path(__file__).parent.parent.parent.parent.parent / "data" / "sentences"

def load_sentences(level: int) -> list:
    fpath = DATA_DIR / "translation_pairs.json"
    if not fpath.exists():
        return []
    with open(fpath) as f:
        sentences = json.load(f)
    return [s for s in sentences if s.get("difficulty", 3) <= level]

class SentenceTranslationTaskBuilder(BaseTaskBuilder):
    @property
    def task_type(self) -> str:
        return "sentence_translation"

    def build(self) -> Task:
        sentences = load_sentences(self.level)
        if not sentences:
            sentences = [{"indonesian": "Saya pergi ke sekolah kemarin.", "english": "I went to school yesterday.", "difficulty": 3}]
        
        sentence = random.choice(sentences)
        instruction = f"Terjemahkan kalimat berikut ke bahasa Inggris:\n'{sentence['indonesian']}'"
        
        return Task(
            task_type=self.task_type,
            instruction=instruction,
            level=self.level,
            expected_answer=sentence["english"],
            sentence_item=sentence
        )
