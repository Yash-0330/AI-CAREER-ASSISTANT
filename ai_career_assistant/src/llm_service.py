"""Provider-agnostic LLM wrapper (Groq / OpenAI / Gemini).

All three expose an OpenAI-compatible /chat/completions endpoint, so the
OpenAI Python SDK works with each one — only base_url, api_key and model
change. This keeps vendor lock-in out of the project.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# provider -> (base_url, env var for key, default model, fallback models)
PROVIDERS = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "env_key": "GROQ_API_KEY",
        "default_model": "llama-3.3-70b-versatile",
        "models": [
            "llama-3.3-70b-versatile",                    # best quality/limit balance
            "meta-llama/llama-4-scout-17b-16e-instruct",  # 30K TPM, 1K RPD
            "llama-3.1-8b-instant",                       # fastest, 14,400 RPD
            "openai/gpt-oss-120b",
        ],
    },
    "openai": {
        "base_url": None,  # SDK default
        "env_key": "OPENAI_API_KEY",
        "default_model": "gpt-4o-mini",
        "models": ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "env_key": "GEMINI_API_KEY",
        "default_model": "gemini-2.5-flash",
        "models": ["gemini-2.5-flash", "gemini-2.5-flash-lite"],
    },
}


def get_provider_config(provider: str) -> dict:
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider '{provider}'. Choose from {list(PROVIDERS)}.")
    return PROVIDERS[provider]


class LLMService:
    def __init__(self, provider: str = "groq", api_key: str | None = None,
                 model: str | None = None):
        cfg = get_provider_config(provider)
        self.provider = provider
        self.model = model or cfg["default_model"]

        key = (api_key or os.getenv(cfg["env_key"]) or "").strip()
        if not key:
            raise ValueError(
                f"No API key found for {provider}. "
                f"Set {cfg['env_key']} in .env or paste it in the sidebar."
            )

        self.client = OpenAI(api_key=key, base_url=cfg["base_url"])

    def generate(self, prompt: str, system_prompt: str = "",
                 temperature: float = 0.4, max_tokens: int = 1500) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content or ""