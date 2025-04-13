from typing import Any, Optional

class ResponseUtils:
    @staticmethod
    def success(data: Optional[Any] = None, message: str = "Успешно") -> dict:
        response = {"result": True, "message": message}
        if data is not None:
            response["data"] = data
        return response

    @staticmethod
    def error(message: str = "Произошла ошибка") -> dict:
        return {"result": False, "message": message}