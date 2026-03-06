def get_evaluation_prompt(task_type: str, instruction: str, user_answer: str,
                           expected_answer: str = None) -> str:
    expected_str = f"\nExpected answer: {expected_answer}" if expected_answer else ""
    
    return f"""You are an English language teacher evaluating a student's answer.

Task type: {task_type}
Task instruction (Indonesian): {instruction}
User answer (English): {user_answer}{expected_str}

Evaluate based on:
1. Grammar (0-5): Correctness of grammar
2. Vocabulary (0-5): Accuracy and appropriateness of word choice
3. Naturalness (0-5): How natural the English sounds
4. Task completion (0-5): Whether the task requirements were fulfilled

For word/phrase translations, be lenient with synonyms.
For sentence translations, focus on meaning preservation and grammar.
For production tasks, focus on grammar, coherence, and task satisfaction.

Return ONLY a JSON object, no other text:
{{
    "grammar": <score 0-5>,
    "vocabulary": <score 0-5>,
    "naturalness": <score 0-5>,
    "task_completion": <score 0-5>,
    "errors": [<list of specific error descriptions>],
    "error_types": [<list from: past_tense, article, preposition, word_choice, plural, subject_verb_agreement, tense, spelling, punctuation, missing_word, extra_word>]
}}"""
