import httpx
import random
from typing import Optional
from datetime import datetime, timedelta

class SmsCode:
    def __init__(self, phone_number: str, code: str, expiration: timedelta):
        self.phone_number = phone_number
        self.code = code
        self.expiration_time = datetime.utcnow() + expiration

    def is_valid(self, code: str) -> bool:
       return self.code == code and datetime.utcnow() < self.expiration_time

class SmsService:
    API_URL = "https://api.exolve.ru/messaging/v1/SendSMS"
    API_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJRV05sMENiTXY1SHZSV29CVUpkWjVNQURXSFVDS0NWODRlNGMzbEQtVHA0In0.eyJleHAiOjIwNTU5MzExNjEsImlhdCI6MTc0MDU3MTE2MSwianRpIjoiOTE5Y2RjYmMtNWEzMi00MTJlLWJhNWQtYzEyM2VkNjUxOGFjIiwiaXNzIjoiaHR0cHM6Ly9zc28uZXhvbHZlLnJ1L3JlYWxtcy9FeG9sdmUiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiZTIwMmFkZDAtZTNmMC00ZGU4LTg5MTEtOWQxZmU1MmQ2OGY0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiY2EwY2FkODAtNjZmMC00MTRiLTg3MmItYTllZmI5OWQ5ODViIiwic2Vzc2lvbl9zdGF0ZSI6Ijc3MWE0ZTY4LWM3N2EtNDZkZS04OWQ5LTYyYTUwMmFlZWM5MSIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1leG9sdmUiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJleG9sdmVfYXBwIHByb2ZpbGUgZW1haWwiLCJzaWQiOiI3NzFhNGU2OC1jNzdhLTQ2ZGUtODlkOS02MmE1MDJhZWVjOTEiLCJ1c2VyX3V1aWQiOiIyMDM5MzQyYS01YWMyLTQwMTEtOWNkYy0zMzg2ODUwNGU0MWMiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImNsaWVudElkIjoiY2EwY2FkODAtNjZmMC00MTRiLTg3MmItYTllZmI5OWQ5ODViIiwiY2xpZW50SG9zdCI6IjE3Mi4xNi4xNjEuMTkiLCJhcGlfa2V5Ijp0cnVlLCJhcGlmb25pY2Ffc2lkIjoiY2EwY2FkODAtNjZmMC00MTRiLTg3MmItYTllZmI5OWQ5ODViIiwiYmlsbGluZ19udW1iZXIiOiIxMjg5MjAzIiwiYXBpZm9uaWNhX3Rva2VuIjoiYXV0ODIwYmE5MmEtNGE5Ni00ZDk5LTgzZjktZTI1ODJiZDQ4MTU1IiwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LWNhMGNhZDgwLTY2ZjAtNDE0Yi04NzJiLWE5ZWZiOTlkOTg1YiIsImN1c3RvbWVyX2lkIjoiOTQ2MTgiLCJjbGllbnRBZGRyZXNzIjoiMTcyLjE2LjE2MS4xOSJ9.d8jr0pFeqk1P0-0IPr5RNmI7F59IUK25vr73-0cZAz8-CshE6rSJM7pUetx_UJJTFpcEbhiXx3xPnfCDzD6kydc2Nc_eMVy1kvCqKj8-qZnetg7lrBKKojGpZoX4jQK6v4NFZ3zK-SbK13vU8_DdVvpOzO3LLiaEepaWliOiOUP97sstC7UodyOA-zGHJvcTm34J89aR3uANMKPf6tBBT8c_0f0P2zyeVZXK0fXUwfRhG1E7S3vJ1a9Q_XxmmW8gFv4GiI8qGnzaprCATKMF3gK0cNgGpoUgOpqV9bj0nM2zxKSd3CxjLuDJFNa_0-8fLomfFMsI40yn3qT-mAOsCA"

    def __init__(self):
        self.client = httpx.AsyncClient(headers={"Authorization": f"Bearer {self.API_KEY.encode('utf-8')}"})
        self.sms_codes = {}

    async def send_sms(self, phone_number: str) -> Optional[dict]:
        # verification_code = self.generate_verification_code()

        verification_code = "111111"
        # Сохранение кода в памяти
        self.sms_codes[phone_number] = SmsCode(phone_number, verification_code, timedelta(minutes=5))
        return {"result": True}
        #
        # # Отправка SMS
        # message = f"Ваш код подтверждения: {verification_code}"
        # payload = {
        #     "number": "79830667260",
        #     "destination": phone_number,
        #     "text": message
        # }
        # try:
        #     response = await self.client.post(self.API_URL, json=payload)
        #     response.raise_for_status()
        #     return response.json()
        # except httpx.HTTPError as e:
        #     print(f"Ошибка при отправке SMS: {e}")
        #     return None

    @staticmethod
    def generate_verification_code() -> str:
        return str(random.randint(100000, 999999))

    def get_sms_code(self, phone_number: str) -> Optional[SmsCode]:
        return self.sms_codes.get(phone_number)

    def delete_sms_code(self, phone_number: str):
        if phone_number in self.sms_codes:
            del self.sms_codes[phone_number]