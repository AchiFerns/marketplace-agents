"""
Chat Moderation Agent (Rule + regex based)

Provides `moderate_message(text)` which returns:
{
  "status": "Safe" | "Abusive" | "Spam" | "PhoneDetected" | "Mixed",
  "reason": "Short explanation",
  "labels": ["phone", "abuse", "spam_link", ...],
  "confidence": 0.0-1.0   # heuristic confidence
}
"""

import re

# Phone regexes (common formats, obfuscated with spaces/dashes)
PHONE_PATTERNS = [
    re.compile(r"\b\d{10}\b"),  # plain 10 digits
    re.compile(r"(?:\+?\d{1,3}[-\s]?)?\d{3}[-\s]?\d{3}[-\s]?\d{4}"),  # common grouping
    re.compile(r"\b(?:\d[\s\-\.\u2011]?){9,13}\d\b"),  # with separators
]

# Basic blacklist - expand as needed.
BLACKLIST = {
    "idiot", "stupid", "dumb", "f***", "bitch", "kys", "scam", "fraud", "kill",
    "asshole", "motherfucker", "screw you", "shut up"
}

# Spam indicators
SPAM_KEYPHRASES = [
    "click here", "buy now", "limited offer", "visit our", "subscribe", "free",
    "work from home", "earn money", "whatsapp group", "join now", "transfer", "upi"
]

# Simple url regex
URL_RE = re.compile(r"(https?://\S+|www\.\S+|\S+\.(com|in|net|org)\b)")

# Short helper
def contains_phone(text: str) -> bool:
    for p in PHONE_PATTERNS:
        if p.search(text):
            return True
    return False

def find_blacklisted_words(text: str):
    words = set(re.findall(r"\w+", text.lower()))
    return sorted(list(words & BLACKLIST))

def contains_url(text: str) -> bool:
    return bool(URL_RE.search(text.lower()))

def excessive_punctuation(text: str) -> bool:
    # e.g., "!!!!!!" or "???!!!" or repeated emoji/punctuations
    if re.search(r"[!?.]{4,}", text):
        return True
    return False

def repeated_chars(text: str) -> bool:
    # e.g., "loooooool", "hiiiiii"
    return bool(re.search(r"(.)\1{6,}", text, flags=re.IGNORECASE))

def spam_score_from_text(text: str) -> float:
    """Heuristic spam score 0..1 from various signals"""
    score = 0.0
    t = text.lower()
    if contains_url(t):
        score += 0.5
    if any(phrase in t for phrase in SPAM_KEYPHRASES):
        score += 0.3
    if re.search(r"\bfree\b|\bdiscount\b|\bpromo\b", t):
        score += 0.2
    if repeated_chars(t):
        score += 0.1
    if excessive_punctuation(t):
        score += 0.1
    return min(1.0, score)

def moderate_message(text: str) -> dict:
    """
    Analyze a chat message and return classification + reason.
    """
    if not isinstance(text, str):
        text = str(text)

    t = text.strip()
    labels = []
    reasons = []

    # Phone detection
    if contains_phone(t):
        labels.append("phone")
        reasons.append("Contains phone number or numeric contact info.")

    # URL / possible phishing / spam
    if contains_url(t):
        labels.append("spam_link")
        reasons.append("Contains a URL or domain link.")

    # Blacklisted abusive words
    abusive_found = find_blacklisted_words(t)
    if abusive_found:
        labels.append("abusive")
        reasons.append(f"Contains abusive/offensive words: {', '.join(abusive_found)}")

    # Spam signals
    spam_score = spam_score_from_text(t)
    if spam_score >= 0.35:
        labels.append("spam")
        reasons.append(f"High spam-like content (score={spam_score:.2f}).")

    # Excessive punctuation / repeated chars
    if excessive_punctuation(t):
        labels.append("excessive_punct")
        reasons.append("Excessive punctuation found.")
    if repeated_chars(t):
        labels.append("repeated_chars")
        reasons.append("Contains elongated/repeated characters (possible spam/noise).")

    # If none flagged, safe
    if len(labels) == 0:
        return {
            "status": "Safe",
            "reason": "No issues detected.",
            "labels": [],
            "confidence": 0.95
        }

    # Compose final status
    if "abusive" in labels:
        status = "Abusive"
    elif "phone" in labels and ("spam" in labels or "spam_link" in labels):
        status = "Mixed"
    elif "phone" in labels:
        status = "PhoneDetected"
    elif "spam" in labels or "spam_link" in labels:
        status = "Spam"
    else:
        status = "Flagged"

    # Heuristic confidence: combine signals (higher when stronger signals exist)
    conf = 0.2
    if "abusive" in labels:
        conf = max(conf, 0.8)
    if "spam" in labels or "spam_link" in labels:
        conf = max(conf, 0.6)
    if "phone" in labels:
        conf = max(conf, 0.7)
    # increase slightly if multiple labels
    conf = min(0.99, conf + 0.05 * (len(labels) - 1))

    return {
        "status": status,
        "reason": " | ".join(reasons),
        "labels": labels,
        "confidence": round(conf, 2)
    }


# Simple demo when run directly
if __name__ == "__main__":
    examples = [
        "Call me at 9876543210 for details.",
        "This is a limited offer! Click here: http://buycheap.com",
        "You are an idiot, go away!",
        "Selling brand new shoes. Free shipping. Visit www.shoedeals.com",
        "Hey, is this still available?",
        "LOOOOOOOL!!!!! best deal ever!!!",
    ]
    for ex in examples:
        print("MSG:", ex)
        print(moderate_message(ex))
        print("-" * 60)
