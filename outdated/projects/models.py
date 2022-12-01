from datetime import date, timedelta

from django.db import models

import environ

env = environ.Env()

env.read_env(".env")


class Package(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Version(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    release_date = models.DateField()
    end_of_life_date = models.DateField()

    def __str__(self):
        return self.name

    @property
    def CSSClass(self):
        if date.today() >= self.end_of_life_date:
            css_class = "od-background-red"
        elif date.today() + timedelta(days=30) >= self.end_of_life_date:
            css_class = "od-background-yellow"
        else:
            css_class = "od-background-green"
        return css_class


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    repo = models.URLField(max_length=200, unique=True)
    used_packages = models.ManyToManyField(Version, blank=False)

    def __str__(self):
        return self.name

    @property
    def status(self):
        print(self.used_packages.all())
        value_packages = 0.0
        colours_packages = {"green": 0, "yellow": 0, "red": 0}
        for package in self.used_packages.all():
            package_class = package.CSSClass
            if package_class == "od-background-green":
                colours_packages["green"] += 1
                value_packages += 1
            elif package_class == "od-background-yellow":
                colours_packages["yellow"] += 1
                value_packages += 0.5
            else:
                colours_packages["red"] += 1
        if colours_packages["red"] != 0:
            colour = "red"
        elif len(self.used_packages.all()) != colours_packages["green"]:
            colour = "yellow"
        else:
            colour = "green"
        return {
            "up_to_dateness": value_packages * 100 // len(self.used_packages.all()),
            "colour": colour,
        }
