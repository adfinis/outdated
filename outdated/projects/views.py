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
    packages = Package.objects.order_by("name")
    context = {"projects": projects, "packages": packages}
    return render(request, "projects.html", context)


def create(request):
    projects = Project.objects.order_by("name")
    packages = Package.objects.order_by("name")
    context = {"projects": projects, "packages": packages}

    package_form = PackageForm(request.POST or None)
    if package_form.is_valid():
        package_form.save()
    context["package_form"] = package_form
    project_form = ProjectForm(request.POST or None)
    if project_form.is_valid():
        project_form.save()
    context["project_form"] = project_form
    context["primary"] = env("PRIMARY")
    context["green"] = env("GREEN")
    context["yellow"] = env("YELLOW")
    context["red"] = env("RED")
    return render(request, "create.html", context)
