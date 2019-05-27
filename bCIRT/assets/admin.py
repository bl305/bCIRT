from django.contrib import admin
from . import models
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class GroupMemberInline(admin.TabularInline):
    model = models.Profile
    model = models.Host
    model = models.Hostname
    model = models.Ipaddress

# admin.site.register(models.Profile)
# admin.site.register(models.Host)
# admin.site.register(models.Hostname)
# admin.site.register(models.Ipaddress)


@admin.register(models.Profile)
class ProfileAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.Host)
class HostAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.Hostname)
class HostnameAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.Ipaddress)
class IpaddressAdmin(ImportExportModelAdmin):
    pass
