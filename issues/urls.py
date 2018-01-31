from django.conf.urls import url

from issues import views

app_name = 'issues'

urlpatterns = [
    url(r'^$', views.IssuePreview.as_view(), name="preview"),
    url(r'^(?P<project_id>[0-9]+)/new/$', views.IssueFormView.as_view(), name="create"),
    url(r'^(?P<id>[0-9]+)/$', views.IssueUpdate.as_view(), name="update"),
    url(r'^(?P<id>[0-9]+)/close/$', views.close_issue, name="close"),
    url(r'^(?P<id>[0-9]+)/reopen/$', views.reopen_issue, name="reopen")
]


