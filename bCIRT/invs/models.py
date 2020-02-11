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
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import transaction
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


# class InvApproval(models.Model):
#     objects = models.Manager()
#     usertoreview = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None,
#                              related_name="invapproval_subjectuser")
#     reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None,
#                              related_name="invapproval_reviewer")
#     enabled = models.BooleanField(default=True)
#
#     def __str__(self):
#         return "%s - %s" % (self.usertoreview, self.reviewer)


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


class InvAttackVector(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=40)
    enabled = models.BooleanField(default=True)
    description = models.CharField(max_length=500, default="")
    description_html = models.TextField(max_length=750, editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(InvAttackVector, self).save(*args, **kwargs)


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                             related_name="inv_users")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, default=None,null=True, blank=True,
                               related_name="inv_parent")
    invid = models.CharField(max_length=20, default="", null=True, blank=True)
    refid = models.CharField(max_length=20, default="", null=True, blank=True)
    ticketid = models.CharField(max_length=20, default="", null=True, blank=True)
    status = models.ForeignKey(InvStatus, on_delete=models.SET_DEFAULT, default="1",
                               related_name="inv_status")
    reviewer1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, blank=True, null=True,
                                  related_name="inv_reviewer1")
    reviewer2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, blank=True, null=True,
                                  related_name="inv_reviewer2")
    # reviewer1 = models.CharField(max_length=20, default="Pending")
    reviewer1comment = models.CharField(max_length=2000, default="", blank=True, null=True)
    # reviewer2 = models.CharField(max_length=20, default="Pending")
    reviewer2comment = models.CharField(max_length=2000, default="", blank=True, null=True)
    phase = models.ForeignKey(InvPhase, on_delete=models.SET_DEFAULT, default="1",
                              related_name="inv_phase")
    severity = models.ForeignKey(InvSeverity, on_delete=models.SET_DEFAULT, default="1",
                                 related_name="inv_severity")
    category = models.ForeignKey(InvCategory, on_delete=models.SET_DEFAULT, default="1",
                                 related_name="inv_category")
    priority = models.ForeignKey(InvPriority, on_delete=models.SET_NULL, null=True, default=None,
                                 related_name="inv_priority")
    attackvector = models.ForeignKey(InvAttackVector, on_delete=models.SET_DEFAULT, default="1", blank=False,
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
    reviewed1_at = models.DateTimeField(auto_now_add=False, default=None, blank=True, null=True)
    reviewed1_by = models.CharField(max_length=20, default=None, blank=True, null=True)
    reviewed2_at = models.DateTimeField(auto_now_add=False, default=None, blank=True, null=True)
    reviewed2_by = models.CharField(max_length=20, default=None, blank=True, null=True)

    potentialloss = models.PositiveIntegerField(default=0, blank=False, null=False)
    monetaryloss = models.PositiveIntegerField(default=0, blank=False, null=False)
    losscurrency = models.ForeignKey(CurrencyType, on_delete=models.SET_DEFAULT, default="1",
                                     related_name="inv_currencytype", blank=True, null=False)
    numofvictims = models.PositiveIntegerField(default=None, blank=True, null=True)
    incstarttime = models.DateTimeField(auto_now=False, blank=True, null=True)
    incendtime = models.DateTimeField(auto_now=False, blank=True, null=True)

    # check if the status has been changed
    __original_status = None

    def __init__(self, *args, **kwargs):
        super(Inv, self).__init__(*args, **kwargs)
        self.__original_status = self.status

    class Meta:
        ordering = ['-id']

    def __str__(self):
        if self.ticketid:
            outstr = "%s-%s-%s-%s" % (self.pk, self.attackvector.name, self.ticketid, str(self.user)[0:2])
        else:
            outstr = "%s-%s-%s" % (self.pk, self.attackvector.name, str(self.user)[0:2])
        return outstr

    def readonly(self):
        if self.status.name == 'Closed' or self.status.name == 'Archived' \
                or self.status.name == 'Review1' or self.status.name == 'Review2':
            return True
        else:
            return False

    @transaction.atomic
    # def save(self, *args, **kwargs):
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        # print("SAVING")
        #  this is to check if the status record has been changed or not
        status_closed = self.status.name == "Closed"
        status_assigned = self.status.name == "Assigned"
        status_review1 = self.status.name == "Review1"
        status_review2 = self.status.name == "Review2"
        if self.status != self.__original_status:
            if status_closed:
                # status changed do something here
                # some actions are performed in the "check" method
                pass
            elif status_assigned:
                # status changed to assigned
                self.reviewed1_at = None
                self.reviewed2_at = None
                pass
            elif status_review1:
                # status changed to review1
                # checking if needs review or not
                # print("1REV1")
                if self.needreview(1):
                    # print("1REV1 REQ")
                    self.getreviewer1()
                else:
                    # no review1 is needed
                    # print("1REV1 XXX")
                    self.autoreview1()
                    # print("1REV2")
                    if self.needreview(2):
                        # print("1REV2 REQ")
                        self.getreviewer2()
                    else:
                        # print("1REV2 XXX")
                        self.autoreview2()
            elif status_review2:
                # print("2REV1")
                # status changed to review2
                # checking if needs review or not
                if self.needreview(2):
                    # print("2REV1 REQ")
                    self.getreviewer2()
                else:
                    # print("2REV1 XXX")
                    # no review is needed
                    # self.reviewer2 = User.objects.get(pk=1)
                    self.autoreview2()
        if status_closed or status_review1 or status_review2:
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

    @transaction.atomic
    def getreviewer1(self):
        reviewers1 = User.objects.filter(profile__reviewer1=True)
        reviewers1list = set()
        for reviewer1 in reviewers1:
            reviewers1list.add(reviewer1)
        randomreviewer1 = reviewers1.order_by("?").first()
        self.reviewer1 = randomreviewer1

    @transaction.atomic
    def getreviewer2(self):
        reviewers2 = User.objects.filter(profile__reviewer2=True)
        reviewers2list = set()
        for reviewer2 in reviewers2:
            reviewers2list.add(reviewer2)
        randomreviewer2 = reviewers2.order_by("?").first()
        self.reviewer2 = randomreviewer2

    @transaction.atomic
    def autoreview1(self):
        self.reviewer1 = User.objects.get(pk=1)
        self.reviewed1_by = "autoreview"
        self.reviewed1_at = timezone_now()
        self.reviewer2 = User.objects.get(pk=1)
        self.status = InvStatus.objects.get(name="Review2")

    @transaction.atomic
    def autoreview2(self):
        self.reviewed2_by = "autoreview"
        self.reviewed2_at = timezone_now()
        self.status = InvStatus.objects.get(name="Closed")

    def needreview(self, revtype=1):
        # checks if the investigation needs review or not
        # if a bypass rule is matching, it will be bypassed. bypass rules are the opposite of normal rules
        bypassreview = False
        bypasslist = None
        if revtype == 1:
            bypasslist = InvReviewRules.objects.filter(bypassreview=True, review1=False)\
                .select_related('severity')
        elif revtype == 2:
            bypasslist = InvReviewRules.objects.filter(bypassreview=True, review2=False)\
                .select_related('severity')
        for bypassrule in bypasslist:
            if bypassrule.bypassreview:
                if (bypassrule.severity is None or int(bypassrule.severity.pk) >= int(self.severity.pk)) and \
                    (bypassrule.category is None or bypassrule.category == self.category) and \
                    (bypassrule.priority is None or bypassrule.priority == self.priority) and \
                    (bypassrule.attackvector is None or bypassrule.attackvector == self.attackvector) and \
                    (bypassrule.potentialloss == 0 or bypassrule.potentialloss >= self.potentialloss) and \
                    (bypassrule.monetaryloss == 0 or bypassrule.monetaryloss >= self.monetaryloss):
                    bypassreview = True

        # if no bypass rule matched
        needreview = False
        if not bypassreview:
            invruleslist = None
            if revtype == 1:
                invruleslist = InvReviewRules.objects.filter(bypassreview=False, review1=True)\
                    .select_related('severity')
            elif revtype == 2:
                invruleslist = InvReviewRules.objects.filter(bypassreview=False, review2=True)\
                    .select_related('severity')
            if invruleslist:
                for invrule in invruleslist:
                    if (invrule.severity is None or int(invrule.severity.pk) <= int(self.severity.pk)) and \
                        (invrule.category is None or invrule.category == self.category) and \
                        (invrule.priority is None or invrule.priority == self.priority) and \
                        (invrule.attackvector is None or invrule.attackvector == self.attackvector) and \
                        (invrule.potentialloss == 0 or invrule.potentialloss <= self.potentialloss) and \
                        (invrule.monetaryloss == 0 or invrule.monetaryloss <= self.monetaryloss):
                        needreview = True
        # retval = False
        if bypassreview:
            retval = False
        elif needreview:
            retval = True
        else:
            retval = False
        return retval

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

    def opentasklist(self):
        retval = self.task_inv.exclude(status__name='Completed').exclude(status__name='Skipped')
        return retval

    def tasklist(self):
        retval = self.task_inv.all()
        return retval

    def get_absolute_url(self):
        return reverse(
            "invs:inv_detail",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    def evidences_table(self):
        retval = self.evidence_inv.all()\
            .select_related('task') \
            .select_related('evidenceformat')\
            .select_related('mitretactic') \
            .select_related('parent') \
            .select_related('parentattr')
        return retval

    def tasks_table(self):
        retval = self.task_inv.all()\
            .select_related('status')\
            .select_related('action') \
            .select_related('actiontarget')\
            .select_related('playbook')\
            .select_related('type')
        return retval

    def clean(self):
        # check if review1 were performed before review2
        # raise ValidationError(_("xx"+str(self.status)))
        if self.__original_status.name == "Closed" and (self.status.name == "Review1" or self.status.name == "Review2"):
            raise ValidationError(_('Cannot select '+self.status.name+' if the previous status was "Closed"!'))
        if self.status.name == "Closed" or self.status.name == "Review1" or self.status.name == "Review2":
            # check if the numofvictims is defined
            if self.numofvictims is None:
                raise ValidationError(_('Please define the "Victim Count"!'))
            if self.status.name == "Closed" and self.reviewed1_by is None:
                # check if reviews were performed
                raise ValidationError(_('No review #1 was performed yet!'))
            if self.status.name == "Closed" and (self.reviewed1_at is None or self.reviewed2_at is None):
                raise ValidationError(_('No reviews were performed yet!'))
            if self.reviewed1_at is None and self.reviewed2_at is not None:
                raise ValidationError(_('First review must happen first!'))
            task_inv_all = self.task_inv.select_related('status').all()
            if task_inv_all.iterator():
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

class InvDetailTabEvidences():
    def inv_tab_evidences_inv(self, inv_pk):
        retval = Inv.objects.filter(pk=inv_pk) \
            .select_related('status')[0]
        return retval

    def inv_tab_evidences_invevidences(self, inv_pk):
        retval = Inv.objects.filter(pk=inv_pk)\
            .select_related('evidence_inv__pk')\
            .select_related('evidence_inv__fileRef')\
            .select_related('evidence_inv__fileName')\
            .select_related('evidence_inv__task__pk')\
            .select_related('evidence_inv__task__title')\
            .select_related('evidence_inv__created_at')\
            .select_related('evidence_inv__created_by')\
            .select_related('evidence_inv__modified_at')\
            .select_related('evidence_inv__modified_by')\
            .select_related('evidence_inv__mitretactic__name')\
            .select_related('evidence_inv__parent__pk')\
            .select_related('evidence_inv__parentattr__pk')\
            .select_related('evidence_inv__evidenceformat__pk')\
            .select_related('evidence_inv__description')\
            .values('pk', 'evidence_inv__pk', 'evidence_inv__fileRef', 'evidence_inv__fileName',
                    'evidence_inv__task__pk', 'evidence_inv__task__title', 'evidence_inv__created_at',
                    'evidence_inv__created_by', 'evidence_inv__modified_at', 'evidence_inv__modified_by',
                    'evidence_inv__mitretactic__name', 'evidence_inv__parent__pk', 'evidence_inv__parentattr__pk',
                    'evidence_inv__evidenceformat__pk', 'evidence_inv__description').order_by('evidence_inv__pk')
        return retval


class InvReviewRules(models.Model):
    objects = models.Manager()
    bypassreview = models.BooleanField(default=False)
    rulename = models.CharField(max_length=50, default="", null=False, blank=False)
    severity = models.ForeignKey(InvSeverity, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                 related_name="invreviewrules_severity")
    category = models.ForeignKey(InvCategory, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                 related_name="invreviewrules_category")
    priority = models.ForeignKey(InvPriority, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                 related_name="invreviewrules_priority")
    attackvector = models.ForeignKey(InvAttackVector, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                     related_name="invreviewrules_attackvector")
    potentialloss = models.PositiveIntegerField(default=0, blank=False, null=False)
    monetaryloss = models.PositiveIntegerField(default=0, blank=False, null=False)
    review1 = models.BooleanField(default=True)
    review2 = models.BooleanField(default=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.rulename


def new_inv(pstatus, ppriority, pdescription, pphase, pseverity, pcategory, pattackvector, pinvid=None,
            puser="action", pticketid=None, pparent=None, prefid=None, psummary=None, pcomment=None, pstarttime=None,
            pendtime=None,
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

class InvList():
    def get_invlist(self, pexcl=None, allownull=False):
        inv_obj = None
        if pexcl:
            inv_objs = Inv.objects.exclude(pk=pexcl)\
                .select_related('attackvector__name')\
                .select_related('user__username')\
                .values_list('pk', 'attackvector__name', 'ticketid', 'user__username')
        else:
            inv_objs = Inv.objects.select_related('attackvector__name')\
                .select_related('user__username')\
                .values_list('pk', 'attackvector__name', 'ticketid', 'user__username')
        outlist = list()
        if allownull:
            outlist.append(('', 'None'))
        NoneType = type(None)
        if inv_objs.exists():
            for inv in inv_objs:
                if type(inv[2]) == NoneType:
                    outstr = "%s-%s-%s" % (int(inv[0]), str(inv[1]), str(inv[3])[0:2])
                else:
                    outstr = "%s-%s-%s-%s" % (int(inv[0]), str(inv[1]), str(inv[2]), str(inv[3])[0:2])
                outlist.append((inv[0], outstr))
        return outlist