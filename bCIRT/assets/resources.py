from import_export import resources
from .models import Profile, Host, Hostname, Ipaddress


class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile


class HostResource(resources.ModelResource):
    class Meta:
        model = Host


class HostNameResource(resources.ModelResource):
    class Meta:
        model = Hostname


class IpAddressResource(resources.ModelResource):
    class Meta:
        model = Ipaddress
