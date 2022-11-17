from datetime import date, timedelta, datetime
import math
from django.db import models
from colour import Color
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
        status = {}
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
    def background(self):

        count = {"green": 0, "yellow": 0, "red": 0}
        for package in self.packages.all():
            colour = package.status

            if colour == env("GREEN"):
                count["green"] += 1
            elif colour == env("YELLOW"):
                count["yellow"] += 1
            else:
                count["red"] += 1

        if count["red"] != 0:
            return f"background: {env('RED')}; "
        elif count["green"] != len(self.packages.all()):
            colour = env("YELLOW")
        else:
            colour = env("GREEN")

        return f"background: linear-gradient(to left, {colour},{env('PRIMARY')}); filter: hue-rotate(5deg): "
