import json
import re

from django.apps import apps
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.views import View

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


class CreateFormView(View):
    template_name = "create.html"

    def get_forms(self, parameter, instance=None):
        return {
            "package_form": PackageForm(parameter, instance=instance),
            "project_form": ProjectForm(parameter, instance=instance),
            "version_form": VersionForm(parameter, instance=instance),
        }

    def get_model_data(self, search=""):
        data_dict = {
            "projects": Project.objects.all(),
            "packages": Package.objects.all(),
            "versions": Version.objects.all(),
        }

        if search:
            data_dict["packages"] = Package.objects.filter(name__icontains=search)

        return data_dict

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                **self.get_forms(None),
                **self.get_model_data(request.GET.get("search")),
            },
        )

    def post(self, request, *args, **kwargs):

        post = self.request.POST
        if "create" in post:
            target = post["create"]
            chosen_form = self.get_forms(post)[target + "_form"]
            if chosen_form.is_valid():
                chosen_form.save()
                return HttpResponseRedirect(self.request.path_info)
            else:
                return render(
                    request,
                    self.template_name,
                    {
                        **self.get_model_data(),
                        **self.get_forms(None),
                        **{target + "_form": chosen_form},
                    },
                )
        elif "edit" in post:
            target, pk = re.findall(r"([A-Za-z]+)-(\d+)", post["edit"])[0]

            chosen_form = self.get_forms(
                post, apps.get_model("projects." + target).objects.filter(pk=pk)[0]
            )[target + "_form"]
            if chosen_form.is_valid():
                chosen_form.save()
            return HttpResponseRedirect(self.request.path_info)
        elif "delete" in post:
            target, pk = re.findall(r"([A-Za-z]+)-(\d+)", post["delete"])[0]
            apps.get_model("projects." + target).objects.filter(pk=pk).delete()
            return HttpResponseRedirect(self.request.path_info)
