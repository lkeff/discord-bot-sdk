import re
from typing import Any

SENSITIVE_PATTERNS = [
    # Emails
    (re.compile(r"[\w\.-]+@[\w\.-]+"), "[REDACTED_EMAIL]"),
    # Phone numbers (simple, generic)
    (re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"), "[REDACTED_PHONE]"),
    # Discord tokens (basic pattern)
    (re.compile(r"[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}"), "[REDACTED_TOKEN]"),
    # Profanity (expand list as needed)
    (re.compile(r"fuck|shit|bitch|asshole", re.IGNORECASE), "[REDACTED_PROFANITY]")
]

def redact_sensitive(text: Any) -> str:
    """Redacts sensitive info from a string."""
    if not isinstance(text, str):
        text = str(text)
    for pattern, repl in SENSITIVE_PATTERNS:
        text = pattern.sub(repl, text)
    return text
