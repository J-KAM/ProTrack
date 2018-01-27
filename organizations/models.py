from django.contrib.auth.models import User
from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=80, unique=True, null=False)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(User, related_name='organization_member')

    def __str__(self):
        return self.name

