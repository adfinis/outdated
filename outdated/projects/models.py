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
        packageValues = 0.0
        count = {"green": 0, "yellow": 0, "red": 0}
        for package in self.packages.all():
            colour = package.status
            if colour == env("GREEN"):
                count["green"] += 1
                packageValues += 1
            elif colour == env("YELLOW"):
                count["yellow"] += 1
                packageValues += 0.5
            else:
                count["red"] += 1
        packageNum = len(self.packages.all())
        completion = packageValues * 100 // packageNum

        if count["red"] != 0:
            return {
                "style": f"background: linear-gradient(to left,#f37169, {env('PRIMARY')});filter: hue-rotate(5deg); filter: brightness(1)",
                "color": "red",
                "completion": completion,
            }
        elif count["green"] != packageNum:
            hex = env("YELLOW")
            color = "yellow"
        else:
            hex = env("GREEN")
            color = "green"

        return {
            "style": f"background: linear-gradient(to left, {hex},{env('PRIMARY')}); filter: hue-rotate(5deg);",
            "color": color,
            "completion": completion,
        }
