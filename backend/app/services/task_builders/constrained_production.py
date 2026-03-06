import json
import random
from pathlib import Path
from app.models.task import Task
from app.services.task_builders.base import BaseTaskBuilder

CONSTRAINT_WORDS = {
    3: ["because", "but", "and", "so"],
    4: ["although", "however", "therefore", "while"],
    5: ["despite", "nevertheless", "furthermore", "consequently"],
    6: ["whereas", "nonetheless", "moreover", "alternatively"],
    7: ["notwithstanding", "subsequently", "simultaneously", "accordingly"],
    8: ["hitherto", "heretofore", "inasmuch", "insofar"]
}

class ConstrainedProductionTaskBuilder(BaseTaskBuilder):
    @property
    def task_type(self) -> str:
        return "constrained_production"

    def build(self) -> Task:
        level_key = min(self.level, 8)
        available_words = []
        for lvl in range(3, level_key + 1):
            if lvl in CONSTRAINT_WORDS:
                available_words.extend(CONSTRAINT_WORDS[lvl])
        
        if not available_words:
            available_words = ["because"]
        
        constraint_word = random.choice(available_words)
        instruction = f"Buat satu kalimat bahasa Inggris yang menggunakan kata '{constraint_word}'."
        
        return Task(
            task_type=self.task_type,
            instruction=instruction,
            level=self.level,
            expected_answer=None,
            constraint_word=constraint_word
        )
