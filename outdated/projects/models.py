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

        red = Color(env("RED"))
        yellow = Color(env("YELLOW"))
        green = Color(env("GREEN"))

        count = {"green": 0, "yellow": 0, "red": 0}
        for package in self.packages.all():
            colour = Color(package.status)

            if colour == green:
                count["green"] += 1
            elif colour == yellow:
                count["yellow"] += 1
            else:
                count["red"] += 1

        packageCount = len(self.packages.all())

        gradient = list(green.range_to(yellow, packageCount)) + list(
            yellow.range_to(red, packageCount)
        )
        if count["green"] == packageCount:
            return f"background: {gradient[0].hex_l}"

        else:
            calculatedGradient = [
                f"{env(key.upper())} {count[key]*88//packageCount}% ,"
                for key in count
                if count[key] != 0
            ]

            return f"background: linear-gradient(to bottom, {calculatedGradient});"
