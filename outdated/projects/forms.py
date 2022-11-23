from django import forms

from .models import Package, Project


def uikitify(fields):
    for _, field in fields.items():
        print(
            field.__class__.__name__,
        )
        field_supertype = field.__class__.__name__
        field_class = field.widget.attrs.get("class", "")
        if field_supertype == "DateField":
            field_class += " uk-input datepicker"
        elif field_supertype == "TextField" or field_supertype == "CharField":
            field_class += " uk-input "
        elif field_supertype == "ModelMultipleChoiceField":
            field_class += " uk-select "
        field.widget.attrs["class"] = field_class

    return fields


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = "__all__"
        override = True

    def __init__(self, *args, **kwargs):
        super(PackageForm, self).__init__(*args, **kwargs)
        self.fields = uikitify(self.fields)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields = uikitify(self.fields)
