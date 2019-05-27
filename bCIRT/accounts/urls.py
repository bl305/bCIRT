from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r"login/$", auth_views.LoginView.as_view(template_name="accounts/account_login.html"), name='login'),
    url(r"password_reset/$", auth_views.PasswordResetView.as_view(template_name="accounts/account_pw_reset.html"), name='password_reset'),
    url(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r"register/$", views.RegisterAccountPage.as_view(), name="register"),
]
