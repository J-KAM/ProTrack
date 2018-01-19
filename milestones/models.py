from django.db import models


class Milestone(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(null=True)
    start_date = models.DateField()
    due_date = models.DateField()
    total_progress = models.PositiveIntegerField()
    total_time_spent = models.FloatField()
    #TODO: add relation with reposiroty


    def __str__(self):
        return self.name
