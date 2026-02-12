"""Small text utilities extracted from prepare_corpus.py for easier testing.
"""
import unicodedata

allowed_lt = set("ąčęėįšųūž")


def remove_accent(c: str) -> str:
    # Preserve ASCII characters, whitespace, and explicitly allowed Lithuanian letters
    if c.isspace() or c.isascii() or c in allowed_lt:
        return c
    # Normalize to NFKD form then remove combining marks (category 'Mn')
    nkfd = unicodedata.normalize("NFKD", c)
    base_chars = [ch for ch in nkfd if unicodedata.category(ch) != "Mn"]
    return "".join(base_chars)


def normalize(param: str) -> str:
    """Clean the input text.

    - replace punctuations with spaces
    - collapse whitespace
    - casefold to lowercase
    - attempt to normalize accents (via NFKD)

    Returns (cleaned_text)
    """
    # remove punctuations
    res = "".join(c if c.isalnum() or c.isspace() else " " for c in param)
    # remove double spaces
    res = " ".join(res.split()).casefold()
    res = "".join([remove_accent(c) for c in res])
    return res
