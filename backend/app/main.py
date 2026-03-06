from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.database import db
from app.database.db import initialize_database
from app.services.task_generator import GenerativeTaskGenerator
from app.services.skill_tracker import SkillTracker
from app.services.evaluator import Evaluator
from app.services.feedback_generator import FeedbackGenerator
from app.services.difficulty_engine import DifficultyEngine
from app.models.task import Task


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(title="Language Trainer API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

task_generator = GenerativeTaskGenerator()
evaluator = Evaluator()
feedback_generator = FeedbackGenerator()
difficulty_engine = DifficultyEngine()


class TaskGenerateRequest(BaseModel):
    username: str = "default"


class TaskEvaluateRequest(BaseModel):
    task_id: int
    answer: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/task/generate")
async def generate_task_endpoint(request: TaskGenerateRequest):
    """Generate new task for user"""
    skill_tracker = SkillTracker(request.username)
    skill_tracker.get_or_create_user()
    user_profile = skill_tracker.get_user_profile()

    task = task_generator.generate_task(user_profile)

    task_id = db.save_task(
        user_id=skill_tracker.user_id,
        task_type=task.task_type,
        instruction=task.instruction,
        expected_answer=task.expected_answer or "",
    )

    return {
        "task_id": task_id,
        "task_type": task.task_type,
        "instruction": task.instruction,
    }


@app.post("/api/task/evaluate")
async def evaluate_task_endpoint(request: TaskEvaluateRequest):
    """Evaluate user's answer"""
    task_data = db.get_task_by_id(request.task_id)
    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")

    task = Task(
        task_type=task_data["task_type"],
        instruction=task_data["instruction"],
        level=1,
        expected_answer=task_data.get("expected_answer") or None,
    )

    db.update_task_answer(request.task_id, request.answer)

    evaluation = evaluator.evaluate(task, request.answer)
    feedback_generator.generate(task, request.answer, evaluation)

    db.save_evaluation(
        task_id=request.task_id,
        grammar=evaluation.grammar,
        vocabulary=evaluation.vocabulary,
        naturalness=evaluation.naturalness,
        task_completion=evaluation.task_completion,
        is_correct=evaluation.is_correct,
        errors=str(evaluation.errors),
        error_types=str(evaluation.error_types),
    )

    user_data = db.get_user_by_id(task_data["user_id"])
    if user_data:
        skill_tracker = SkillTracker(user_data["username"])
        skill_tracker.get_or_create_user()

        for error_type in evaluation.error_types:
            db.update_user_error(skill_tracker.user_id, error_type)

        profile = skill_tracker.profile
        profile.total_tasks += 1
        if evaluation.is_correct:
            profile.correct_tasks += 1
        if profile.total_tasks > 0:
            profile.success_rate = profile.correct_tasks / profile.total_tasks

        new_level = difficulty_engine.adjust_level(profile)
        profile.level = new_level
        db.update_user_stats(
            user_id=skill_tracker.user_id,
            level=new_level,
            total_tasks=profile.total_tasks,
            correct_tasks=profile.correct_tasks,
        )

    return {
        "is_correct": evaluation.is_correct,
        "scores": {
            "grammar": evaluation.grammar,
            "vocabulary": evaluation.vocabulary,
            "naturalness": evaluation.naturalness,
            "task_completion": evaluation.task_completion,
            "average": evaluation.average_score,
        },
        "errors": evaluation.errors,
        "error_types": evaluation.error_types,
        "feedback": {
            "message": evaluation.feedback,
            "correction": evaluation.correction,
            "explanation": evaluation.explanation,
            "better_examples": evaluation.better_examples,
        },
    }


@app.get("/api/user/{username}/stats")
async def get_user_stats(username: str):
    """Get user statistics"""
    user_data = db.get_user(username)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    total = user_data["total_tasks"]
    correct = user_data["correct_tasks"]
    accuracy = correct / total if total > 0 else 0.0
    streak = db.get_user_streak(user_data["id"])

    return {
        "level": user_data["level"],
        "total_tasks": total,
        "correct_tasks": correct,
        "accuracy": accuracy,
        "streak": streak,
    }
