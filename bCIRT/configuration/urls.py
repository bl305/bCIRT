from django.conf.urls import url
from . import views
# from django.contrib.auth import views as auth_views

app_name = 'configuration'

urlpatterns = [
    url(r"^$", views.ConfigurationPage.as_view(), name='conf_base'),
    url(r"^update/list$", views.UpdatePackageListView.as_view(), name='conf_updatelist'),
    url(r"^update/create$", views.UpdatePackageCreateView.as_view(), name='conf_updatecreate'),
    url(r"^update/detail/(?P<pk>\d+)/$", views.UpdatePackageDetailView.as_view(), name="conf_updatedetail"),
    url(r'^update/edit/(?P<pk>\d+)/$', views.UpdatePackageUpdateView.as_view(), name='conf_updateedit'),
    url(r'^update/remove/(?P<pk>\d+)/$', views.UpdatePackageRemoveView.as_view(), name='conf_updateremove'),

    url(r"logging$", views.ConfigurationLoggingPage.as_view(), name='conf_logging'),
]
