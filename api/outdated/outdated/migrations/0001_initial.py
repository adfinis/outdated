# Generated by Django 4.2.6 on 2023-10-24 14:19

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text
import outdated.models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("user", "0001_initial"),
    ]

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
                "unique_together": {("name", "provider")},
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
                "unique_together": {("dependency", "major_version", "minor_version")},
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
                "unique_together": {("release_version", "patch_version")},
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
                ("repo", outdated.models.RepositoryURLField(max_length=100)),
                (
                    "versioned_dependencies",
                    models.ManyToManyField(blank=True, to="outdated.version"),
                ),
            ],
            options={
                "ordering": ["name", "id"],
            },
        ),
        migrations.CreateModel(
            name="Maintainer",
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
                ("is_primary", outdated.models.UniqueBooleanField(default=False)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="maintainers",
                        to="outdated.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="user.user"
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="project",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("name"),
                name="unique_project_name",
            ),
        ),
        migrations.AddConstraint(
            model_name="project",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("repo"),
                name="unique_project_repo",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="maintainer",
            unique_together={("user", "project")},
        ),
    ]
