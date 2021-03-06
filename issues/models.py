from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

# Create your models here.

from activities.models import Activity
from comments.models import Comment
from milestones.models import Milestone
from projects.models import Project

WEIGHT_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)

PROGRESS_CHOICES = (
    ('0%', '0%'),
    ('10%', '10%'),
    ('20%', '20%'),
    ('30%', '30%'),
    ('40%', '40%'),
    ('50%', '50%'),
    ('60%', '60%'),
    ('70%', '70%'),
    ('80%', '80%'),
    ('90%', '90%'),
    ('100%', '100%'),
)

TYPE_CHOICES = (
    ('Feature', 'Feature'),
    ('Bug', 'Bug'),
    ('Documentation', 'Documentation'),
    ('Support', 'Support'),
    ('Model', 'Model')
)

STATUS_CHOICES = (
    ('Open', 'Open'),
    ('In progress', 'In progress'),
    ('Done', 'Done'),
    ('Closed', 'Closed'),
)

PRIORITY_CHOICES = (
    ('Normal', 'Normal'),
    ('Low', 'Low'),
    ('High', 'High'),
    ('Urgent', 'Urgent'),
)


class Issue(models.Model):
    title = models.CharField(max_length=80, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True, choices=WEIGHT_CHOICES)
    progress = models.CharField(max_length=4, null=True, blank=True, choices=PROGRESS_CHOICES)
    time_spent = models.FloatField(null=False, blank=True, default=0.0)
    type = models.CharField(max_length=30, null=True, blank=True, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=10, null=True, blank=True, choices=PRIORITY_CHOICES)

    total_time_spent = models.FloatField(null=False, default=0.0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
    milestone = models.ForeignKey(Milestone, on_delete=models.SET_NULL, null=True)
    assignees = models.ManyToManyField(User, related_name='assignees')

    comments = GenericRelation(Comment, related_query_name='issues', content_type_field='content_type', object_id_field='object_id')
    activities = GenericRelation(Activity, related_query_name='issues', content_type_field='content_type',
                                 object_id_field='object_id')

    def __str__(self):
        return self.title

    def progress_in_numbers(self):
        return self.progress.split('%')[0]
