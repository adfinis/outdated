# Generated by Django 3.2.18 on 2023-04-05 09:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'ordering': ['name', 'id'],
            },
        ),
        migrations.CreateModel(
            name='DependencyVersion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('version', models.CharField(max_length=100)),
                ('release_date', models.DateField()),
                ('end_of_life_date', models.DateField(blank=True, null=True)),
                ('dependency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outdated.dependency')),
            ],
            options={
                'ordering': ['end_of_life_date', 'dependency__name', 'version', 'release_date'],
                'unique_together': {('dependency', 'version')},
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('repo', models.URLField(max_length=100, unique=True)),
                ('dependency_versions', models.ManyToManyField(blank=True, to='outdated.DependencyVersion')),
            ],
            options={
                'ordering': ['name', 'id'],
            },
        ),
    ]
