from django.db import models
from tinymce.models import HTMLField
from django.utils.timezone import now as timezone_now
import os
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR, S_IWGRP
import string
import random
from django.urls import reverse
from django.dispatch import receiver
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


# Create your models here.
class UpdatePackage(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="update_users")
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
