#!/usr/bin/env python3
"""
AI Language Production Trainer - CLI Interface
Indonesian to English language learning system
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from app.database.db import initialize_database
from app.models.user import UserProfile
from app.services.task_generator import GenerativeTaskGenerator
from app.services.evaluator import Evaluator
from app.services.feedback_generator import FeedbackGenerator
from app.services.skill_tracker import SkillTracker
from app.services.difficulty_engine import DifficultyEngine
from app.services.error_analyzer import ErrorAnalyzer


def print_separator():
    print("\n" + "-" * 50 + "\n")


def print_evaluation(evaluation, task_type: str):
    if evaluation.is_correct:
        print("✓ Benar!")
    else:
        print("✗ Belum tepat")

    print()

    if task_type == "word_translation":
        print(f"  Vocabulary: {evaluation.vocabulary}/5")
        print(f"  Task completion: {evaluation.task_completion}/5")
    elif task_type == "phrase_translation":
        print(f"  Grammar: {evaluation.grammar}/5")
        print(f"  Vocabulary: {evaluation.vocabulary}/5")
        print(f"  Naturalness: {evaluation.naturalness}/5")
        print(f"  Task completion: {evaluation.task_completion}/5")
    else:
        print(f"  Grammar: {evaluation.grammar}/5")
        print(f"  Vocabulary: {evaluation.vocabulary}/5")
        print(f"  Naturalness: {evaluation.naturalness}/5")
        print(f"  Task completion: {evaluation.task_completion}/5")


def print_feedback(evaluation):
    if evaluation.errors:
        print("\nErrors found:")
        for error in evaluation.errors:
            print(f"  - {error}")

    if evaluation.correction and evaluation.correction != "":
        print(f"\nKoreksi:")
        print(f"  {evaluation.correction}")

    if evaluation.explanation:
        print(f"\nPenjelasan:")
        print(f"  {evaluation.explanation}")

    if evaluation.better_examples:
        print(f"\nContoh yang lebih baik:")
        for ex in evaluation.better_examples:
            print(f"  {ex}")


def print_stats(profile: UserProfile, task_num: int):
    print(f"\nStatistik saat ini:")
    print(f"  Level: {profile.level}")
    success_pct = int(profile.success_rate * 100)
    print(f"  Success Rate: {success_pct}% ({profile.correct_tasks}/{profile.total_tasks})")
    if profile.avg_grammar_score > 0:
        print(f"  Avg Grammar: {profile.avg_grammar_score:.1f}/5")
    if profile.avg_vocabulary_score > 0:
        print(f"  Avg Vocabulary: {profile.avg_vocabulary_score:.1f}/5")


def main():
    print("=" * 50)
    print("  AI Language Production Trainer")
    print("  Indonesian -> English")
    print("=" * 50)
    print()
    print("Selamat datang! Sistem ini akan melatih")
    print("kemampuan produksi bahasa Inggris kamu.")
    print()

    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key or api_key == "your_api_key_here":
        print("⚠️  Peringatan: OPENROUTER_API_KEY tidak ditemukan.")
        print("   Set API key di file .env untuk evaluasi penuh.")
        print("   Evaluasi dasar akan tetap tersedia.\n")

    try:
        initialize_database()
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

    username = input("Username: ").strip()
    if not username:
        username = "user"

    skill_tracker = SkillTracker(username)
    profile = skill_tracker.get_or_create_user()
    difficulty_engine = DifficultyEngine()
    error_analyzer = ErrorAnalyzer()
    task_generator = GenerativeTaskGenerator()
    evaluator = Evaluator()
    feedback_gen = FeedbackGenerator()

    print(f"\nSelamat datang, {username}!")
    print(f"Level saat ini: {profile.level}")
    if profile.total_tasks > 0:
        print(f"Tasks sebelumnya: {profile.total_tasks}")

    task_num = 0

    while True:
        print_separator()
        task_num += 1
        print(f"[Task {task_num}] Level: {profile.level}")
        print()

        # Build a full profile dict for AI-based task generation
        user_profile = skill_tracker.get_user_profile()

        print("🤖 AI sedang membuat soal khusus untuk kamu...")
        try:
            task = task_generator.generate_task(user_profile)
        except RuntimeError as e:
            print(f"  (Task generation failed: {e})")
            continue

        print(f"\n{task.instruction}")
        print()

        try:
            user_answer = input("Jawaban kamu: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nTerima kasih! Sampai jumpa!")
            print_stats(profile, task_num)
            break

        if not user_answer:
            print("Jawaban kosong, melewati task...")
            continue

        print("\nMengevaluasi jawaban...")
        try:
            evaluation = evaluator.evaluate(task, user_answer)

            if not evaluation.is_correct or evaluation.errors:
                evaluation = feedback_gen.generate(task, user_answer, evaluation)
        except RuntimeError as e:
            print(f"  (Evaluasi LLM tidak tersedia: {e})")
            from app.models.evaluation import EvaluationResult
            evaluation = EvaluationResult(
                grammar=3, vocabulary=3, naturalness=3, task_completion=3,
                is_correct=True, errors=[], error_types=[]
            )

        print()
        print_evaluation(evaluation, task.task_type)

        if not evaluation.is_correct or evaluation.errors:
            print_feedback(evaluation)
        elif evaluation.is_correct:
            print("\nBagus! Jawaban kamu sudah benar.")

        new_level = difficulty_engine.adjust_level(profile)

        skill_tracker.update_after_task(task, user_answer, evaluation, new_level)

        if new_level != profile.level:
            if new_level > profile.level:
                print(f"\n🎉 Level naik! {profile.level} -> {new_level}")
            else:
                print(f"\n📉 Level turun. {profile.level} -> {new_level}")

        # Show weak areas from the error analyzer
        if profile.error_profile:
            top_errors = error_analyzer.get_priority_focus_areas(profile.error_profile, top_n=3)
            if top_errors:
                print(f"\n📌 Fokus latihan: {', '.join(top_errors)}")

        print_stats(profile, task_num)

        print()
        try:
            cont = input("Lanjutkan? (y/n) > ").strip().lower()
            if cont not in ("y", "ya", ""):
                print("\nTerima kasih sudah berlatih! Sampai jumpa!")
                break
        except (KeyboardInterrupt, EOFError):
            print("\n\nTerima kasih! Sampai jumpa!")
            break


if __name__ == "__main__":
    main()
