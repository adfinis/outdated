from django import template
from django.utils.safestring import mark_safe
import environ

env = environ.Env()

env.read_env(".env")

register = template.Library()


@register.simple_tag
def submitButton():
    return mark_safe(
        f"<button type='submit' class='uk-button-danger uk-margin-top ' uk-icon='icon: check; ratio: 2;' ></button>"
    )


@register.simple_tag
def get_env(key):
    return env.get_value(key, default="")
