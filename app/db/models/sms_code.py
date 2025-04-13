from datetime import datetime, timedelta

class SmsCode:
    def __init__(self, phone_number: str, code: str, expiration: timedelta):
        self.phone_number = phone_number
        self.code = code
        self.expiration_time = datetime.utcnow() + expiration

    def is_valid(self, code: str) -> bool:
        return self.code == code and datetime.utcnow() < self.expiration_time