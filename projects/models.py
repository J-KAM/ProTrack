from django.contrib.auth.models import User
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=80, unique=True, null=False)
    owner = models.ForeignKey(User, null=True)
    members = models.ManyToManyField(User, related_name="members")

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=80)
    url = models.URLField()
    description = models.TextField(null=True, blank=True)
    created = models.DateField()
    num_of_stars = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    organization_owner = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    collaborators = models.ManyToManyField(User, related_name='collaborators')
    invited_collaborators = models.ManyToManyField(User, related_name='invited_collaborators')

    class Meta:
        unique_together = ('name', 'url')

    def __str__(self):
        return self.name

