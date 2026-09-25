import logging
from .base import OTPProvider
logger = logging.getLogger(__name__)
class ConsoleOTPProvider(OTPProvider):
    def send_otp(self, phone_number: str, otp: str) -> bool:
        logger.warning(f"\n========================================\n  SMART KISAAN — DEV OTP\n  Phone  : {phone_number}\n  OTP    : {otp}\n  Set TWILIO_* vars for real SMS\n========================================")
        return True
