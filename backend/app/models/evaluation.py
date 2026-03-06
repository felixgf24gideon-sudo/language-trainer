from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class EvaluationResult:
    grammar: int = 0
    vocabulary: int = 0
    naturalness: int = 0
    task_completion: int = 0
    is_correct: bool = False
    errors: List[str] = field(default_factory=list)
    error_types: List[str] = field(default_factory=list)
    feedback: Optional[str] = None
    correction: Optional[str] = None
    explanation: Optional[str] = None
    better_examples: List[str] = field(default_factory=list)

    @property
    def average_score(self) -> float:
        scores = [self.grammar, self.vocabulary, self.naturalness, self.task_completion]
        return sum(scores) / len(scores)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "grammar": self.grammar,
            "vocabulary": self.vocabulary,
            "naturalness": self.naturalness,
            "task_completion": self.task_completion,
            "is_correct": self.is_correct,
            "average_score": self.average_score,
            "errors": self.errors,
            "error_types": self.error_types,
            "feedback": self.feedback,
            "correction": self.correction,
            "explanation": self.explanation,
            "better_examples": self.better_examples
        }
