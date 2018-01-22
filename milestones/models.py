from django.db import models


class Milestone(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    due_date = models.DateField()
    total_progress = models.PositiveIntegerField(default=0)
    total_time_spent = models.FloatField(default=0.0)
    status = models.CharField(max_length=8,default="OPEN")
    #TODO: add relation with reposiroty

    def __str__(self):
        return self.name
