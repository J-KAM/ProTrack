from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'projects'

urlpatterns = [
    url(r'^$', views.ProjectsPreview.as_view(), name="preview"),
    url(r'^new/$', views.ProjectCreate.as_view(), name="create"),
    url(r'^(?P<id>[0-9]+)/$', views.ProjectUpdate.as_view(), name="update"),
    url(r'^(?P<pk>[0-9]+)/details/$', views.ProjectDetail.as_view(), name="detail"),
    url(r'^(?P<pk>[0-9]+)/delete/$', login_required(views.ProjectDelete.as_view()), name="delete"),
    url(r'^(?P<id>[0-9]+)/add_collaborators/$', views.add_collaborators, name="add_collaborators"),
    url(r'^(?P<pid>[0-9]+)/collaborator/(?P<uid>[0-9]+)/remove/$', views.remove_collaborator, name="remove_collaborator"),
    url(r'^invite/$', views.invite_collaborators, name="invite"),
    url(r'^invitation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<pidb64>[0-9A-Za-z_\-]+)/$', views.show_invitation, name="show_invitation"),
    url(r'^invitation/manage/$', views.manage_invitation, name="manage"),

]