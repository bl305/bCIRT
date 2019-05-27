from django.contrib import admin
# Register your models here.
from . import models
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin


class GroupMemberInline(admin.TabularInline):
    model = models.InvAttackvector
    model = models.InvCategory
    model = models.InvPriority
    model = models.InvPhase
    model = models.InvSeverity
    model = models.InvStatus
    model = models.Inv


# admin.site.register(models.Inv)
# admin.site.register(models.InvAttackvector)
# admin.site.register(models.InvCategory)
# admin.site.register(models.InvPriority)
# admin.site.register(models.InvPhase)
# admin.site.register(models.InvSeverity)
# admin.site.register(models.InvStatus)


@admin.register(models.InvAttackvector)
class InvAttackvectorAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvCategory)
class InvCategoryAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvPriority)
class InvPriorityAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvPhase)
class InvPhaseAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvSeverity)
class InvSeverityAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.InvStatus)
class InvStatusAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.Inv)
class InvAdmin(ImportExportModelAdmin):
    pass
