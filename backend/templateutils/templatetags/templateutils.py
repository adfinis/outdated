from django import template
from django.utils.safestring import mark_safe
from projects.forms import PackageForm, ProjectForm, VersionForm
from projects.models import Package, Project, Version

register = template.Library()


@register.simple_tag
def submitButton(type: str, value: str):
    """Return a HTML button with given name and given text."""

    return mark_safe(
        f"<button name='{type}' value='{value}' type='submit' class='uk-button uk-button-secondary uk-margin-top uk-border-rounded'>submit</button>"
    )


@register.simple_tag
def get_versions(pk):
    """Return all Versions with given primary key."""
    return Version.objects.filter(package=int(pk))


@register.simple_tag
def get_package(foreign_key):
    """Get a package from a versions foreign-key."""
    return Package.objects.filter(pk=foreign_key)[0]


@register.simple_tag
def closeable_warning(text: str):
    """Return the HTML for a closable warning."""
    return mark_safe(
        f"""<div class="uk-alert-danger uk-margin-remove uk-flex uk-flex-middle" uk-alert>
        <a class="uk-alert-close" uk-close></a>
        <p>{text}</p>
        </div>"""
    )


@register.simple_tag
def warning(text: str):
    """Return the HTML for an unclosable warning."""
    return mark_safe(
        f'<div class="uk-alert-danger uk-margin-remove uk-flex uk-flex-middle" uk-alert><p>{text}</p></div>'
    )


@register.simple_tag
def package_form(pk: int):
    return PackageForm(None, instance=Package.objects.filter(pk=pk)[0])


@register.simple_tag
def version_form(pk: int):
    return VersionForm(None, instance=Version.objects.filter(pk=pk)[0])


@register.simple_tag
def project_form(pk: int):

    return ProjectForm(None, instance=Project.objects.filter(pk=pk)[0])
