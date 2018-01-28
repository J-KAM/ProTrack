from django.conf.urls import url
from . import views

app_name = 'projects'

urlpatterns = [
    url(r'^new/$', views.ProjectCreate.as_view(), name="create"),
    url(r'^collaborators/invite/$', views.invite_collaborators, name="invite"),
    url(r'^accept/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<pidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.accept_invitation, name="accept"),
]