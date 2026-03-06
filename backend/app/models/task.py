from dataclasses import dataclass, field
from typing import Optional, List, Any, Dict
from datetime import datetime

@dataclass
class Task:
    task_type: str
    instruction: str
    level: int
    expected_answer: Optional[str] = None
    vocabulary_item: Optional[Dict[str, Any]] = None
    phrase_item: Optional[Dict[str, Any]] = None
    sentence_item: Optional[Dict[str, Any]] = None
    constraint_word: Optional[str] = None
    grammar_structure: Optional[str] = None
    context_topic: Optional[str] = None
    task_id: Optional[int] = None
    user_answer: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_type": self.task_type,
            "instruction": self.instruction,
            "level": self.level,
            "expected_answer": self.expected_answer,
            "task_id": self.task_id,
            "user_answer": self.user_answer,
            "created_at": self.created_at
        }
