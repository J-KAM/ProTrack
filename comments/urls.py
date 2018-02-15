from django.conf.urls import url
from . import views

app_name = 'comments'

urlpatterns = [
    url(r'^comment/$', views.CommentCreateView.as_view(), name="comment"),
    url(r'^update/$', views.CommentUpdateView.as_view(), name="update"),
]