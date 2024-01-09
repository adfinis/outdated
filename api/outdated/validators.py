from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any

    from rest_framework_json_api.serializers import Serializer

type ValidatorFunction = Callable[[dict[str, Any], Serializer], None]


def with_context(func: ValidatorFunction) -> ValidatorFunction:
    def wrapper(attrs: dict[str, Any], serializer: Serializer) -> None:
        func(attrs, serializer)

    wrapper.requires_context = True
    return wrapper
