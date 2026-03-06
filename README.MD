# AI Language Production Trainer

A bilingual language trainer that helps Indonesian learners actively produce English sentences. The system uses LLM-based evaluation and adaptive difficulty based on Vygotsky's Zone of Proximal Development theory.

## Features

- **6 Task Types**: word translation, phrase translation, sentence translation, constrained production, context production, paragraph production
- **AI Evaluation**: LLM-powered evaluation with scores for grammar, vocabulary, naturalness, and task completion
- **Bilingual Feedback**: Explanations in Indonesian with English examples
- **Adaptive Difficulty**: Levels 1–10 that adjust based on your success rate (target: 70%)
- **Error Profiling**: Tracks common error patterns to target your weaknesses
- **Persistent Progress**: SQLite database stores your history across sessions

## Setup

### 1. Clone and install dependencies

```bash
cd language-trainer
pip install -r backend/requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
```

Get a free API key at [openrouter.ai](https://openrouter.ai).

### 3. Run the CLI trainer

```bash
python backend/cli.py
```

## Usage

```
=== AI Language Production Trainer ===
Selamat datang! Sistem ini akan melatih kemampuan produksi bahasa Inggris kamu.

Username: user123
Starting Level: 1

---

[Task 1] Level: 1

Terjemahkan kata berikut ke bahasa Inggris: 'berlari'

Jawaban kamu: > run

✓ Benar!
Vocabulary: 5/5
Task completion: 5/5
```

## Project Structure

```
language-trainer/
├── backend/
│   ├── app/
│   │   ├── config/          # Language pair config, task type weights
│   │   ├── database/        # SQLite setup and schema
│   │   ├── llm/             # OpenRouter client and prompt templates
│   │   ├── models/          # Data models (User, Task, Evaluation)
│   │   └── services/
│   │       ├── task_builders/  # 6 task type builders
│   │       ├── task_generator.py   # Weighted task selection
│   │       ├── evaluator.py        # LLM evaluation
│   │       ├── feedback_generator.py  # Bilingual feedback
│   │       ├── skill_tracker.py    # User progress tracking
│   │       └── difficulty_engine.py   # Adaptive difficulty
│   ├── cli.py               # Interactive CLI interface
│   └── requirements.txt
├── data/
│   ├── vocabulary/          # 60 words (beginner/intermediate/advanced)
│   ├── phrases/             # 20 common phrases
│   ├── sentences/           # 20 translation pairs
│   └── grammar/             # 10 grammar structures
├── .env.example
└── .gitignore
```

## Task Types

| Type | Level Range | Description |
|------|-------------|-------------|
| Word Translation | 1–3 | Translate a single Indonesian word to English |
| Phrase Translation | 2–5 | Translate an Indonesian phrase to English |
| Sentence Translation | 3–7 | Translate a full Indonesian sentence to English |
| Constrained Production | 3–8 | Write an English sentence using a specific word |
| Context Production | 5–10 | Write one English sentence about a given topic |
| Paragraph Production | 7–10 | Write a short English paragraph (3–4 sentences) |

## Adaptive Difficulty

| Success Rate | Action |
|---|---|
| > 85% | Level up |
| 50–85% | Maintain level |
| < 50% | Level down |

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | — | Required for LLM evaluation |
| `DATABASE_PATH` | `./language_trainer.db` | SQLite database path |
| `DEFAULT_MODEL` | `meta-llama/llama-3.2-3b-instruct:free` | LLM model to use |
| `TARGET_SUCCESS_RATE` | `0.70` | Target success rate for difficulty adjustment |
| `LLM_TIMEOUT` | `30` | Timeout in seconds for LLM API calls |
