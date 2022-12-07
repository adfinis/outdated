from django import template
from django.utils.safestring import mark_safe
import environ
from projects.models import Version

env = environ.Env()

env.read_env(".env")

register = template.Library()


@register.simple_tag
def submitButton(name: str, text="submit"):

    return mark_safe(
        f"<button name='{name}' type='submit' class='uk-button uk-button-secondary uk-margin-top uk-border-rounded' >{text}</button>"
    )


@register.simple_tag
def get_env(key):
    return env.get_value(key, default="")


@register.simple_tag
def get_elements(pk):
    return Version.objects.filter(package=int(pk))


@register.simple_tag
def closeable_warning(text: str):
    return mark_safe(
        f'<div class="uk-alert-danger uk-margin-remove uk-border-rounded" uk-alert><a class="uk-alert-close" uk-close></a><p>{text}</p></div>'
    )


@register.simple_tag
def warning(text: str):
    return mark_safe(
        f'<div class="uk-alert-danger uk-margin-remove uk-border-rounded" uk-alert><p>{text}</p></div>'
    )
