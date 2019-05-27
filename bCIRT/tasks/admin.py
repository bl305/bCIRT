from django.contrib import admin
# Register your models here.
from . import models
from import_export.admin import ImportExportModelAdmin

class GroupMemberInline(admin.TabularInline):
    model = models.TaskCategory
    model = models.TaskPriority
    model = models.TaskStatus
    model = models.TaskType
    model = models.TaskVarCategory
    model = models.TaskVarType
    model = models.TaskVar
    model = models.Task
    model = models.Playbook
    model = models.PlaybookTemplate
    model = models.PlaybookTemplateItem
    model = models.Action
    model = models.ScriptType
    model = models.ScriptOs
    model = models.Type
    model = models.ActionQ
    model = models.ActionQStatus
    model = models.ScriptCategory
    model = models.ScriptOutput
    model = models.OutputTarget
    model = models.Evidence
    model = models.EvidenceFormat
    model = models.EvidenceAttr
    model = models.EvidenceAttrFormat


# admin.site.register(models.Evidence)
# admin.site.register(models.EvidenceFormat)
# admin.site.register(models.EvidenceAttr)
# admin.site.register(models.EvidenceAttrFormat)
#
# admin.site.register(models.Action)
# admin.site.register(models.ScriptType)
# admin.site.register(models.ScriptOs)
# admin.site.register(models.ScriptCategory)
# admin.site.register(models.ScriptOutput)
# admin.site.register(models.OutputTarget)
# admin.site.register(models.Type)
# admin.site.register(models.ActionQ)
# admin.site.register(models.ActionQStatus)
#
# admin.site.register(models.Task)
# admin.site.register(models.TaskCategory)
# admin.site.register(models.TaskPriority)
# admin.site.register(models.TaskStatus)
# admin.site.register(models.TaskType)
# admin.site.register(models.TaskTemplate)
# admin.site.register(models.TaskVar)
# admin.site.register(models.TaskVarCategory)
# admin.site.register(models.TaskVarType)
# admin.site.register(models.Playbook)
# admin.site.register(models.PlaybookTemplate)
# admin.site.register(models.PlaybookTemplateItem)


@admin.register(models.Evidence)
class EvidenceAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.EvidenceFormat)
class EvidenceFormatAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.EvidenceAttr)
class EvidenceAttrAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.EvidenceAttrFormat)
class EvidenceAttrFormatAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.Action)
class ActionAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.ScriptType)
class ScriptTypeAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.ScriptOs)
class ScriptOsAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.ScriptCategory)
class ScriptCategoryAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.ScriptOutput)
class ScriptOutputAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.OutputTarget)
class OutputTargetAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.Type)
class TypeAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.ActionQ)
class ActionQAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.ActionQStatus)
class ActionQStatusAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.Task)
class TaskAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.TaskCategory)
class TaskCategoryAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.TaskPriority)
class TaskPriorityAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.TaskStatus)
class TaskStatusAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.TaskType)
class TaskTypeAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.TaskTemplate)
class TaskTemplateAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.TaskVar)
class TaskVarAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.TaskVarCategory)
class TaskVarCategoryAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.TaskVarType)
class TaskVarTypeAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.Playbook)
class PlaybookAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.PlaybookTemplate)
class PlaybookTemplateAdmin(ImportExportModelAdmin):
    pass


@admin.register(models.PlaybookTemplateItem)
class PlaybookTemplateItemAdmin(ImportExportModelAdmin):
    pass
