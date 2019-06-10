from django.conf.urls import url
from . import views
# from django.contrib.auth import views as auth_views

app_name = 'reports'

urlpatterns = [
    url(r"^$", views.ReportsPage.as_view(), name='rep_base'),

    url(r"dashboard$", views.ReportsDashboardPage.as_view(), name='rep_dashboard'),
]
