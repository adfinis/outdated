import json

from django.shortcuts import render

from .forms import PackageForm, ProjectForm, VersionForm
from .models import Package, Project, Version


# Create your views here.
def index(request):
    context = {}
    error_message = None
    if request.method == "POST":

        if "edit_project" in request.POST:
            data = ProjectForm(
                request.POST,
                instance=Project.objects.filter(pk=request.POST["edit_project"])[0],
            )
            if data.is_valid():
                data.save()
            else:
                error_message = "".join(
                    [
                        f"Error: {field}, {e[0]['message']}"
                        for field, e in json.loads(data.errors.as_json()).items()
                    ]
                )
        elif "delete_project" in request.POST:

            instances = Project.objects.filter(pk=request.POST["delete_project"])
            if instances:
                instances.delete()
            else:
                error_message = (
                    "The Project, you were trying to delete does not seem to exist."
                )
        context["error_message"] = error_message

    if request.GET.get("search", ""):
        context["projects"] = Project.objects.order_by("name").filter(
            name__icontains=request.GET["search"]
        )
    else:
        context["projects"] = Project.objects.order_by("name")
    return render(request, "projects.html", context)


def create(request):
    context = {}
    if request.method == "POST":
        package_form = PackageForm(request.POST)
        project_form = ProjectForm(request.POST)
        version_form = VersionForm(request.POST)
        success_message = None
        error_message = None
        if "create_package" in request.POST:
            if package_form.is_valid():
                package_form.save()

                success_message = "Package was successfully created"
                package_form = PackageForm(None)

            project_form = ProjectForm(None)
            version_form = VersionForm(None)
        elif "create_project" in request.POST:
            if project_form.is_valid():
                project_form.save(commit=True)

                success_message = "Project was successfully created"
                project_form = ProjectForm(None)

            package_form = PackageForm(None)
            version_form = VersionForm(None)
        elif "create_version" in request.POST:

            if version_form.is_valid():
                version_form.save()

                success_message = "Version was successfully added"
                version_form = VersionForm(None)
            package_form = PackageForm(None)
            project_form = ProjectForm(None)
        else:
            if "edit_package" in request.POST:
                edit_package_form = PackageForm(
                    request.POST,
                    instance=Package.objects.filter(pk=request.POST["edit_package"])[0],
                )
                if edit_package_form.is_valid():
                    edit_package_form.save()
                    success_message = "Package Updated!"

                else:
                    error_message = "".join(
                        [
                            f"Error: {field}, {e[0]['message']}"
                            for field, e in json.loads(
                                edit_package_form.errors.as_json()
                            ).items()
                        ]
                    )

            elif "edit_version" in request.POST:
                edit_version_form = VersionForm(
                    request.POST,
                    instance=Version.objects.filter(pk=request.POST["edit_version"])[0],
                )
                if edit_version_form.is_valid():
                    edit_version_form.save()
                    success_message = "Version Updated!"

                else:
                    error_message = "".join(
                        [
                            f"Error: {field}, {e[0]['message']}"
                            for field, e in json.loads(
                                edit_version_form.errors.as_json()
                            ).items()
                        ]
                    )

            elif "delete_version" in request.POST:

                instances = Version.objects.filter(pk=request.POST["delete_version"])
                if instances:
                    instances.delete()
                else:
                    error_message = (
                        "The Version, you were trying to delete does not seem to exist."
                    )
            elif "delete_package" in request.POST:
                instances = Package.objects.filter(pk=request.POST["delete_package"])
                if instances:
                    instances.delete()
                else:
                    error_message = (
                        "The Package, you were trying to delete does not seem to exist."
                    )
            package_form = PackageForm(None)
            project_form = ProjectForm(None)
            version_form = VersionForm(None)
        context["success_message"] = success_message
        context["error_message"] = error_message
    else:
        package_form = PackageForm(None)
        project_form = ProjectForm(None)
        version_form = VersionForm(None)

    if request.GET.get("search", ""):
        context["packages"] = Package.objects.order_by("name").filter(
            name__icontains=request.GET["search"]
        )
    else:
        context["packages"] = Package.objects.order_by("name")
    context["versions"] = Version.objects
    context["project_form"] = project_form
    context["package_form"] = package_form
    context["version_form"] = version_form
    return render(request, "create.html", context)
