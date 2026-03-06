import json
from app.models.task import Task
from app.models.evaluation import EvaluationResult
from app.llm.client import call_llm
from app.llm.prompts.evaluation_prompts import get_evaluation_prompt

PASSING_THRESHOLD = 3.0

class Evaluator:
    def evaluate(self, task: Task, user_answer: str) -> EvaluationResult:
        if not user_answer or not user_answer.strip():
            return EvaluationResult(
                grammar=0, vocabulary=0, naturalness=0, task_completion=0,
                is_correct=False,
                errors=["No answer provided"],
                error_types=["missing_word"]
            )
        
        prompt = get_evaluation_prompt(
            task_type=task.task_type,
            instruction=task.instruction,
            user_answer=user_answer,
            expected_answer=task.expected_answer
        )
        
        try:
            response = call_llm(prompt, expect_json=True)
            data = json.loads(response)
            
            grammar = min(max(int(data.get("grammar", 0)), 0), 5)
            vocabulary = min(max(int(data.get("vocabulary", 0)), 0), 5)
            naturalness = min(max(int(data.get("naturalness", 0)), 0), 5)
            task_completion = min(max(int(data.get("task_completion", 0)), 0), 5)
            
            avg = (grammar + vocabulary + naturalness + task_completion) / 4
            is_correct = avg >= PASSING_THRESHOLD
            
            errors = data.get("errors", [])
            error_types = data.get("error_types", [])
            
            return EvaluationResult(
                grammar=grammar,
                vocabulary=vocabulary,
                naturalness=naturalness,
                task_completion=task_completion,
                is_correct=is_correct,
                errors=errors if isinstance(errors, list) else [],
                error_types=error_types if isinstance(error_types, list) else []
            )
        except (json.JSONDecodeError, ValueError, KeyError):
            if task.task_type == "word_translation" and task.expected_answer:
                answer_lower = user_answer.strip().lower()
                expected_lower = task.expected_answer.lower()
                vocab = task.vocabulary_item or {}
                synonyms = [s.lower() for s in vocab.get("synonyms", [])]
                is_correct = answer_lower == expected_lower or answer_lower in synonyms
                score = 5 if is_correct else 2
                return EvaluationResult(
                    grammar=score, vocabulary=score, naturalness=score, task_completion=score,
                    is_correct=is_correct,
                    errors=[] if is_correct else [f"Expected '{task.expected_answer}'"],
                    error_types=[] if is_correct else ["word_choice"]
                )
            return EvaluationResult(
                grammar=3, vocabulary=3, naturalness=3, task_completion=3,
                is_correct=True,
                errors=[],
                error_types=[]
            )
