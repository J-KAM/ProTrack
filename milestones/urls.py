from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'milestones'

urlpatterns = [
    url(r'^$', views.preview.as_view(), name="preview"),
    url(r'^new/$', views.MilestoneFormView.as_view(), name="create"),
]