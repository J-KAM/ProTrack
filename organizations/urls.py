from django.conf.urls import url

from organizations import views

app_name = 'organizations'

urlpatterns = [
    url(r'^new/$', views.OrganizationFormView.as_view(), name="create"),
]