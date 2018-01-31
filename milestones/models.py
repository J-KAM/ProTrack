from django.db import models
from datetime import date

from projects.models import Project

STATUS_CHOICES = (
    ('OPEN', 'Open'),
    ('CLOSED', 'Closed'),
)


class Milestone(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    due_date = models.DateField()
    total_progress = models.PositiveIntegerField(default=0)
    total_time_spent = models.FloatField(default=0.0)
    status = models.CharField(max_length=6,choices=STATUS_CHOICES,default="OPEN")
    #TODO: Change this if possible
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

    @property
    def is_past_due(self):
        if self.status != 'OPEN':
            return False
        return date.today() > self.due_date
