from datetime import date, timedelta

from django.db import models


class Package(models.Model):

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """Return Package name."""
        return self.name


class Version(models.Model):

    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    end_of_life_date = models.DateField()

    class Meta:
        """Define ordering and unique together."""

        ordering = ["end_of_life_date"]
        unique_together = ("package", "name")

    def __str__(self):

        return self.name

    @property
    def status(self):
        """Return the current status of given version."""
        if date.today() >= self.end_of_life_date:

            colour = "red"
        elif date.today() + timedelta(days=30) >= self.end_of_life_date:

            colour = "yellow"
        else:

            colour = "green"
        return {"CSSClass": f"od-background-{colour}", "colour": colour}


class Project(models.Model):

    name = models.CharField(max_length=100, unique=True)
    repo = models.URLField(max_length=200, unique=True)
    used_packages = models.ManyToManyField(Version, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):

        return self.name

    @property
    def status(self):
        """Return the current status of given project."""
        packages = self.used_packages.all()
        if packages:

            value_packages = 0.0
            colours_packages = {"green": 0, "yellow": 0, "red": 0}
            for package in packages:
                package_class = package.status["colour"]
                if package_class == "green":
                    colours_packages["green"] += 1
                    value_packages += 1
                elif package_class == "yellow":
                    colours_packages["yellow"] += 1
                    value_packages += 0.5
                else:
                    colours_packages["red"] += 1
            if colours_packages["red"] != 0:
                colour = "red"
            elif len(packages) != colours_packages["green"]:
                colour = "yellow"
            else:
                colour = "green"
            return {
                "up_to_dateness": value_packages * 100 // len(packages),
                "colour": colour,
            }
        else:
            return {"up_to_dateness": 100, "colour": "grey"}
