from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from organizations import views

app_name = 'organizations'

urlpatterns = [
    url(r'^$', views.OrganizationPreview.as_view(), name="preview"),
    url(r'^new/$', views.OrganizationFormView.as_view(), name="create"),
    url(r'^(?P<id>[0-9]+)/$', views.OrganizationUpdate.as_view(), name="update"),
    url(r'^(?P<id>[0-9]+)/details/$', views.OrganizationDetails.as_view(), name="details"),
    url(r'^(?P<pk>[0-9]+)/delete/$', login_required(views.OrganizationDelete.as_view()), name="delete"),
    url(r'^(?P<id_org>[0-9]+)/member/(?P<id_mem>[0-9]+)/remove/$', views.remove_member_from_organization,
        name="remove_from_org"),
    url(r'^(?P<id>[0-9]+)/add_members/$', views.add_members, name="add_members"),
    url(r'^invite/$', views.invite_members, name="invite"),
    url(r'^invitation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<oidb64>[0-9A-Za-z_\-]+)/$', views.show_invitation,
        name="show_invitation"),
    url(r'^invitation/manage/$', views.manage_invitation, name="manage"),

]