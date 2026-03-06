import os
import json
import requests
from typing import Optional

API_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_api_key() -> str:
    key = os.getenv("OPENROUTER_API_KEY", "")
    return key

def get_model() -> str:
    return os.getenv("DEFAULT_MODEL", "meta-llama/llama-3.2-3b-instruct:free")

def call_llm(prompt: str, system_prompt: Optional[str] = None, expect_json: bool = False) -> str:
    api_key = get_api_key()
    model = get_model()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/language-trainer",
        "X-Title": "Language Trainer"
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.3
    }

    try:
        timeout = int(os.getenv("LLM_TIMEOUT", "30"))
        response = requests.post(API_URL, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        if expect_json:
            content = content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
        return content
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"LLM API call failed: {e}")
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected LLM response format: {e}")
