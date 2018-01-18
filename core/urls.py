from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    url(r'^$', views.SignInFormView.as_view(), name="sign_in"),
    url(r'^sign_out/$', auth_views.logout, {'next_page': '/'}, name="sign_out"),
    url(r'^register/$', views.UserFormView.as_view(), name="registration"),
    url(r'^home/$', views.home, name="home")
]