def get_feedback_prompt(task_type: str, instruction: str, user_answer: str,
                         evaluation: dict, expected_answer: str = None) -> str:
    expected_str = f"\nJawaban yang diharapkan: {expected_answer}" if expected_answer else ""
    errors_str = "\n".join(f"- {e}" for e in evaluation.get("errors", []))
    
    return f"""Kamu adalah guru bahasa Inggris yang memberikan umpan balik kepada pelajar Indonesia.

Instruksi tugas: {instruction}
Jawaban pengguna: {user_answer}{expected_str}
Nilai rata-rata: {(evaluation.get('grammar', 0) + evaluation.get('vocabulary', 0) + evaluation.get('naturalness', 0) + evaluation.get('task_completion', 0)) / 4:.1f}/5

Kesalahan ditemukan:
{errors_str if errors_str else "- Tidak ada kesalahan signifikan"}

Berikan umpan balik dalam format berikut (gunakan bahasa Indonesia untuk penjelasan, bahasa Inggris untuk contoh):

Koreksi:
[Tuliskan versi yang benar dari jawaban pengguna]

Penjelasan:
[Jelaskan kesalahan dan cara memperbaikinya dalam bahasa Indonesia. Sertakan contoh dalam bahasa Inggris.]

Contoh yang lebih baik:
[Berikan 2 contoh kalimat bahasa Inggris yang lebih baik]

Jaga umpan balik tetap singkat, jelas, dan mendidik."""
