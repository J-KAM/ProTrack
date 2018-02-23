from django.contrib.auth.models import User
from django.db import models

from organizations.models import Organization


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
    git_owner = models.CharField(max_length=255, null=True, blank=True)
    git_name = models.CharField(max_length=255, null=True, blank=True)
    stargazers = models.ManyToManyField(User, related_name='stargazers')


    class Meta:
        unique_together = ('name', 'url')

    def __str__(self):
        return self.name

    @property
    def is_git(self):
        if self.git_owner is not None and self.git_owner != '':
            return True
        return False

