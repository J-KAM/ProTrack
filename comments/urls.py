from django.conf.urls import url

from . import views

app_name = 'comments'

urlpatterns = [
    url(r'^comment/$', views.comment_create, name="comment"),
    url(r'^update/$', views.comment_update, name="update"),
    url(r'^(?P<comment_id>[0-9]+)/delete/$', views.comment_delete, name="delete"),
]