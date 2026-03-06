#!/usr/bin/env python3
"""
Test script for the generative task system.

Run from the backend/ directory:
    python test_generative.py

Requires OPENROUTER_API_KEY to be set in .env or the environment.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from app.services.task_generator import GenerativeTaskGenerator
from app.services.error_analyzer import ErrorAnalyzer


def test_beginner():
    print("=" * 60)
    print("TEST 1: Beginner student (level 1, no history)")
    print("=" * 60)

    generator = GenerativeTaskGenerator()
    beginner_profile = {
        "level": 1,
        "total_tasks": 0,
        "success_rate": 0.0,
        "avg_grammar_score": 0,
        "avg_vocabulary_score": 0,
        "avg_naturalness_score": 0,
        "error_profile": {},
        "recent_tasks": []
    }

    task = generator.generate_task(beginner_profile)
    print(f"Task Type   : {task.task_type}")
    print(f"Instruction : {task.instruction}")
    print(f"Expected    : {task.expected_answer}")
    print(f"Acceptable  : {task.acceptable_answers}")
    print(f"Metadata    : {json.dumps(task.metadata, indent=2)}")
    print()
    return task


def test_intermediate_past_tense():
    print("=" * 60)
    print("TEST 2: Intermediate student with past-tense weakness")
    print("=" * 60)

    generator = GenerativeTaskGenerator()
    intermediate_profile = {
        "level": 4,
        "total_tasks": 20,
        "success_rate": 0.65,
        "avg_grammar_score": 3.2,
        "avg_vocabulary_score": 4.0,
        "avg_naturalness_score": 3.5,
        "error_profile": {
            "past_tense": 0.65,
            "articles": 0.30,
            "prepositions": 0.15
        },
        "recent_tasks": [
            {"task_type": "sentence_translation", "instruction": "Terjemahkan: 'Saya makan nasi tadi malam.'"},
        ]
    }

    task = generator.generate_task(intermediate_profile)
    print(f"Task Type   : {task.task_type}")
    print(f"Instruction : {task.instruction}")
    print(f"Expected    : {task.expected_answer}")
    print(f"Focus Area  : {task.metadata.get('focus_area')}")
    print(f"Target Errs : {task.metadata.get('target_errors')}")
    print()
    return task


def test_advanced():
    print("=" * 60)
    print("TEST 3: Advanced student (level 8)")
    print("=" * 60)

    generator = GenerativeTaskGenerator()
    advanced_profile = {
        "level": 8,
        "total_tasks": 80,
        "success_rate": 0.82,
        "avg_grammar_score": 4.3,
        "avg_vocabulary_score": 4.1,
        "avg_naturalness_score": 4.0,
        "error_profile": {
            "articles": 0.20,
            "word_choice": 0.15
        },
        "recent_tasks": [
            {"task_type": "paragraph_production", "instruction": "Tulis paragraf tentang rutinitas pagi kamu..."},
            {"task_type": "context_production", "instruction": "Jelaskan mengapa kamu belajar bahasa Inggris..."},
        ]
    }

    task = generator.generate_task(advanced_profile)
    print(f"Task Type   : {task.task_type}")
    print(f"Instruction : {task.instruction}")
    print(f"Expected    : {task.expected_answer}")
    print(f"Metadata    : {json.dumps(task.metadata, indent=2)}")
    print()
    return task


def test_error_analyzer():
    print("=" * 60)
    print("TEST 4: ErrorAnalyzer - priority focus areas")
    print("=" * 60)

    analyzer = ErrorAnalyzer()
    error_profile = {
        "past_tense": 0.65,
        "articles": 0.30,
        "prepositions": 0.15,
        "plural": 0.40,
        "word_choice": 0.10
    }

    top_errors = analyzer.get_priority_focus_areas(error_profile, top_n=3)
    print(f"Top 3 errors to focus on: {top_errors}")
    print()


if __name__ == "__main__":
    print("AI-Generative Language Trainer - Test Suite")
    print()

    test_error_analyzer()

    try:
        test_beginner()
        test_intermediate_past_tense()
        test_advanced()
        print("All generative tests passed!")
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
