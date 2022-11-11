from datetime import date
from dateutil.relativedelta import relativedelta
from django.db import models


class Package(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    end_of_life_date = models.DateField()

    def __str__(self):
        return self.name

    @property
    def status(self):
        if date.today() >= self.end_of_life_date:
            return "danger"
        elif date.today() - relativedelta(months=1) >= self.end_of_life_date:
            return "warning"
        else:
            return "success"


class Project(models.Model):
    name = models.CharField(max_length=100)
    repo = models.CharField(max_length=200)
    packages = models.ManyToManyField(Package)

    def __str__(self):
        return self.name
