from django import template
from django.utils.safestring import mark_safe
import environ

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
