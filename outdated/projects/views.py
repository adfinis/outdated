from django.shortcuts import render


from .forms import PackageForm, ProjectForm, VersionForm
from .models import Project, Package, Version


# Create your views here.
def index(request):

    projects = Project.objects.order_by("name")
    context = {"projects": projects}
    return render(request, "projects.html", context)


def create(request):

    packages = Package.objects.order_by("name")
    versions = Version.objects
    context = {
        "packages": packages,
        "versions": versions,
        "unfiltered_packages": packages,
    }
    if request.method == "POST":
        package_form = PackageForm(request.POST)
        project_form = ProjectForm(request.POST)
        version_form = VersionForm(request.POST)
        success_message = None
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
        context["success_message"] = success_message

    else:
        package_form = PackageForm(None)
        project_form = ProjectForm(None)
        version_form = VersionForm(None)
    if request.method == "GET":
        if "package_search" in request.GET:
            context["packages"] = Package.objects.order_by("name").filter(
                name__icontains=request.GET["package_search"]
            )
    context["project_form"] = project_form
    context["package_form"] = package_form
    context["version_form"] = version_form
    return render(request, "create.html", context)
