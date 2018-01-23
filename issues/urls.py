from django.conf.urls import url

from issues import views

app_name = 'issues'

urlpatterns = [
    url(r'^$', views.IssuePreview.as_view(), name="preview"),
    url(r'^new/$', views.IssueFormView.as_view(), name="create"),
    url(r'^(?P<id>[0-9]+)/$', views.IssueUpdate.as_view(), name="update"),

]


