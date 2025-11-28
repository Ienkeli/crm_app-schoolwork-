import re

def normalize_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone or "")
    if len(digits) < 10: return ""
    if len(digits) == 10: return "7" + digits
    if len(digits) == 11 and digits.startswith("8"): return "7" + digits[1:]
    if len(digits) == 11 and digits.startswith("7"): return digits
    if len(digits) >= 10: return "7" + digits[-10:]
    return ""

def format_phone_for_db(normalized: str) -> str:
    if not normalized: return ""
    return "+7" + normalized[1:]
