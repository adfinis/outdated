# Generated by Django 4.1.8 on 2023-04-27 09:19

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text
import outdated.outdated.models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Dependency",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "provider",
                    models.CharField(
                        choices=[("PIP", "PIP"), ("NPM", "NPM")], max_length=10
                    ),
                ),
            ],
            options={
                "ordering": ["name", "id"],
            },
        ),
        migrations.CreateModel(
            name="ReleaseVersion",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("major_version", models.IntegerField()),
                ("minor_version", models.IntegerField()),
                (
                    "_latest_patch_version",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "last_checked",
                    models.DateTimeField(
                        blank=True,
                        default=outdated.outdated.models.get_yesterday,
                        editable=False,
                        null=True,
                    ),
                ),
                ("end_of_life", models.DateField(blank=True, null=True)),
                (
                    "dependency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="outdated.dependency",
                    ),
                ),
            ],
            options={
                "ordering": [
                    "end_of_life",
                    "dependency__name",
                    "major_version",
                    "minor_version",
                ],
            },
        ),
        migrations.CreateModel(
            name="Version",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("patch_version", models.IntegerField()),
                ("release_date", models.DateField(blank=True, null=True)),
                (
                    "release_version",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="outdated.releaseversion",
                    ),
                ),
            ],
            options={
                "ordering": [
                    "release_version__end_of_life",
                    "release_version__dependency__name",
                    "release_version__major_version",
                    "release_version__minor_version",
                    "patch_version",
                ],
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=100)),
                ("repo", models.URLField(max_length=100, unique=True)),
                (
                    "versioned_dependencies",
                    models.ManyToManyField(blank=True, to="outdated.version"),
                ),
            ],
            options={
                "ordering": ["name", "id"],
            },
        ),
        migrations.AddIndex(
            model_name="dependency",
            index=models.Index(fields=["name", "provider"], name="name_provider_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="dependency",
            unique_together={("name", "provider")},
        ),
        migrations.AddIndex(
            model_name="releaseversion",
            index=models.Index(
                fields=["dependency", "major_version", "minor_version"],
                name="dependency_version_idx",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="releaseversion",
            unique_together={("dependency", "major_version", "minor_version")},
        ),
        migrations.AddConstraint(
            model_name="project",
            constraint=models.UniqueConstraint(
                condition=models.Q(
                    ("name__iexact", django.db.models.functions.text.Lower("name"))
                ),
                fields=("name",),
                name="unique_project_name",
            ),
        ),
    ]
