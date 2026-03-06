import random
from typing import Optional
from app.models.task import Task
from app.config.languages import TASK_TYPES
from app.services.task_builders.word_translation import WordTranslationTaskBuilder
from app.services.task_builders.phrase_translation import PhraseTranslationTaskBuilder
from app.services.task_builders.sentence_translation import SentenceTranslationTaskBuilder
from app.services.task_builders.constrained_production import ConstrainedProductionTaskBuilder
from app.services.task_builders.context_production import ContextProductionTaskBuilder
from app.services.task_builders.paragraph_production import ParagraphProductionTaskBuilder

BUILDER_MAP = {
    "word_translation": WordTranslationTaskBuilder,
    "phrase_translation": PhraseTranslationTaskBuilder,
    "sentence_translation": SentenceTranslationTaskBuilder,
    "constrained_production": ConstrainedProductionTaskBuilder,
    "context_production": ContextProductionTaskBuilder,
    "paragraph_production": ParagraphProductionTaskBuilder
}

class TaskGenerator:
    def __init__(self, level: int, error_profile: dict = None):
        self.level = level
        self.error_profile = error_profile or {}

    def get_available_task_types(self) -> list:
        available = []
        for task_type, config in TASK_TYPES.items():
            min_level, max_level = config["level_range"]
            if min_level <= self.level <= max_level:
                available.append(task_type)
        return available

    def select_task_type(self) -> str:
        available = self.get_available_task_types()
        if not available:
            return "word_translation"
        
        weights = []
        for task_type in available:
            config = TASK_TYPES[task_type]
            weight = config["weight_by_level"].get(self.level, 0.1)
            weights.append(weight)
        
        total = sum(weights)
        if total == 0:
            return random.choice(available)
        
        normalized = [w / total for w in weights]
        return random.choices(available, weights=normalized, k=1)[0]

    def generate(self) -> Task:
        task_type = self.select_task_type()
        builder_class = BUILDER_MAP.get(task_type, WordTranslationTaskBuilder)
        builder = builder_class(level=self.level)
        return builder.build()
