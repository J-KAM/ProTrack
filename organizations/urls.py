from django.conf.urls import url

from organizations import views

app_name = 'organizations'

urlpatterns = [
    url(r'^$', views.OrganizationPreview.as_view(), name="preview"),
    url(r'^new/$', views.OrganizationFormView.as_view(), name="create"),
    url(r'^(?P<id>[0-9]+)/$', views.OrganizationUpdate.as_view(), name="update"),
    url(r'^(?P<id>[0-9]+)/details/$', views.OrganizationDetails.as_view(), name="details"),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.OrganizationDelete.as_view(), name="delete"),
    url(r'^(?P<id_org>[0-9]+)/member/(?P<id_mem>[0-9]+)/remove/$', views.remove_member_from_organization,
        name="remove_from_org"),

]