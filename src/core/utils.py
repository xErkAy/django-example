from typing import Any, Callable

from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class ExceptionWithMessage(APIException):
    status_code = 400
    default_detail = _("Ошибка")

    def __init__(self, detail: str = "Ошибка", code: int = 400) -> None:
        self.detail = _(detail)
        self.status_code = str(code)
        super().__init__(self.detail, self.status_code)


def atomic_transaction(message: str = "Произошла ошибка, обратитесь к администратору") -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: dict[str, Any]) -> Callable:
            try:
                with transaction.atomic():
                    return func(*args, **kwargs)
            except ExceptionWithMessage:
                raise
            except Exception:
                raise ExceptionWithMessage(message)

        return wrapper

    return decorator
