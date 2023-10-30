from subprocess import run
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


class UUIDModel(models.Model):
    """Model which uses an uuid as primary key."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class UniqueBooleanField(models.BooleanField):
    """
    BooleanField that guarantees for one True record and sets others to `False`.

    By default only one record is allowed to be `True`. This can be further configured
    by providing a list of field names as `together` param.

    Example:
    -------
        ```
        >>> class Email(models.Model):
        ...     user = models.ForeignKey(User)
        ...     email = models.EmailField()
        ...     default = UniqueBooleanField(together=["user"])
        ```

        This will enforce three things:
         1. only allow for one entry where `default == True` per user
         2. if only one record exists for a given user, we set `default = True`,
            regardless of the input
         3. The same happens, if records exists, but none of them have `default = True`
    """

    def __init__(self, *args, together=None, **kwargs):
        self.together = together if together else []
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        model = model_instance.__class__
        together = model.objects.filter(
            **{t: getattr(model_instance, t, None) for t in self.together},
        ).exclude(pk=model_instance.pk)

        if getattr(model_instance, self.attname) is True:
            # If True then set all others as False
            together.filter(**{self.attname: True}).update(**{self.attname: False})

        elif not together.exists():
            # We're the only one, thus setting to True
            setattr(model_instance, self.attname, True)

        return super().pre_save(model_instance, add)


def validate_repo_exists(value: str) -> None:
    """Validate the existance of a remote git repository."""
    url = "https://" + value

    if value.startswith("file://") and settings.ENV == "test":
        url = value

    result = run(
        ["/usr/bin/git", "ls-remote", url],
        capture_output=True,
        check=False,
        shell=False,
    )
    if result.returncode != 0:
        raise ValidationError("Repository does not exist.", params={"value": value})


class RepositoryURLField(models.CharField):
    default_validators = [
        RegexValidator(
            regex=r"^([-_\w]+\.[-._\w]+)\/([-_\w]+)\/([-_\w]+)$",
            message="Invalid repository url",
        ),
        validate_repo_exists,
    ]
    description = "Field for git repository URLs."
