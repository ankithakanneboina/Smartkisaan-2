from abc import ABC, abstractmethod
class OTPProvider(ABC):
    @abstractmethod
    def send_otp(self, phone_number: str, otp: str) -> bool:
        raise NotImplementedError
