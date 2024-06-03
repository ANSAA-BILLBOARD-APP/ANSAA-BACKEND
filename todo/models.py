from django.db import models
from authentication.models import AnsaaUser


class DeviceDetail(models.Model):
    user = models.ForeignKey(AnsaaUser, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=255)
    device_id = models.CharField(max_length=255, unique=True)
    os = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.fullname} - {self.device_name}'


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(AnsaaUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


def create_default_task(sender, instance, created, **kwargs):
    """
    Create a default task for a user upon creation.
    """
    if created:
        Task.objects.create(
            title="Add a Profile Picture",
            description="Upload a profile picture to personalize your account.",
            user=instance
        )
        Task.objects.create(
            title="Approve Device",
            description="Add a device to access your account securely.",
            user=instance
        )
        Task.objects.create(
            title="Add a Media Asset",
            description="Add a your first media Media asset",
            user=instance
        )

# Connect signal to create default task
models.signals.post_save.connect(create_default_task, sender=AnsaaUser)