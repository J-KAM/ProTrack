from django.conf.urls import url

from organizations import views

app_name = 'organizations'

urlpatterns = [
    url(r'^$', views.OrganizationPreview.as_view(), name="preview"),
    url(r'^new/$', views.OrganizationFormView.as_view(), name="create"),
    url(r'^(?P<id>[0-9]+)/details/$', views.OrganizationDetails.as_view(), name="details"),

]