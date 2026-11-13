"""Input validation helpers."""


def validate_name(name: str) -> tuple[bool, str]:
    if not name or not name.strip():
        return False, "Please enter your name."
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters."
    return True, ""


def validate_resume_text(text: str, min_words: int = 50) -> tuple[bool, str]:
    if not text or not text.strip():
        return False, "Resume appears to be empty."
    word_count = len(text.split())
    if word_count < min_words:
        return False, f"Resume is too short ({word_count} words). Upload a fuller resume."
    return True, ""


def validate_api_key(key: str) -> tuple[bool, str]:
    if not key or not key.strip():
        return False, "OpenAI API key is required."
    if not key.strip().startswith("sk-"):
        return False, "That doesn't look like an OpenAI key (should start with 'sk-')."
    return True, ""