# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : invs/models.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Models file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
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
from tinymce.models import HTMLField
User = get_user_model()
# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
register = template.Library()

class CurrencyType(models.Model):
    objects = models.Manager()
    currencyname = models.CharField(max_length=20, default="", null=True, blank=True)
    currencyshortname = models.CharField(max_length=3, default="", null=True, blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.currencyshortname


class InvStatus(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=20)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=500, default='')
    description_html = models.TextField(max_length=750, editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(InvStatus, self).save(*args, **kwargs)


class InvPhase(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=40)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=100, default="")
    description_html = models.TextField(max_length=150, editable=True, default='', blank=True)

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
    description_html = models.TextField(max_length=750, editable=True, default='', blank=True)

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
    description_html = models.TextField(max_length=750, editable=True, default='', blank=True)
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
    description_html = models.TextField(max_length=750, editable=True, default='', blank=True)

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
    description_html = models.TextField(max_length=750, editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(InvAttackvector, self).save(*args, **kwargs)


def timediff(pdate1, pdate2):
    if pdate1 and pdate2:
        diff = pdate2 - pdate1
        days, seconds = diff.days, diff.seconds
        # print(days)
        # print(seconds)
        retval = seconds + days * 60 * 60 * 24
    else:
        retval = None
    return retval


# Create your models here.
class Inv(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name="inv_users")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="inv_parent")
    invid = models.CharField(max_length=20, default="", null=True, blank=True)
    refid = models.CharField(max_length=20, default="", null=True, blank=True)
    ticketid = models.CharField(max_length=20, default="", null=True, blank=True)
    status = models.ForeignKey(InvStatus, on_delete=models.SET_DEFAULT, default="1",
                               related_name="inv_status")
    phase = models.ForeignKey(InvPhase, on_delete=models.SET_DEFAULT, default="1",
                              related_name="inv_phase")
    severity = models.ForeignKey(InvSeverity, on_delete=models.SET_DEFAULT, default="1",
                                 related_name="inv_severity")
    category = models.ForeignKey(InvCategory, on_delete=models.SET_DEFAULT, default="1",
                                 related_name="inv_category")
    priority = models.ForeignKey(InvPriority, on_delete=models.SET_NULL, null=True, default=None,
                                 related_name="inv_priority")
    attackvector = models.ForeignKey(InvAttackvector, on_delete=models.SET_DEFAULT, default="1", blank=False,
                                     null=False, related_name="inv_attackvector")
    # description = models.CharField(max_length=200, default="")
    # description_html = models.TextField(editable=True, default='', blank=True)
    description = HTMLField()
    description_html = HTMLField()
    summary = models.CharField(max_length=2000, default="", blank=True, null=True)
    comment = models.CharField(max_length=50, default="", blank=True, null=True)
    processimprovement = models.CharField(max_length=2000, default="", blank=True, null=True)
    starttime = models.DateTimeField(auto_now=False, blank=True, null=True)
    endtime = models.DateTimeField(auto_now=False, blank=True, null=True)
    invduration = models.PositiveIntegerField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")

    potentialloss = models.PositiveIntegerField(default=0, blank=False, null=False)
    monetaryloss = models.PositiveIntegerField(default=0, blank=False, null=False)
    losscurrency = models.ForeignKey(CurrencyType, on_delete=models.SET_DEFAULT, default="1",
                                     related_name="inv_currencytype", blank=True, null=False)
    numofvictims = models.PositiveIntegerField(default=None, blank=True, null=True)
    # check if the status has been changed
    __original_status = None

    def __init__(self, *args, **kwargs):
        super(Inv, self).__init__(*args, **kwargs)
        self.__original_status = self.status

    class Meta:
        ordering = ['-id']

    def __str__(self):
        if self.ticketid:
            outstr = "%s-%s-%s-%s"%(self.pk, self.attackvector.name, self.ticketid, str(self.user)[0:2])
        else:
            outstr = "%s-%s-%s" % (self.pk, self.attackvector.name, str(self.user)[0:2])
        return outstr

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
            self.phase = InvPhase.objects.get(pk=4)
        #  if start time is not set, set it to the investigation creation date
        if self.starttime is None:
            self.starttime = timezone_now()

        if self.starttime is not None and self.endtime is not None:
            self.invduration = timediff(self.starttime, self.endtime)
            if self.invduration < 0:
                self.invduration = 0
        else:
            self.invduration = None

        self.description_html = misaka.html(self.description)
        # super(Inv, self).save(*args, **kwargs)
        super(Inv, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_status = self.status

    def invdurationprint(self):
        if self.invduration:
            tduration = self.invduration
            day = int(tduration // (24 * 3600))
            tduration = tduration % (24 * 3600)
            hour = int(tduration // 3600)
            tduration %= 3600
            minutes = int(tduration // 60)
            tduration %= 60
            seconds = int(tduration)
            retval = str(day)+"d"+str(hour)+"h"+str(minutes)+"m"+str(seconds)+"s"
        else:
            retval = "-"
        return retval

    def opentasklistprint(self):
        retval = self.task_inv.exclude(status__name='Completed').exclude(status__name='Skipped').count()
        return retval

    def get_absolute_url(self):
        return reverse(
            "invs:inv_detail",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    def clean(self):
        # if self.invid == '':
            # raise ValidationError(_('You must enter an Investigation ID.'))
            # self.invid = self.attackvector.name
        if self.status.name == "Closed":
            # check if the numofvictims is defined
            if self.numofvictims is None:
                raise ValidationError(_('Please define the "Victim Count"!'))
            if self.task_inv.all():
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


def new_inv(pstatus, ppriority, pdescription, pphase, pseverity, pcategory, pattackvector,pinvid=None,
            puser="action", pticketid=None, pparent=None, prefid=None, psummary=None, pcomment=None, pstarttime=None, pendtime=None,
            pinvduration=None, pcreated_at=None, pcreated_by=None, pmodified_at=None, pmodified_by=None,
            pmonetaryloss=None, plosscurrency=None, pnumofvictims=None
            ):
    new_inv_item = Inv.objects.create(
                                user=puser,
                                parent=pparent,
                                invid=pinvid,
                                ticketid=pticketid,
                                refid=prefid,
                                status=pstatus,
                                phase=pphase,
                                severity=pseverity,
                                category=pcategory,
                                priority=ppriority,
                                attackvector=pattackvector,
                                description=pdescription,
                                summary=psummary,
                                comment=pcomment,
                                starttime=pstarttime,
                                endtime=pendtime,
                                invduration=pinvduration,
                                created_at=pcreated_at,
                                created_by=pcreated_by,
                                modified_at=pmodified_at,
                                modified_by=pmodified_by,
                                monetaryloss=pmonetaryloss,
                                losscurrency=plosscurrency,
                                numofvictims=pnumofvictims
                            )
    return new_inv_item
