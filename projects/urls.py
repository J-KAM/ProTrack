from django.conf.urls import url
from . import views

app_name = 'projects'

urlpatterns = [
    url(r'^new/$', views.ProjectCreate.as_view(), name="create"),
]