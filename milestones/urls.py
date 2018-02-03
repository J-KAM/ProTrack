from django.conf.urls import url
from . import views

app_name = 'milestones'

urlpatterns = [
    url(r'^$', views.MilestonesPreview.as_view(), name="preview"),
    url(r'^new/$', views.MilestoneFormView.as_view(), name="create"),
    url(r'^(?P<id>[0-9]+)/$', views.MilestoneUpdate.as_view(), name="update"),
    url(r'^(?P<id>[0-9]+)/details/$', views.MilestoneDetail.as_view(), name="detail"),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.MilestoneDelete.as_view(), name="delete"),
    url(r'^(?P<id>[0-9]+)/close/$', views.close_milestone, name="close"),
    url(r'^(?P<id>[0-9]+)/reopen/$', views.reopen_milestone, name="reopen")
]