"""
Shared keyword extraction for turning a natural-language question
into search terms for the Bills/Hansard/Parliament APIs.

Previously this logic was duplicated (and inconsistently maintained)
in both BillsAPIClient and BillLensResearcher, each with an incomplete
stopword list. That caused filler words like "of" or "has" to slip
through as the "topic" when every real content word happened to be a
stopword -- e.g. "Who is the prime minister of the UK?" reduced to
just "of", which was then sent to the Bills API and matched almost
any bill containing that substring (Office, Offences, Off-patent...).
"""

from __future__ import annotations

# Keep the stop-word list focused on true grammatical filler words and
# pronouns. Previously this list included domain words (e.g. "bill",
# "parliament", "prime", "minister") which often removed the only
# meaningful tokens in a user's question and caused the system to
# fallback to a small housing-only dataset.
STOP_WORDS: set[str] = {
    "a", "an", "the", "and", "or", "but", "if", "so", "than", "then",
    "of", "in", "on", "at", "to", "for", "with", "about", "by", "from",
    "as", "into", "over", "under", "between", "during",
    "it", "its", "they", "them", "their", "this", "that", "these", "those",
    "i", "you", "he", "she", "we", "us", "our", "your",
    "is", "are", "was", "were", "be", "been", "being",
    "do", "does", "did", "doing", "done",
    "has", "have", "had", "having",
    "will", "would", "shall", "should", "can", "could", "may", "might", "must",
    "what", "which", "who", "whom", "whose", "when", "where", "why", "how",
    "tell", "me", "please", "recent", "current", "latest", "any", "some",
    "know", "explain", "show", "give",
    "uk",
}


def extract_keywords(text: str, max_keywords: int = 3) -> str:
    """
    Extract up to `max_keywords` meaningful search terms from a
    natural-language question, in their original order.

    This function is conservative by default but now falls back to a
    relaxed extraction when the strict filtering removes all tokens.

    Returns an empty string only if no candidate tokens of length > 2
    are present.
    """
    words = [w.strip("?.,!\"'():;").lower() for w in text.split()]
    # Strict pass: remove stop words and short tokens
    keywords = [w for w in words if len(w) > 2 and w not in STOP_WORDS]

    if not keywords:
        # Relaxed fallback: keep any token longer than 2 characters
        fallback = [w for w in words if len(w) > 2]
        if not fallback:
            return ""
        # Preserve original order and limit to `max_keywords`
        ordered = []
        seen = set()
        for w in fallback:
            if w not in seen:
                seen.add(w)
                ordered.append(w)
            if len(ordered) >= max_keywords:
                break
        return " ".join(ordered)

    # Prefer the longest `max_keywords` tokens but preserve original order
    keep = set(sorted(keywords, key=len, reverse=True)[:max_keywords])
    ordered: list[str] = []
    seen: set[str] = set()
    for word in keywords:
        if word in keep and word not in seen:
            seen.add(word)
            ordered.append(word)

    return " ".join(ordered)
