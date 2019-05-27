from import_export import resources
from .models import Task, TaskCategory, TaskPriority, TaskStatus, TaskType,\
    TaskTemplate, TaskVar, TaskVarCategory, TaskVarType, \
    Playbook, PlaybookTemplate, PlaybookTemplateItem,\
    Evidence, EvidenceFormat, EvidenceAttr, EvidenceAttrFormat, \
    Action, ScriptType, ScriptOs, ScriptCategory, ScriptOutput, OutputTarget, Type, \
    ActionQ, ActionQStatus


class EvidenceResource(resources.ModelResource):
    class Meta:
        model = Evidence


class EvidenceFormatResource(resources.ModelResource):
    class Meta:
        model = EvidenceFormat


class EvidenceAttrResource(resources.ModelResource):
    class Meta:
        model = EvidenceAttr


class EvidenceAttrFormatResource(resources.ModelResource):
    class Meta:
        model = EvidenceAttrFormat


class ActionResource(resources.ModelResource):
    class Meta:
        model = Action


class ScriptTypeResource(resources.ModelResource):
    class Meta:
        model = ScriptType


class ScriptOsResource(resources.ModelResource):
    class Meta:
        model = ScriptOs


class ScriptCategoryResource(resources.ModelResource):
    class Meta:
        model = ScriptCategory


class ScriptOutputResource(resources.ModelResource):
    class Meta:
        model = ScriptOutput


class OutputTargetResource(resources.ModelResource):
    class Meta:
        model = OutputTarget


class TypeResource(resources.ModelResource):
    class Meta:
        model = Type


class ActionQResource(resources.ModelResource):
    class Meta:
        model = ActionQ


class ActionQStatusResource(resources.ModelResource):
    class Meta:
        model = ActionQStatus


class TaskResource(resources.ModelResource):
    class Meta:
        model = Task


class TaskCategoryResource(resources.ModelResource):
    class Meta:
        model = TaskCategory


class TaskPriorityResource(resources.ModelResource):
    class Meta:
        model = TaskPriority


class TaskStatusResource(resources.ModelResource):
    class Meta:
        model = TaskStatus


class TaskTypeResource(resources.ModelResource):
    class Meta:
        model = TaskType


class TaskTemplateResource(resources.ModelResource):
    class Meta:
        model = TaskTemplate


class TaskVarResource(resources.ModelResource):
    class Meta:
        model = TaskVar


class TaskVarCategoryResource(resources.ModelResource):
    class Meta:
        model = TaskVarCategory


class TaskVarTypeResource(resources.ModelResource):
    class Meta:
        model = TaskVarType


class PlaybookResource(resources.ModelResource):
    class Meta:
        model = Playbook


class PlaybookTemplateResource(resources.ModelResource):
    class Meta:
        model = PlaybookTemplate


class PlaybookTemplateItemResource(resources.ModelResource):
    class Meta:
        model = PlaybookTemplateItem
