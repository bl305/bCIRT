from import_export import resources
from django.contrib.auth.models import User, Group


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class GroupResource(resources.ModelResource):
    class Meta:
        model = Group
