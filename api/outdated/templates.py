from django.template.backends.jinja2 import Jinja2 as Jinja2Backend


class Jinja2(Jinja2Backend):
    app_dirname = "templates"
