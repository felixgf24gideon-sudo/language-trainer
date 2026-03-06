from dataclasses import dataclass, field
from typing import Dict, List, Any
from datetime import datetime

@dataclass
class UserProfile:
    username: str
    level: int = 1
    total_tasks: int = 0
    correct_tasks: int = 0
    success_rate: float = 0.0
    avg_grammar_score: float = 0.0
    avg_vocabulary_score: float = 0.0
    avg_naturalness_score: float = 0.0
    error_profile: Dict[str, float] = field(default_factory=dict)
    task_history: List[Dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "level": self.level,
            "total_tasks": self.total_tasks,
            "correct_tasks": self.correct_tasks,
            "success_rate": self.success_rate,
            "avg_grammar_score": self.avg_grammar_score,
            "avg_vocabulary_score": self.avg_vocabulary_score,
            "avg_naturalness_score": self.avg_naturalness_score,
            "error_profile": self.error_profile,
            "task_history": self.task_history,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
