from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'milestones'

urlpatterns = [
    url(r'^$', login_required(views.MilestonesPreview.as_view()), name="preview"),
    url(r'^new/$', views.MilestoneCreateView.as_view(), name="create"),
    url(r'^(?P<project_id>[0-9]+)/new/$', views.MilestoneCreateFromProjectView.as_view(), name="create_from_project"),
    url(r'^(?P<id>[0-9]+)/$', views.MilestoneUpdate.as_view(), name="update"),
    url(r'^(?P<id>[0-9]+)/details/$', login_required(views.MilestoneDetail.as_view()), name="detail"),
    url(r'^(?P<pk>[0-9]+)/delete/$', login_required(views.MilestoneDelete.as_view()), name="delete"),
    url(r'^(?P<id>[0-9]+)/close/$', views.close_milestone, name="close"),
    url(r'^(?P<id>[0-9]+)/reopen/$', views.reopen_milestone, name="reopen")
]