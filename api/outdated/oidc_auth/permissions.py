from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

from rest_framework.permissions import SAFE_METHODS, BasePermission

if TYPE_CHECKING:
    from collections.abc import Sequence

    from django.views import View

    from .models import OIDCUser


class Request(Protocol):  # pragma: no cover
    """Request protocol for permissions."""

    @property
    def method(self) -> str: ...

    @property
    def user(self) -> None | OIDCUser: ...


class ObjectPermissionIsHasPermission(BasePermission):
    """Base Class for Permissions that makes has_object_permission equal to has_permission."""

    def has_object_permission(self, request: Request, view: View, _: Any) -> bool:  # noqa: ANN401
        return self.has_permission(request, view)


class IsAuthenticated(ObjectPermissionIsHasPermission):
    """Allow only authenticated users."""

    def has_permission(self, request: Request, _: View) -> bool:
        return bool(request.user and request.user.is_authenticated)


class IsAdmin(ObjectPermissionIsHasPermission):
    """Allow only admin users."""

    def has_permission(self, request: Request, _: View) -> bool:
        return getattr(request.user, "is_admin", False)


def normalize(permission: type[BasePermission]) -> type[BasePermission]:
    """Normalize permission so admin bypasses it and authentication is required."""
    return IsAuthenticated & (permission | IsAdmin)


def is_methods(
    methods: Sequence[str], normalized: bool = False
) -> type[BasePermission]:
    """Allow only specified methods."""

    def has_permission(self: BasePermission, request: Request, view: View) -> bool:
        return request.method in methods

    permission = type(
        "IsMethod",
        (ObjectPermissionIsHasPermission,),
        {
            "has_permission": has_permission,
            "__doc__": """Allow only specified methods.""",
        },
    )

    return normalize(permission) if normalized else permission


def is_readonly(normalized: bool = True) -> type[BasePermission]:
    """Allow only readonly methods."""
    return is_methods(SAFE_METHODS, normalized)
