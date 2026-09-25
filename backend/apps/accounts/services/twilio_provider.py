import logging
from .base import OTPProvider
logger = logging.getLogger(__name__)
class TwilioOTPProvider(OTPProvider):
    def __init__(self, account_sid, auth_token, from_number):
        from twilio.rest import Client
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number
    def send_otp(self, phone_number: str, otp: str) -> bool:
        try:
            msg = self.client.messages.create(
                body=f"Your Smart Kisaan OTP is: {otp}. Valid 10 minutes. Do not share.",
                from_=self.from_number, to=phone_number)
            logger.info(f"OTP sent SID:{msg.sid}")
            return True
        except Exception as e:
            logger.error(f"Twilio failed: {e}")
            return False
