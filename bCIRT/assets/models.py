from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from invs.models import Inv
# HTML renderer
import misaka
# Get the user so we can use this
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.
class Host(models.Model):
    objects = models.Manager()
    name = models.CharField(blank=False, null=False, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=True, default='', blank=True)
    # ip = models.GenericIPAddressField(blank=True, null=True, default='')

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(Host, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "assets:host_detail",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        # if self.ip == '' and self.name == '':
        #     raise ValidationError(_('You must enter an IP address or a Hostname.'))
        pass

    class Meta:
        ordering = ["id"]


# To store related hostnames
class Hostname(models.Model):
    objects = models.Manager()
    name = models.CharField(blank=True, default='', max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=True, default='', blank=True)
    hosts = models.ForeignKey(Host, blank=True, related_name="hostname_hosts", default=None, on_delete=models.SET_NULL,
                              null=True)

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(Hostname, self).save(*args, **kwargs)


# To store related ips
class Ipaddress(models.Model):
    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    ip = models.GenericIPAddressField(blank=True, null=True, default='')
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=True, default='', blank=True)
    hosts = models.ForeignKey(Host, blank=True, related_name="ipaddress_hosts", default=None,
                              on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.ip)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(Ipaddress, self).save(*args, **kwargs)


# Create your models here.
class Profile(models.Model):
    objects = models.Manager()
    username = models.CharField(blank=True, null=True, default='', max_length=50)
    userid = models.CharField(blank=True, null=True, default='', max_length=30)
    email = models.EmailField(blank=True, null=True, max_length=50)
    host = models.CharField(blank=True, null=True, default='', max_length=30)
    ip = models.GenericIPAddressField(blank=True, null=True, default='')
    location = models.CharField(blank=True, null=True, default='', max_length=30)
    department = models.CharField(blank=True, null=True, default='', max_length=30)
    location_contact = models.CharField(blank=True, null=True, default='', max_length=30)
    inv = models.ForeignKey(Inv, on_delete=models.SET_NULL, null=True, blank=True, related_name="profile_inv")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "assets:prof_detail",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    def clean(self):
        # Don't allow empty record.
        if self.username is None and \
                self.userid is None and \
                self.email is None and \
                self.host is None and \
                self.ip == "":
            raise ValidationError(_('You must fill in one of the fields: Username, UserID, Email, Host, IP'))

    class Meta:
        ordering = ["id"]