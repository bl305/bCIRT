from django.db import models
from uuid import uuid1
import misaka
from tinymce.models import HTMLField
from django.urls import reverse
from django.utils.timezone import now as timezone_now
import random
import string
import os
from django.db import transaction
from django.dispatch import receiver
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR, S_IWGRP

def create_random_string(length=8):
    if length <= 0:
        length = 8

    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join([random.choice(symbols) for x in range(length)])


def upload_to_kb(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return 'uploads/actions/{}_{}_{}_{}{}'.format(
        instance.pk,
        filename.lower(),
        now.strftime("%Y%m%d%H%M%S"),
        create_random_string(),
        filename_ext.lower()
    )


class KnowledgeBaseFormat(models.Model):
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)
    #  to satisfy pyCharm

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(KnowledgeBaseFormat, self).save(*args, **kwargs)


class KnowledgeBase(models.Model):
    myuuid = models.UUIDField(unique=True, default=uuid1, editable=False)
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    builtin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    kbformat = models.ForeignKey(KnowledgeBaseFormat, on_delete=models.SET_DEFAULT, default=1, null=False,
                                       blank=False, related_name="kb_kbformat")
    title = models.CharField(max_length=50, default="", blank=False, null=False)
    description = HTMLField()
    fileName = models.CharField(max_length=255, default="", null=True, blank=True)
    fileRef = models.FileField(upload_to=upload_to_kb, null=True, blank=True)
    filecreated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    #    class Meta:
    #        ordering = ['-id']

    class Meta:
        ordering = ['id']

    def __str__(self):
        # return self.description
        return str(self.pk)

    def get_absolute_url(self):
        return reverse(
            "tasks:ev_detail",
            kwargs={
                # "username": self.user.username,
                # "inv_pk": '3',
                # "task_pk": '3',
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
                super(KnowledgeBase, self).save(*args, **kwargs)
                self.fileRef = file_to_save
            # kwargs.pop('force_insert')
        super(KnowledgeBase, self).save(*args, **kwargs)

    def clean(self):
        # if self.inv is None and self.task is None:
        #     raise ValidationError(_('You must select an Investigation or a Task.'))
        # if self.task and Task.objects.filter(pk=self.task.pk).exists:
        #     if self.task and Task.objects.get(pk=self.task.pk).readonly():
        #         raise ValidationError(_('Task cannot be closed!'))

        super(KnowledgeBase, self).clean()


# Replace/delete files
@receiver(models.signals.post_delete, sender=KnowledgeBase)
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
