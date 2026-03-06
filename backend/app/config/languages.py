LANGUAGE_CONFIG = {
    "source_language": "Indonesian",
    "source_language_code": "id",
    "target_language": "English",
    "target_language_code": "en",
    "instruction_language": "Indonesian",
    "answer_language": "English"
}

TASK_TYPES = {
    "word_translation": {
        "level_range": [1, 3],
        "weight_by_level": {1: 0.5, 2: 0.3, 3: 0.2}
    },
    "phrase_translation": {
        "level_range": [2, 5],
        "weight_by_level": {2: 0.3, 3: 0.4, 4: 0.3, 5: 0.2}
    },
    "sentence_translation": {
        "level_range": [3, 7],
        "weight_by_level": {3: 0.2, 4: 0.3, 5: 0.4, 6: 0.3, 7: 0.2}
    },
    "constrained_production": {
        "level_range": [3, 8],
        "weight_by_level": {3: 0.2, 4: 0.3, 5: 0.4, 6: 0.4, 7: 0.3, 8: 0.2}
    },
    "context_production": {
        "level_range": [5, 10],
        "weight_by_level": {5: 0.1, 6: 0.2, 7: 0.3, 8: 0.4, 9: 0.5, 10: 0.5}
    },
    "paragraph_production": {
        "level_range": [7, 10],
        "weight_by_level": {7: 0.1, 8: 0.2, 9: 0.3, 10: 0.4}
    }
}
