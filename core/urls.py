from django.conf.urls import url
from . import views

app_name = 'core'

urlpatterns = [
    url(r'^$', views.SignInFormView.as_view(), name="sign_in"),
    url(r'^register/$', views.UserFormView.as_view(), name="registration"),
]