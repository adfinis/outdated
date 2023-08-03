from django.conf import settings
from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from outdated.models import UUIDModel
from outdated.outdated.models import Project, ReleaseVersion

TEMPLATE_CHOICES = [(template, template) for template, _ in settings.NOTIFICATIONS]


class Notification(UUIDModel):
    schedule = models.DurationField()
    template = models.CharField(max_length=50, choices=TEMPLATE_CHOICES)

    def __str__(self) -> str:
        return f"{self.template} ({self.schedule.days} days before EOL)"

    class Meta:
        unique_together = ("schedule", "template")
        ordering = ("-schedule",)


def build_notification_queue(project: Project):
    duration_until_outdated = project.duration_until_outdated
    notifications = project.notification_queue
    unsent_notifications = Notification.objects.filter(
        schedule__gte=duration_until_outdated
    )
    notifications.set(
        [
            *list(unsent_notifications)[-1:],
            *Notification.objects.filter(schedule__lte=duration_until_outdated),
        ]
    )
    project.save()


@receiver(post_save, sender=ReleaseVersion)
def release_version_changed(instance: ReleaseVersion, **kwargs):
    if not instance.end_of_life:
        return
    concerned_projects = []
    for version in instance.versions.all():
        concerned_projects.extend(version.projects.all())

    for project in set(concerned_projects):
        if project.duration_until_outdated is not None:
            build_notification_queue(project)


@receiver(m2m_changed, sender=Project.versioned_dependencies.through)
def versioned_dependencies_changed(action: str, instance: Project, **kwargs):
    if (
        action.startswith("pre")
        or action.endswith("clear")
        or instance.duration_until_outdated is None
    ):
        return
    build_notification_queue(instance)
