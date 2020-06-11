# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : configuration/models.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Models file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# 2019.08.12  Lendvay     2      Added decrypt_string function
# **********************************************************************;
from django.db import models
from tinymce.models import HTMLField
from django.utils.timezone import now as timezone_now
import os
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR, S_IWGRP
import string
import random
from django.db import transaction
from django.urls import reverse
from django.dispatch import receiver
import misaka
from SupportingScripts.encrypion_bcirt_simple import bCIRT_Encryption
from bCIRT.custom_variables import ENCRYPTION_KEY_1, SALT_1
from django.contrib.auth import get_user_model
User = get_user_model()


def create_random_string(length=8):
    if length <= 0:
        length = 8
    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join([random.choice(symbols) for x in range(length)])


def upload_to_updates(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return 'uploads/configuration/updates/{}_{}_{}_{}{}'.format(
        instance.pk,
        filename.lower(),
        now.strftime("%Y%m%d%H%M%S"),
        create_random_string(),
        filename_ext.lower()
    )

from django.conf import settings
# Create your models here.
class UpdatePackage(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True, related_name="update_users")
    updateversion = models.CharField(max_length=15, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    description = HTMLField()
    fileName = models.CharField(max_length=255, default="", null=True, blank=True)
    fileRef = models.FileField(upload_to=upload_to_updates, null=True, blank=True)
    filecreated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        # return self.description
        return str(self.pk)

    def get_absolute_url(self):
        return reverse(
            "configuration:conf_base",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    @transaction.atomic
    def save(self, *args, **kwargs):
        # this removes the filename if a file is not attached
        if not self.fileRef:
            self.fileName = ""
        #  This little trick saves the record without the file and then saves the file.
        #  The instance ID is not available at the first save, so the filename cannot have it
        #  alternative would be to use UUID as table ID or as a custom field to track evidences
        if self.pk is None:
            if self.fileRef:
                file_to_save = self.fileRef
                self.fileRef = None
                super(UpdatePackage, self).save(*args, **kwargs)
                self.fileRef = file_to_save
        super(UpdatePackage, self).save(*args, **kwargs)

    def clean(self):
        super(UpdatePackage, self).clean()

# Connections model


class ConnectionItem(models.Model):
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=20, blank=False, null=False)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(ConnectionItem, self).save(*args, **kwargs)


class ConnectionItemField(models.Model):
    objects = models.Manager()
    connectionitemid = models.ForeignKey(ConnectionItem, on_delete=models.CASCADE, blank=False, null=False,
                                         related_name="connectionitemfield_connectionitem")
    connectionitemfieldname = models.CharField(max_length=20, blank=False, null=False)
    connectionitemfieldvalue = models.CharField(max_length=256, blank=False, null=False)
    encryptvalue = models.BooleanField(default=True)

    def __str__(self):
        return str(self.connectionitemfieldname)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.encryptvalue:
            key = bCIRT_Encryption().generate_key_manual(ENCRYPTION_KEY_1, SALT_1)
            strenc = bCIRT_Encryption().encrypt_string(self.connectionitemfieldvalue, key)
            self.connectionitemfieldvalue = strenc.decode()
        super(ConnectionItemField, self).save(*args, **kwargs)

    def decrypted_string(self):
        key = bCIRT_Encryption().generate_key_manual(ENCRYPTION_KEY_1, SALT_1)
        strdec = bCIRT_Encryption().decrypt_string(key, self.connectionitemfieldvalue.encode()).decode()
        return strdec


def decrypt_string(pstr):
    key = bCIRT_Encryption().generate_key_manual(ENCRYPTION_KEY_1, SALT_1)
    strdec = bCIRT_Encryption().decrypt_string(key, pstr.encode()).decode()
    return strdec


# Replace/delete files
@receiver(models.signals.post_delete, sender=UpdatePackage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `InvestigationDetails` object is deleted.
    """
    if instance.fileRef:
        if os.path.isfile(instance.fileRef.path):
            #  This makes the files writable
            os.chmod(instance.fileRef.path, S_IWUSR | S_IREAD | S_IRGRP | S_IWGRP | S_IROTH)
            os.remove(instance.fileRef.path)
            instance.fileName = None


@receiver(models.signals.post_save, sender=UpdatePackage)
def auto_make_readonly(sender, instance, **kwargs):
    """
    Make evidences read-only on the filesystem
    """
    if instance.fileRef:
        if os.path.isfile(instance.fileRef.path):
            #  This makes the files readonly
            os.chmod(instance.fileRef.path, S_IREAD | S_IRGRP | S_IROTH)


@receiver(models.signals.pre_save, sender=UpdatePackage)
@transaction.atomic
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `InvestigationDetails` object is changed.
    """
    if not instance.pk:
        return False

    try:
        old_file = UpdatePackage.objects.get(pk=instance.pk).fileRef
    except UpdatePackage.DoesNotExist:
        return False

    new_file = instance.fileRef
    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                #  This makes the files writable
                os.chmod(old_file.path, S_IWUSR | S_IREAD | S_IRGRP | S_IWGRP | S_IROTH)
                os.remove(old_file.path)
        except Exception:
            return False


class SettingsCategory(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                             related_name="settingscategory_users")
    categoryname = models.CharField(max_length=25, null=True, blank=True, default=None)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    description = models.CharField(max_length=255, null=True, blank=True, default=None)

    def __str__(self):
        # return self.description
        return str(self.categoryname)

    def get_absolute_url(self):
        return reverse(
            "configuration:conf_base",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    @transaction.atomic
    def save(self, *args, **kwargs):
        super(SettingsCategory, self).save(*args, **kwargs)

    def clean(self):
        super(SettingsCategory, self).clean()


class SettingsUser(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True,
                             related_name="settingsuser_users")
    settingname = models.CharField(max_length=25, null=True, blank=True, default=None)
    settingvalue = models.CharField(max_length=255, null=True, blank=True, default=None)
    settingcategory = models.ForeignKey(SettingsCategory, on_delete=models.SET_NULL, blank=True, null=True,
                                         default=None, related_name="settingsuser_settingscategory")
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    description = models.CharField(max_length=255, null=True, blank=True, default=None)

    def __str__(self):
        # return self.description
        return str(self.pk)

    def get_absolute_url(self):
        return reverse(
            "configuration:conf_base",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    @transaction.atomic
    def save(self, *args, **kwargs):
        super(SettingsUser, self).save(*args, **kwargs)

    def clean(self):
        super(SettingsUser, self).clean()


class SettingsSystem(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                             related_name="settingssystem_users")
    settingname = models.CharField(max_length=25, null=True, blank=True, default=None)
    settingvalue = models.CharField(max_length=255, null=True, blank=True, default=None)
    settingcategory = models.ForeignKey(SettingsCategory, on_delete=models.SET_NULL, blank=True, null=True,
                                         default=None, related_name="settingssystem_settingscategory")
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    description = models.CharField(max_length=255, null=True, blank=True, default=None)

    def __str__(self):
        # return self.description
        return str(self.pk)

    def get_absolute_url(self):
        return reverse(
            "configuration:conf_base",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    @transaction.atomic
    def save(self, *args, **kwargs):
        super(SettingsSystem, self).save(*args, **kwargs)

    def clean(self):
        super(SettingsSystem, self).clean()
