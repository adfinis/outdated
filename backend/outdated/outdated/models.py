from datetime import date, timedelta

from django.db import models

from outdated.models import UUIDModel


class Dependency(UUIDModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name", "id"]

    def __str__(self):
        return self.name


class DependencyVersion(UUIDModel):

    dependency = models.ForeignKey(Dependency, on_delete=models.CASCADE)
    version = models.CharField(max_length=100)
    release_date = models.DateField()
    eol_date = models.DateField()

    class Meta:
        ordering = ["eol_date", "dependency__name", "version", "release_date"]
        unique_together = ("dependency", "version")

    @property
    def status(self):
        if date.today() >= self.eol_date:
            return "OUTDATED"  # als konstante definieren
        elif date.today() + timedelta(days=30) >= self.eol_date:
            return "WARNING"
        return "UP-TO-DATE"

    def __str__(self):
        return self.dependency.name + self.version


class Project(UUIDModel):

    name = models.CharField(max_length=100, unique=True)
    repo = models.URLField(max_length=200, unique=True)
    dependency_versions = models.ManyToManyField(DependencyVersion, blank=True)

    class Meta:
        ordering = ["name", "id"]

    @property
    def status(self) -> str:
        first = self.dependency_versions.first()
        return first.status if first else "UNDEFINED"

    def __str__(self):
        return self.name
