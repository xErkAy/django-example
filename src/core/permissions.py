from rest_framework.request import Request


class IsAuthenticated:
    def has_permission(self, request: Request, view) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request: Request, view, obj) -> bool:
        return bool(request.user and request.user.is_authenticated)


class AllowAny:
    def has_permission(self, request: Request, view) -> bool:
        return True

    def has_object_permission(self, request: Request, view, obj) -> bool:
        return True
