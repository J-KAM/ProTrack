from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views
from projects import views as project_views

app_name = 'core'

urlpatterns = [
    url(r'^$', views.SignInFormView.as_view(), name="sign_in"),
    url(r'^sign_out/$', auth_views.logout, {'next_page': '/'}, name="sign_out"),
    url(r'^register/$', views.UserFormView.as_view(), name="registration"),
    # url(r'^home/$', views.home, name="home"),
    url(r'^home/$', login_required(project_views.ProjectsPreview.as_view()), name="home"),
    url(r'^home/profile/$', views.UserUpdateFormView.as_view(), name="profile"),
    url(r'^home/profile/password/$', views.change_password, name="change_password"),
    url(r'^search/$', views.search, name="search"),
]