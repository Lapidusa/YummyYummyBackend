import os
import httpx
import random
from typing import Optional
from datetime import datetime, timedelta

import logger
import redis
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class SmsCode:
    def __init__(self, phone_number: str, code: str, expiration: timedelta):
        self.phone_number = phone_number
        self.code = code
        self.expiration_time = datetime.utcnow() + expiration

    def is_valid(self, code: str) -> bool:
        return self.code == code and datetime.utcnow() < self.expiration_time

class SmsService:
    API_URL = os.getenv("SMS_API_URL")
    API_KEY = os.getenv("SMS_API_KEY")

    def __init__(self):
        self.client = httpx.AsyncClient(headers={"Authorization": f"Bearer {self.API_KEY}"})
        self.redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)

    async def send_sms(self, phone_number: str) -> Optional[dict]:
      verification_code = self.generate_verification_code()
      logger.info(f"Generated verification code: {verification_code}")

      # Установим код в Redis с таймаутом в 5 минут
      success = await self.redis_client.setex(phone_number, timedelta(minutes=5), verification_code)
      if not success:
        logger.error(f"Failed to save verification code for {phone_number}")
        return None

      # Отправляем SMS
      message = f"Ваш код подтверждения: {verification_code}. Никому не сообщайте код."
      payload = {
        "number": "79856010277",
        "destination": phone_number,
        "text": message
      }
      try:
        response = await self.client.post(self.API_URL, json=payload)
        print(response)
        response.raise_for_status()
        return response.json()
      except httpx.HTTPError as e:
        logger.error(f"Ошибка при отправке SMS: {e}")
        return None

    @staticmethod
    def generate_verification_code() -> str:
        return str(random.randint(100000, 999999))

    def verify_sms_code(self, phone_number: str, code: str) -> bool:
        stored_code = self.redis_client.get(phone_number)
        if stored_code:
            # Decode the stored code and check if it matches
            return stored_code.decode('utf-8') == code
        return False

    def delete_sms_code(self, phone_number: str):
        self.redis_client.delete(phone_number)