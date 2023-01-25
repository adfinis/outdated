from datetime import date, timedelta
from django.db import models

# Create your models here.


class Dependency(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class DependencyVersion(models.Model):

    dependency = models.ForeignKey(Dependency, on_delete=models.CASCADE)
    version = models.CharField(max_length=100)
    release_date = models.DateField()
    end_of_life_date = models.DateField()

    class Meta:
        ordering = ["end_of_life_date"]
        unique_together = ("dependency", "version")

    def __str__(self):
        return self.dependency.name + " " + self.version

    @property
    def status(self):
        if date.today() >= self.end_of_life_date:
            return "OUTDATED"
        elif date.today() + timedelta(days=30) >= self.end_of_life_date:
            return "WARNING"
        return "UP-TO-DATE"


class Project(models.Model):

    name = models.CharField(max_length=100, unique=True)
    repo = models.URLField(max_length=200, unique=True)
    dependency_versions = models.ManyToManyField(DependencyVersion, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def status(self) -> str:
        return self.dependency_versions.first().status
