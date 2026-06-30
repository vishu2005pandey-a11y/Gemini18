"""Locale loader — returns translated strings for a given language code."""
from locales.en import STRINGS as EN_STRINGS
from locales.es import STRINGS as ES_STRINGS

_LOCALES: dict[str, dict] = {
    "en": EN_STRINGS,
    "es": ES_STRINGS,
}

def get(lang: str, key: str, **kwargs) -> str:
    """Return translated string, falling back to English if key missing."""
    locale = _LOCALES.get(lang, EN_STRINGS)
    text = locale.get(key) or EN_STRINGS.get(key, f"[{key}]")
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    return text

def available_languages() -> list[str]:
    return list(_LOCALES.keys())
