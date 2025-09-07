from agents.moderation_agent import moderate_message

def test_phone_detection():
    r = moderate_message("Call 9876543210")
    assert r["status"] in ("PhoneDetected", "Mixed")
    assert "phone" in r["labels"]

def test_abusive_detection():
    r = moderate_message("You are an idiot")
    assert r["status"] == "Abusive"
    assert "abusive" in r["labels"]

def test_spam_link_detection():
    r = moderate_message("Click here http://spam.com for free money")
    assert r["status"] in ("Spam", "Mixed")
    assert "spam" in r["labels"] or "spam_link" in r["labels"]

def test_safe_message():
    r = moderate_message("Is this still available?")
    assert r["status"] == "Safe"
    assert r["labels"] == []
