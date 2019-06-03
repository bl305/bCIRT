from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# HTML renderer
import misaka
from django.utils.timezone import now as timezone_now
# Get the user so we can use this
from django import template
from django.contrib.auth import get_user_model
User = get_user_model()
# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
register = template.Library()


class InvStatus(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=20)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(InvStatus, self).save(*args, **kwargs)


class InvPhase(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=40)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(InvPhase, self).save(*args, **kwargs)


class InvSeverity(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=40)
    enabled = models.BooleanField(default=True)
    description = models.CharField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(InvSeverity, self).save(*args, **kwargs)


class InvCategory(models.Model):
    objects = models.Manager()
    catid = models.CharField(max_length=10, default="")
    name = models.CharField(max_length=40)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)
    reporting_timeframe = models.TextField(max_length=500, default="")

    def __str__(self):
        return str(self.catid) + " - " + str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(InvCategory, self).save(*args, **kwargs)


class InvPriority(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=40)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(InvPriority, self).save(*args, **kwargs)


class InvAttackvector(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=40)
    enabled = models.BooleanField(default=True)
    description = models.CharField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(InvAttackvector, self).save(*args, **kwargs)


def timediff(pdate1, pdate2):
    if pdate1 and pdate2:
        diff = pdate2 - pdate1
        days, seconds = diff.days, diff.seconds
        print(days)
        print(seconds)
        retval = seconds + days * 60 * 60 * 24
    else:
        retval = None
    return retval


# Create your models here.
class Inv(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="inv_users")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="inv_parent")
    invid = models.CharField(max_length=20)
    status = models.ForeignKey(InvStatus, on_delete=models.SET_DEFAULT, default="1", related_name="inv_status")
    phase = models.ForeignKey(InvPhase, on_delete=models.SET_DEFAULT, default="1", related_name="inv_phase")
    severity = models.ForeignKey(InvSeverity, on_delete=models.SET_DEFAULT, default="1", related_name="inv_severity")
    category = models.ForeignKey(InvCategory, on_delete=models.SET_DEFAULT, default="1", related_name="inv_category")
    priority = models.ForeignKey(InvPriority, on_delete=models.SET_NULL, null=True, default=None,
                                 related_name="inv_priority")
    attackvector = models.ForeignKey(InvAttackvector, on_delete=models.SET_DEFAULT, default="1", blank=True, null=True,
                                     related_name="inv_attackvector")
    description = models.CharField(max_length=200, default="")
    description_html = models.TextField(editable=True, default='', blank=True)
    summary = models.CharField(max_length=2000, default="", blank=True, null=True)
    comment = models.CharField(max_length=50, default="", blank=True, null=True)
    starttime = models.DateTimeField(auto_now=False, blank=True, null=True)
    endtime = models.DateTimeField(auto_now=False, blank=True, null=True)
    invduration = models.PositiveIntegerField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")

    # check if the status has been changed
    __original_status = None

    def __init__(self, *args, **kwargs):
        super(Inv, self).__init__(*args, **kwargs)
        self.__original_status = self.status

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.invid

    # def save(self, *args, **kwargs):
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        #  this is to check if the status record has been changed or not
        if self.status != self.__original_status:
            if self.status.name == "Closed":
                # status changed do something here
                # some actions are performed in the "check" method
                pass
        if self.status.name == "Closed":
            # status changed to closed
            # set investigation close date
            if self.endtime is None:
                # self.endtime = datetime.now()
                self.endtime = timezone_now()
        #  if start time is not set, set it to the investigation creation date
        if self.starttime is None:
            self.starttime = timezone_now()

        if self.starttime is not None and self.endtime is not None:
            self.invduration = timediff(self.starttime, self.endtime)
            print(self.starttime)
            print(self.endtime)
        else:
            self.invduration = None

        self.description_html = misaka.html(self.description)
        # super(Inv, self).save(*args, **kwargs)
        super(Inv, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_status = self.status

    def invdurationprint(self):
        if self.invduration:
            tduration = self.invduration
            day = tduration // (24 * 3600)
            tduration = tduration % (24 * 3600)
            hour = tduration // 3600
            tduration %= 3600
            minutes = tduration // 60
            tduration %= 60
            seconds = tduration
            retval = str(day)+"d"+str(hour)+"h"+str(minutes)+"m"+str(seconds)+"s"
        else:
            retval = "-"
        return retval

    def get_absolute_url(self):
        return reverse(
            "invs:inv_detail",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    def clean(self):
        if self.invid == '':
            raise ValidationError(_('You must enter an Investigation ID.'))
        if self.status.name == "Closed":
            # status changed to closed, check if all tasks are closed
            anyopen = 0
            for atask in self.task_inv.all():
                if (atask.status.name == 'Completed') or (atask.status.name == 'Skipped'):
                    pass
                else:
                    anyopen += 1
            if anyopen:
                raise ValidationError(_('Cannot close the Investigation with open Tasks.'))
            if self.user is None:
                raise ValidationError(_('Assign field cannot be empty.'))
            # set investigation close date
            if self.endtime is None:
                self.endtime = timezone_now()
        if self.status.name == "Assigned" and self.user is None:
            raise ValidationError(_('If status is "Assigned", an "Assigned to" user must be selected.'))
        if self.status.name == "Open" and self.user is not None:
            raise ValidationError(_('If status is "Open", the "Assigned to" user must be empty too.'))
        super(Inv, self).clean()
