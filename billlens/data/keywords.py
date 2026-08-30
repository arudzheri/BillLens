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
    "uk", "parliament", "parliamentary", "government", "bill", "bills",
    "law", "laws", "act", "acts", "legislation", "prime", "minister",
}


def extract_keywords(text: str, max_keywords: int = 3) -> str:
    """
    Extract up to `max_keywords` meaningful search terms from a
    natural-language question, in their original order.

    Returns an empty string if no meaningful keyword is found -- callers
    should treat that as "no clear topic" and skip the API search rather
    than searching on leftover filler words.
    """
    words = [w.strip("?.,!\"'():;").lower() for w in text.split()]
    keywords = [w for w in words if len(w) > 2 and w not in STOP_WORDS]

    if not keywords:
        return ""

    keep = set(sorted(keywords, key=len, reverse=True)[:max_keywords])
    ordered: list[str] = []
    seen: set[str] = set()
    for word in keywords:
        if word in keep and word not in seen:
            seen.add(word)
            ordered.append(word)

    return " ".join(ordered)