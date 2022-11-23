from datetime import date, timedelta

from django.db import models

import environ

env = environ.Env()

env.read_env(".env")


class Package(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    end_of_life_date = models.DateField()

    def __str__(self):
        return self.name

    @property
    def status(self):
        if date.today() >= self.end_of_life_date:
            colour = env("RED")
        elif date.today() + timedelta(days=30) >= self.end_of_life_date:
            colour = env("YELLOW")
        else:
            colour = env("GREEN")
        return colour


class Project(models.Model):
    name = models.CharField(max_length=100)
    repo = models.CharField(max_length=200)
    packages = models.ManyToManyField(Package)

    def __str__(self):
        return self.name

    @property
    def status(self):
        value_packages = 0.0
        colours_packages = {"green": 0, "yellow": 0, "red": 0}
        for package in self.packages.all():
            colour = package.status
            if colour == env("GREEN"):
                colours_packages["green"] += 1
                value_packages += 1
            elif colour == env("YELLOW"):
                colours_packages["yellow"] += 1
                value_packages += 0.5
            else:
                colours_packages["red"] += 1
        if colours_packages["red"] != 0:
            colour = "RED"
        elif len(self.packages.all()) != colours_packages["green"]:
            colour = "YELLOW"
        else:
            colour = "GREEN"
        return {
            "up_to_dateness": value_packages * 100 // len(self.packages.all()),
            "background": env(colour + "_GRADIENT"),
            "colour": colour,
        }
