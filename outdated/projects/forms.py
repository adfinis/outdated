from django import forms
from django.forms.utils import ErrorList
from django.utils.html import format_html, format_html_join

from .models import Package, Project, Version

from .environ import env


class UiKitErrorList(ErrorList):
    def as_uikit(self):
        if not self.data:
            return ""
        print(vars(self))
        return format_html(
            '<div class=" {}"  >{}</div>',
            self.error_class,
            format_html_join(
                "",
                """<div class="uk-alert-danger uk-margin-small-bottom" uk-alert>
            <a class="uk-alert-close" uk-close></a>
            <p>{}</p>
          </div>""",
                ((e,) for e in self),
            ),
        )

    def __str__(self):
        return self.as_uikit()


def uikitify(fields):
    for _, field in fields.items():
        field_supertype = field.__class__.__name__

        field_class = field.widget.attrs.get("class", "")
        if field_supertype == "DateField":
            field_class += " uk-input datepicker"
            field.widget.attrs[
                "pattern"
            ] = "[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])"
        elif (
            field_supertype == "TextField"
            or field_supertype == "CharField"
            or field_supertype == "URLField"
        ):
            field_class += " uk-input "
        elif (
            field_supertype == "ModelMultipleChoiceField"
            or field_supertype == "ModelChoiceField"
        ):
            field_class += " uk-select "

        field.widget.attrs["class"] = field_class + " uk-border-rounded"
    return fields


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = "__all__"
        override = True

    def __init__(self, *args, **kwargs):
        super(PackageForm, self).__init__(*args, **kwargs)
        self.fields = uikitify(self.fields)
        self.error_class = UiKitErrorList


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields = uikitify(self.fields)
        self.error_class = UiKitErrorList

        self.fields["used_packages"].widget.choices = [
            (
                package.name + ":",
                tuple(
                    tuple([version.pk, version.name])
                    for version in Version.objects.filter(package=package.pk)
                ),
            )
            for package in Package.objects.all()
            if Version.objects.filter(package=package.pk)
        ]


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)
        self.fields = uikitify(self.fields)
        self.error_class = UiKitErrorList
