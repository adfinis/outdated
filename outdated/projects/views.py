from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from .models import Project, Package

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
    return render(request, "create.html", context)
