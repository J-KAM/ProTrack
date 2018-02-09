
import datetime
from django.utils.timezone import utc

from django.shortcuts import render

from activities.models import Activity


def save_activity(user, action, resource, content=None, content_id=None):
    activity = Activity(user=user, action=action, content_object=resource,
                        date_time=datetime.datetime.utcnow().replace(tzinfo=utc),
                        content=content, content_id=content_id)
    activity.save()
