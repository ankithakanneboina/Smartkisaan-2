import random, string, uuid, logging
from django.core.cache import cache

logger = logging.getLogger(__name__)
OTP_LENGTH, OTP_EXPIRY_SECONDS, OTP_MAX_ATTEMPTS = 6, 600, 5


def get_otp_provider():
    from .console_provider import ConsoleOTPProvider
    return ConsoleOTPProvider()


def send_otp(phone_number):
    cleaned = phone_number.strip().replace(" ", "").replace("-", "")
    if cleaned.startswith("0"): cleaned = "+91" + cleaned[1:]
    elif not cleaned.startswith("+"): cleaned = "+91" + cleaned
    otp = "".join(random.choices(string.digits, k=OTP_LENGTH))
    session_id = str(uuid.uuid4())
    cache.set(f"otp:{session_id}", {"otp": otp, "phone_number": cleaned, "attempts": 0, "verified": False}, timeout=OTP_EXPIRY_SECONDS)
    sent = get_otp_provider().send_otp(cleaned, otp)
    if not sent: cache.delete(f"otp:{session_id}")
    return {"session_id": session_id, "sent": sent, "phone_number": cleaned}


def verify_otp(session_id, otp_input):
    session = cache.get(f"otp:{session_id}")
    if not session: return {"verified": False, "phone_number": None, "error": "OTP expired. Request a new one."}
    if session["verified"]: return {"verified": True, "phone_number": session["phone_number"], "error": None}
    if session["attempts"] >= OTP_MAX_ATTEMPTS:
        cache.delete(f"otp:{session_id}")
        return {"verified": False, "phone_number": None, "error": "Too many attempts. Request a new OTP."}
    if session["otp"] != otp_input.strip():
        session["attempts"] += 1
        remaining = OTP_MAX_ATTEMPTS - session["attempts"]
        cache.set(f"otp:{session_id}", session, timeout=OTP_EXPIRY_SECONDS)
        return {"verified": False, "phone_number": None, "error": f"Incorrect OTP. {remaining} attempt(s) remaining."}
    session["verified"] = True
    cache.set(f"otp:{session_id}", session, timeout=OTP_EXPIRY_SECONDS)
    return {"verified": True, "phone_number": session["phone_number"], "error": None}


def consume_verified_session(session_id):
    session = cache.get(f"otp:{session_id}")
    if not session or not session.get("verified"): return None
    phone = session["phone_number"]
    cache.delete(f"otp:{session_id}")
    return phone
