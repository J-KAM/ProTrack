from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=80, unique=True)
    url = models.URLField(unique=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateField()
    num_of_stars = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    collaborators = models.ManyToManyField(User, related_name='project_collaborator')

    def __str__(self):
        return self.name + self.url
