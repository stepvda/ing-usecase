"""Fills the model_assisted fields with ONE structured call per page.

sieg 14/09, new module - answers "will you use my .env.example?": yes, same
provider order and same env-var names (GROQ_API_KEY[_2/_3] -> OPENROUTER_API_KEY
-> CEREBRAS_API_KEY -> SAMBANOVA_API_KEY -> OLLAMA_HOST), because it's already
a working pattern and there's no reason to invent a second one for this
project. Only the LLM section of your .env.example is relevant here - the
market-data/news/academic keys belong to portfolio_forecasting, not this repo.

WHY ONE CALL, NOT AN AGENT: same reasoning as the rest of this project (see
README "why a chain, not an agent"). Every page gets the same fixed prompt and
schema, applied identically - consistency across banks is the point, not
autonomous tool use. This is a feature-extraction call, nothing decides
anything here.

Providers are called via their OpenAI-compatible chat-completions endpoint
directly (requests), so this needs no per-provider SDK. VERIFY the base URLs
below against each provider's current docs before relying on the fallbacks -
Groq and OpenRouter are ones I'm confident about, Cerebras/SambaNova less so.
"""
from __future__ import annotations

import json
import os

import requests
from pydantic import BaseModel, ValidationError

MODEL_FIELDS = (
    "primary_product", "dominant_image_type", "people_present", "imagery_register",
    "institutional_trust_signal_present", "youth_student_targeting",
    "secondary_bank_positioning", "expat_cross_border_targeting",
    "branch_network_cited_as_benefit", "first_time_investor_targeting",
    "senior_preretirement_targeting",
)

SYSTEM_PROMPT = """You are extracting structured features from a bank campaign page for a
comparison across several banks. Apply the SAME criteria to every bank - consistency across
banks matters more than being generous to any single one.

Return ONLY a JSON object with exactly these keys:
- "primary_product": string, the specific product named on the page, in the page's own words
- "dominant_image_type": one of "photo", "illustration", "render_3d", "icon_only", "none"
- "people_present": boolean, whether any image on the page shows people
- "imagery_register": one of "lifestyle", "product", "abstract", "mixed", "none"
- "institutional_trust_signal_present": boolean, does the page invoke tenure, customer count,
  or ownership backing (e.g. state ownership) as a trust/safety argument
- "youth_student_targeting": boolean, is a junior/student account or youth-oriented offer promoted
- "secondary_bank_positioning": boolean, does the bank frame itself as an ADDITION to an existing
  bank ("keep your bank, add us") rather than a full replacement
- "expat_cross_border_targeting": boolean, does the page target expats/international clients
- "branch_network_cited_as_benefit": boolean, does the page explicitly cite branch/ATM network
  size as an advantage
- "first_time_investor_targeting": boolean, does the page frame investing as a first step for a
  novice (beginner glossary, low/no minimum amount) rather than assuming existing experience
- "senior_preretirement_targeting": boolean, does the page target a pre-retirement/senior life
  stage (pension planning, wealth transfer or succession, end-of-career estate management)

No preamble, no markdown fences, JSON only."""


class ModelAssistedFields(BaseModel):
    primary_product: str
    dominant_image_type: str
    people_present: bool
    imagery_register: str
    institutional_trust_signal_present: bool
    youth_student_targeting: bool
    secondary_bank_positioning: bool
    expat_cross_border_targeting: bool
    branch_network_cited_as_benefit: bool
    first_time_investor_targeting: bool
    senior_preretirement_targeting: bool


class LLMExtractionError(Exception):
    """Raised when every provider fails or the response can't be validated."""


# (env var prefix, chat-completions URL, model env var, default model)
# sieg 14/09: same order as .env.example - Groq first (with key rotation),
# then hosted fallbacks, then local Ollama for dev.
_PROVIDERS = [
    ("GROQ_API_KEY", "https://api.groq.com/openai/v1/chat/completions", "GROQ_MODEL", "openai/gpt-oss-120b"),
    ("OPENROUTER_API_KEY", "https://openrouter.ai/api/v1/chat/completions", "OPENROUTER_MODEL", "openai/gpt-oss-120b:free"),
    ("CEREBRAS_API_KEY", "https://api.cerebras.ai/v1/chat/completions", "CEREBRAS_MODEL", "llama-3.3-70b"),
    ("SAMBANOVA_API_KEY", "https://api.sambanova.ai/v1/chat/completions", "SAMBANOVA_MODEL", "Meta-Llama-3.3-70B-Instruct"),
]


def _groq_keys() -> list[str]:
    keys = [os.getenv("GROQ_API_KEY"), os.getenv("GROQ_API_KEY_2"), os.getenv("GROQ_API_KEY_3")]
    return [k for k in keys if k]


def _call_openai_compatible(url: str, api_key: str, model: str, user_prompt: str) -> str:
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def _call_ollama(user_prompt: str) -> str:
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3.1")
    response = requests.post(
        f"{host}/v1/chat/completions",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def _call_llm(user_prompt: str) -> str:
    """Try Groq (with key rotation on failure), then each hosted fallback in
    order, then local Ollama last. Raises only if every option fails."""
    errors: list[str] = []

    for key in _groq_keys():
        try:
            return _call_openai_compatible(_PROVIDERS[0][1], key, os.getenv("GROQ_MODEL", _PROVIDERS[0][3]), user_prompt)
        except requests.RequestException as exc:  # noqa: PERF203 - rotation needs the loop
            errors.append(f"groq: {exc}")

    for env_key, url, model_env, default_model in _PROVIDERS[1:]:
        api_key = os.getenv(env_key)
        if not api_key:
            continue
        try:
            return _call_openai_compatible(url, api_key, os.getenv(model_env, default_model), user_prompt)
        except requests.RequestException as exc:
            errors.append(f"{env_key}: {exc}")

    try:
        return _call_ollama(user_prompt)
    except requests.RequestException as exc:
        errors.append(f"ollama: {exc}")

    raise LLMExtractionError(f"every provider failed: {'; '.join(errors)}")


def extract_model_assisted(page_text: str, *, image_count: int, has_animation: bool, retries: int = 1) -> ModelAssistedFields:
    """Run the extraction with validation + one retry on a bad response."""
    user_prompt = (
        f"Page text (truncated): {page_text[:3000]}\n\n"
        f"Image count on page: {image_count}\n"
        f"Contains animation/video: {has_animation}"
    )
    last_error: Exception | None = None
    for _ in range(retries + 1):
        raw = _call_llm(user_prompt)
        cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        try:
            data = json.loads(cleaned)
            return ModelAssistedFields.model_validate(data)
        except (json.JSONDecodeError, ValidationError) as exc:
            last_error = exc
            continue
    raise LLMExtractionError(f"could not get a valid structured response after {retries + 1} attempt(s): {last_error}")
