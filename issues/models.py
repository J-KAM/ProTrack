from django.db import models

# Create your models here.


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

    def __str__(self):
        return self.title

    def progress_in_numbers(self):
        return self.progress.split('%')[0]
