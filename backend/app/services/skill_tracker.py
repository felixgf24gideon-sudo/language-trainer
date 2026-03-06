import json
from app.models.user import UserProfile
from app.models.evaluation import EvaluationResult
from app.database import db


class SkillTracker:
    def __init__(self, username: str):
        self.username = username
        self._user_id = None
        self._profile = None

    def get_or_create_user(self) -> UserProfile:
        db.initialize_database()
        user_data = db.get_user(self.username)
        if not user_data:
            self._user_id = db.create_user(self.username)
            user_data = db.get_user(self.username)
        else:
            self._user_id = user_data["id"]

        error_profile = db.get_user_error_profile(self._user_id)

        success_rate = 0.0
        if user_data["total_tasks"] > 0:
            success_rate = user_data["correct_tasks"] / user_data["total_tasks"]

        self._profile = UserProfile(
            username=self.username,
            level=user_data["level"],
            total_tasks=user_data["total_tasks"],
            correct_tasks=user_data["correct_tasks"],
            success_rate=success_rate,
            error_profile=error_profile
        )
        return self._profile

    @property
    def user_id(self) -> int:
        return self._user_id

    def get_user_profile(self) -> dict:
        """
        Return a comprehensive profile dict suitable for task generation.
        Ensures get_or_create_user() has been called first.
        """
        if not self._profile:
            self.get_or_create_user()

        profile = self._profile
        recent_tasks = db.get_user_recent_tasks(self._user_id, limit=5)

        return {
            "user_id": self._user_id,
            "level": profile.level,
            "total_tasks": profile.total_tasks,
            "correct_tasks": profile.correct_tasks,
            "success_rate": profile.success_rate,
            "avg_grammar_score": profile.avg_grammar_score,
            "avg_vocabulary_score": profile.avg_vocabulary_score,
            "avg_naturalness_score": profile.avg_naturalness_score,
            "error_profile": profile.error_profile,
            "recent_tasks": [
                {
                    "task_type": t["task_type"],
                    "instruction": t["instruction"]
                }
                for t in recent_tasks
            ]
        }

    def update_after_task(self, task, user_answer: str, evaluation: EvaluationResult, new_level: int):
        if not self._profile:
            return

        task_id = db.save_task(
            user_id=self._user_id,
            task_type=task.task_type,
            instruction=task.instruction,
            expected_answer=task.expected_answer or "",
            user_answer=user_answer
        )

        db.save_evaluation(
            task_id=task_id,
            grammar=evaluation.grammar,
            vocabulary=evaluation.vocabulary,
            naturalness=evaluation.naturalness,
            task_completion=evaluation.task_completion,
            is_correct=evaluation.is_correct,
            errors=json.dumps(evaluation.errors),
            error_types=json.dumps(evaluation.error_types)
        )

        for error_type in evaluation.error_types:
            db.update_user_error(self._user_id, error_type)

        self._profile.total_tasks += 1
        if evaluation.is_correct:
            self._profile.correct_tasks += 1
        self._profile.level = new_level
        if self._profile.total_tasks > 0:
            self._profile.success_rate = self._profile.correct_tasks / self._profile.total_tasks

        db.update_user_stats(
            user_id=self._user_id,
            level=new_level,
            total_tasks=self._profile.total_tasks,
            correct_tasks=self._profile.correct_tasks
        )

        n = self._profile.total_tasks
        self._profile.avg_grammar_score = (
            (self._profile.avg_grammar_score * (n - 1) + evaluation.grammar) / n
        )
        self._profile.avg_vocabulary_score = (
            (self._profile.avg_vocabulary_score * (n - 1) + evaluation.vocabulary) / n
        )
        self._profile.avg_naturalness_score = (
            (self._profile.avg_naturalness_score * (n - 1) + evaluation.naturalness) / n
        )
