from django.conf.urls import url

from issues import views

app_name = 'issues'

urlpatterns = [
    url(r'^all/$', views.IssuePreview.as_view(), name="preview_all"),
    url(r'^assigned/$', views.IssuePreview.as_view(), name="preview_assigned"),
    url(r'^(?P<project_id>[0-9]+)/new/$', views.IssueFormView.as_view(), name="create"),
    url(r'^(?P<id>[0-9]+)/$', views.IssueUpdate.as_view(), name="update"),
    url(r'^(?P<id>[0-9]+)/details/$', views.IssueDetails.as_view(), name="details"),
    url(r'^(?P<id>[0-9]+)/close/$', views.close_issue, name="close"),
    url(r'^(?P<id>[0-9]+)/reopen/$', views.reopen_issue, name="reopen"),
    url(r'^(?P<iid>[0-9]+)/assignee/(?P<uid>[0-9]+)/remove/$', views.remove_assignment,
        name="remove_assignment"),
]


