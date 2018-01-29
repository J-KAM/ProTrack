from django.conf.urls import url
from . import views

app_name = 'projects'

urlpatterns = [
    url(r'^new/$', views.ProjectCreate.as_view(), name="create"),
    url(r'^invite/$', views.invite_collaborators, name="invite"),
    url(r'^invitation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<pidb64>[0-9A-Za-z_\-]+)/$', views.show_invitation, name="show_invitation"),
    url(r'^invitation/manage/$', views.manage_invitation, name="manage"),
]