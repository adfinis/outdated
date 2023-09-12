from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class RepositoryURLValidator(RegexValidator):
    regex = r"([-_\w]+\.[-._\w]+)\/([-_\w]+)\/([-_\w]+)\.git"
    message = "Enter a valid url for a git repository."
