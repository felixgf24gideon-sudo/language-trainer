from app.models.task import Task
from app.models.evaluation import EvaluationResult
from app.llm.client import call_llm
from app.llm.prompts.feedback_prompts import get_feedback_prompt

class FeedbackGenerator:
    def generate(self, task: Task, user_answer: str, evaluation: EvaluationResult) -> EvaluationResult:
        if evaluation.is_correct and not evaluation.errors:
            evaluation.feedback = "✓ Jawaban kamu sudah benar dan natural!"
            evaluation.correction = user_answer
            evaluation.explanation = "Tidak ada kesalahan yang ditemukan."
            evaluation.better_examples = []
            return evaluation
        
        prompt = get_feedback_prompt(
            task_type=task.task_type,
            instruction=task.instruction,
            user_answer=user_answer,
            evaluation=evaluation.to_dict(),
            expected_answer=task.expected_answer
        )
        
        try:
            feedback_text = call_llm(prompt)
            
            lines = feedback_text.strip().split("\n")
            correction = ""
            explanation = ""
            better_examples = []
            
            current_section = None
            for line in lines:
                line = line.strip()
                if "Koreksi:" in line:
                    current_section = "correction"
                elif "Penjelasan:" in line:
                    current_section = "explanation"
                elif "Contoh yang lebih baik:" in line:
                    current_section = "examples"
                elif line and current_section == "correction" and not correction:
                    correction = line
                elif line and current_section == "explanation":
                    explanation += line + " "
                elif line and current_section == "examples":
                    if line.startswith("-"):
                        line = line[1:].strip()
                    if line:
                        better_examples.append(line)
            
            evaluation.correction = correction or task.expected_answer or user_answer
            evaluation.explanation = explanation.strip()
            evaluation.better_examples = better_examples[:2]
            evaluation.feedback = feedback_text
            
        except Exception:
            evaluation.correction = task.expected_answer or user_answer
            evaluation.explanation = "Silakan periksa tata bahasa dan kosakata Anda."
            evaluation.better_examples = []
            evaluation.feedback = evaluation.correction
        
        return evaluation
