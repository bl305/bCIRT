from import_export import resources
from .models import InvAttackvector, \
    InvCategory,\
    InvPriority,\
    InvPhase,\
    InvSeverity,\
    InvStatus,\
    Inv


class InvAttackvectorResource(resources.ModelResource):
    class Meta:
        model = InvAttackvector


class InvCategoryResource(resources.ModelResource):
    class Meta:
        model = InvCategory


class InvPriorityResource(resources.ModelResource):
    class Meta:
        model = InvPriority


class InvPhaseResource(resources.ModelResource):
    class Meta:
        model = InvPhase


class InvSeverityResource(resources.ModelResource):
    class Meta:
        model = InvSeverity


class InvStatusResource(resources.ModelResource):
    class Meta:
        model = InvStatus


class InvResource(resources.ModelResource):
    class Meta:
        model = Inv
