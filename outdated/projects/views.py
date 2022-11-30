from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
import environ
from .models import Project, Package
from .forms import PackageForm, ProjectForm

env = environ.Env()

env.read_env(".env")


# Create your views here.
def index(request):

    projects = Project.objects.order_by("name")
    context = {"projects": projects}
    return render(request, "projects.html", context)


def create(request):

    if request.method == "POST":
        success_message = None
        if "create_package" in request.POST:
            package_details = PackageForm(request.POST)
            if package_details.is_valid():
                post = package_details.save(commit=False)
                post.save()
                package_form = PackageForm(None)
                project_form = ProjectForm(None)
                success_message = "Package was successfully created"
            else:
                package_form = package_details
                project_form = ProjectForm(None)
        elif "create_project" in request.POST:
            project_details = ProjectForm(request.POST)
            if project_details.is_valid():
                post = project_details.save(commit=False)
                post.save()
                package_form = PackageForm(None)
                project_form = ProjectForm(None)
                success_message = "Project was successfully created"
            else:
                project_form = project_details
                package_form = PackageForm(None)
        return render(
            request,
            "create.html",
            {
                "package_form": package_form,
                "project_form": project_form,
                "success_message": success_message,
            },
        )
    else:
        package_form = PackageForm(None)
        project_form = ProjectForm(None)

    return render(
        request,
        "create.html",
        {
            "package_form": package_form,
            "project_form": project_form,
        },
    )
