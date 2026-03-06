def get_word_task_prompt(word: dict, level: int) -> str:
    return f"""Buat instruksi singkat dalam bahasa Indonesia untuk menerjemahkan kata berikut ke bahasa Inggris.
Kata: {word['indonesian']}
Level: {level}

Format: Hanya tulis instruksi, tidak ada penjelasan tambahan.
Contoh: "Terjemahkan kata berikut ke bahasa Inggris: 'berlari'"
"""

def get_phrase_task_prompt(phrase: dict, level: int) -> str:
    return f"""Buat instruksi singkat dalam bahasa Indonesia untuk menerjemahkan frasa berikut ke bahasa Inggris.
Frasa: {phrase['indonesian']}
Level: {level}

Format: Hanya tulis instruksi, tidak ada penjelasan tambahan.
Contoh: "Terjemahkan frasa berikut ke bahasa Inggris: 'lari cepat'"
"""

def get_sentence_task_prompt(sentence: dict, level: int) -> str:
    return f"""Buat instruksi singkat dalam bahasa Indonesia untuk menerjemahkan kalimat berikut ke bahasa Inggris.
Kalimat: {sentence['indonesian']}
Level: {level}

Format: Hanya tulis instruksi, tidak ada penjelasan tambahan.
Contoh: "Terjemahkan kalimat berikut ke bahasa Inggris: 'Saya pergi ke sekolah kemarin.'"
"""

def get_constrained_task_prompt(constraint_word: str, grammar_structure: str, level: int) -> str:
    return f"""Buat instruksi dalam bahasa Indonesia untuk membuat kalimat bahasa Inggris dengan batasan tertentu.
Kata yang harus digunakan: {constraint_word}
Struktur tata bahasa: {grammar_structure}
Level: {level}

Format: Hanya tulis instruksi, tidak ada penjelasan tambahan.
Contoh: "Buat satu kalimat bahasa Inggris menggunakan kata 'because'."
"""

def get_context_task_prompt(topic: str, level: int) -> str:
    return f"""Buat instruksi dalam bahasa Indonesia untuk membuat satu kalimat bahasa Inggris tentang topik tertentu.
Topik: {topic}
Level: {level}

Format: Hanya tulis instruksi, tidak ada penjelasan tambahan.
Contoh: "Jelaskan dalam satu kalimat bahasa Inggris mengapa kamu belajar bahasa Inggris."
"""

def get_paragraph_task_prompt(topic: str, level: int) -> str:
    return f"""Buat instruksi dalam bahasa Indonesia untuk menulis paragraf pendek dalam bahasa Inggris.
Topik: {topic}
Level: {level}

Format: Hanya tulis instruksi, tidak ada penjelasan tambahan.
Contoh: "Tulis satu paragraf pendek (3-4 kalimat) tentang rutinitas pagi kamu."
"""
