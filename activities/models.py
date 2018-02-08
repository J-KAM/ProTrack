from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

ACTION_CHOICES = (
    ('opened', 'opened'),
    ('closed', 'closed'),
    ('reopened', 'reopened'),
    ('created', 'created'),
    ('updated', 'updated'),
    ('assigned', 'assigned'),
    ('added to project', 'added to project'),
    ('set milestone', 'set milestone'),
    ('removed milestone', 'removed milestone'),
    ('commented', 'commented'),
)


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=17, null=False, choices=ACTION_CHOICES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    date_time = models.DateTimeField()

    def __str__(self):
        return self.user.username + "-" + self.action
