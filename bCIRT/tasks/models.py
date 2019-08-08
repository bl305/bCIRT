# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : tasks/models.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Models file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from django.db import models
from django.urls import reverse
import tempfile
# HTML renderer
import misaka
from invs.models import Inv
from tinymce.models import HTMLField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.dispatch import receiver
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR, S_IWGRP
import ipaddress
import re
import pathlib
from bCIRT.settings import PROJECT_ROOT
from django.utils.timezone import now as timezone_now
import random
import string
import magic
import os
from os import path
import hashlib
from shutil import copy
from base64 import b64encode
from bCIRT.settings import MEDIA_ROOT
from .scriptmanager.run_script import run_script_class
import logging
logger = logging.getLogger('log_file_verbose')

# Get the user so we can use this
from django.contrib.auth import get_user_model
User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
from django import template
register = template.Library()


# Create your models here.
# ###Supporting functions
# Create your models here.
def create_random_string(length=8):
    if length <= 0:
        length = 8

    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join([random.choice(symbols) for x in range(length)])


def upload_to_action(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return 'uploads/actions/{}_{}_{}_{}{}'.format(
        instance.pk,
        filename.lower(),
        now.strftime("%Y%m%d%H%M%S"),
        create_random_string(),
        filename_ext.lower()
    )


def upload_to_evidence(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    # return 'evidences/uploads/evidences/{}_{}_{}_{}{}'.format(
    # this is also used in the script, so if changed here, need to change when attaching files
    return 'uploads/evidences/{}_{}_{}_{}{}'.format(
        instance.pk,
        filename.lower(),
        now.strftime("%Y%m%d%H%M%S"),
        create_random_string(),
        filename_ext.lower()
    )


def timediff(pdate1, pdate2):
    if pdate1 and pdate2:
        diff = pdate2 - pdate1

        days, seconds = diff.days, diff.seconds
        # print(days)
        # print(seconds)
        retval = seconds + days * 60 * 60 * 24
        # hours = days * 24 + seconds // 3600
        # minutes = (seconds % 3600) // 60
        # seconds = seconds % 60
        # return {'hours': hours, 'minutes': minutes, 'seconds': seconds}
        #minutes = (diff.seconds % 3600) // 60
    else:
        retval = None
    return retval


def check_file_type(pfile):
    f = magic.Magic()
    ftype = f.from_file(pfile)
    if ftype.startswith("PNG") or ftype.startswith('JPG') or ftype.startswith('BMP'):
        return "image"
    elif ftype.startswith("ASCII"):
        return "text"
    else:
        return "na"

class MitreAttck_Tactics(models.Model):
    objects = models.Manager()
    matacid = models.CharField(max_length=6, blank=False, null=False)
    name = models.CharField(max_length=25, blank=False, null=False)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(MitreAttck_Tactics, self).save(*args, **kwargs)


class MitreAttck_Techniques(models.Model):
    objects = models.Manager()
    matacref = models.ForeignKey(MitreAttck_Tactics, on_delete=models.SET_DEFAULT, default=None, related_name="matec_matac")
    matecid = models.CharField(max_length=6, blank=False, null=False)
    name = models.CharField(max_length=25, blank=False, null=False)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(MitreAttck_Techniques, self).save(*args, **kwargs)


class TaskStatus(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=20)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(TaskStatus, self).save(*args, **kwargs)


class TaskType(models.Model):
    objects = models.Manager()
    typeid = models.CharField(max_length=10, default="")
    name = models.CharField(max_length=20)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.typeid) + " - " + str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(TaskType, self).save(*args, **kwargs)


class TaskCategory(models.Model):
    objects = models.Manager()
    catid = models.CharField(max_length=10, default="")
    name = models.CharField(max_length=40)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)
    acknowledge_required = models.IntegerField(default=1)
    resolution_required = models.IntegerField(default=1)

    def __str__(self):
        return str(self.catid) + " - " + str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(TaskCategory, self).save(*args, **kwargs)


class TaskPriority(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=40)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(TaskPriority, self).save(*args, **kwargs)


class TaskVarType(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=20)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(TaskVarType, self).save(*args, **kwargs)


class TaskVarCategory(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=20)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(TaskVarCategory, self).save(*args, **kwargs)


class Playbook(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50, default="", blank=False, null=False)
    version = models.CharField(max_length=20, default="", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="playbook_users")
    inv = models.ForeignKey(Inv, on_delete=models.CASCADE, default=None, null=True, blank=True,
                            related_name="playbook_inv")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")

    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.pk)+" - "+str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(Playbook, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "tasks:play_detail",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        # if self.prev :
        #     raise ValidationError(_('You must select a Task.'+str(self.next)))
        pass


def new_playbook(pplaybooktemplate, pname, pversion, puser, pinv, pdescription, pmodified_by, pcreated_by):

    playbook_obj = Playbook.objects.create(
        name=pname,
        version=pversion,
        user=puser,
        inv=pinv,
        description=pdescription,
        modified_by=pmodified_by,
        created_by=pcreated_by,
    )
    item_mapping = dict()
    for tmp_item in pplaybooktemplate.playbooktemplateitem_playbooktemplate.all().order_by('itemorder'):
        tmp_to_copy = TaskTemplate.objects.get(pk=tmp_item.acttask.pk)
        # if the playbooktemplateitem refers to a previous item, we need to
        # find the pk of the newly created previous item matching the previous reference
        if tmp_item.prevtask:
            tmp_item_prevtaskpk = TaskTemplate.objects.get(pk=tmp_item.prevtask.pk).pk
            # print(str(tmp_item.pk)+"->"+str(tmp_item_prevtaskpk))
            tmp_item_prevtask = Task.objects.get(pk=item_mapping[tmp_item_prevtaskpk])
            # print(tmp_item_prevtask)
        else:
            tmp_item_prevtask = None
        # if tmp_item.prevtask:
        #     tmp_item_prevtask=TaskTemplate.objects.get(pk=tmp_item.prevtask.pk)
        # else:
        #     tmp_item_prevtask = None
        # tmp_item_prevtask = None
        new_task = add_task_from_template(
            atitle=tmp_to_copy.title,
            astatus=tmp_to_copy.status,
            aplaybook=playbook_obj,
            auser=tmp_to_copy.user,
            ainv=pinv,
            aaction=tmp_to_copy.action,
            aactiontarget=tmp_item_prevtask,
            acategory=tmp_to_copy.category,
            apriority=tmp_to_copy.priority,
            atype=tmp_to_copy.type,
            asummary=tmp_to_copy.summary,
            adescription=tmp_to_copy.description,
            amodified_by=str(puser),
            acreated_by=str(puser)
        )
        # print(str(new_task)+"->->"+str(tmp_item_prevtask))
        #  here I need to map the tampate pks to the new pks so I can assign the proper actions
        item_mapping.update({tmp_item.pk: new_task.pk})
    return playbook_obj

# Create your models here.
class Task(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="task_users")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="task_parent")
    inputfrom = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name="task_inputfrom")
    inv = models.ForeignKey(Inv, on_delete=models.CASCADE, null=True, blank=True, related_name="task_inv")
    #  this is circular reference...could cause issues...lazy relationship
    action = models.ForeignKey('tasks.Action', on_delete=models.SET_NULL, default=None, null=True, blank=True,
                               related_name="task_action")
    actiontarget = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="task_actiontarget")
    playbook = models.ForeignKey(Playbook, on_delete=models.CASCADE, default=None, null=True, blank=True,
                                 related_name="task_playbook")
    # playbookid = models.PositiveIntegerField(default=None, null=True, blank=True)
    # playbookname = models.CharField(max_length=50, default="", blank=True, null=True)
    title = models.CharField(max_length=50, blank=False, null=False)
    status = models.ForeignKey(TaskStatus, on_delete=models.SET_DEFAULT, default="1", related_name="task_status")
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_DEFAULT, default="1", related_name="task_category")
    priority = models.ForeignKey(TaskPriority, on_delete=models.SET_NULL, null=True, default=None,
                                 related_name="task_priority")
    type = models.ForeignKey(TaskType, on_delete=models.SET_DEFAULT, default="1", related_name="task_type")
    description = HTMLField()
    description_html = models.TextField(editable=True, default='', blank=True)
    summary = models.CharField(max_length=2000, default="", blank=True, null=True)
    starttime = models.DateTimeField(auto_now=False, blank=True, null=True)
    endtime = models.DateTimeField(auto_now=False, blank=True, null=True)
    taskduration = models.PositiveIntegerField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")

    # check if the status has been changed
    __original_status = None

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.__original_status = self.status

    # result = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return str(self.pk)+" - "+str(self.title)

    # def save(self, *args, **kwargs):
    #     self.description_html = misaka.html(self.description)
    #     super(Task, self).save(*args, **kwargs)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        #  this is to check if the status record has been changed or not
        if self.status != self.__original_status:
            if self.status.name == "Completed":
                # status changed do something here
                # print("completed"+str(self.status))
                if Task.objects.filter(actiontarget=self.pk).exists():
                    #  exclude tasks that are already completed (pk=2)
                    targettasks = Task.objects.filter(actiontarget=self.pk).exclude(status=2).order_by('pk')
                    for targettask in targettasks:
                        targettaskactionpk = int()
                        if targettask.type.pk == 1:
                            #  this means there is a task which relies on this and is automated task
                            #  we need to run the task referred
                            #  will have to run on all related tasks, so using filter instead of get
                            targettaskpk = targettask.pk
                            targettaskactionpk = targettask.action.pk
                            targettaskinvpk = targettask.inv.pk
                            # targettaskactiontarget = targettask.actiontarget.pk
                            #  here we need to find the proper evidence...
                            sourcetask = Task.objects.get(pk=self.pk)
                            evid = sourcetask.evidence_task.all()
                            evattrs = None
                            # # here we will need a nested for loop
                            if TaskVar.objects.filter(task=sourcetask, name='ActionTarget', category=2).exists():
                                taskvar_obj = TaskVar.objects.get(task=sourcetask, name='ActionTarget', category=2)
                                taskvar_value = taskvar_obj.value
                                # print(taskvar_value)
                                if taskvar_value == 'first' or taskvar_value == "" and Task.objects.filter(pk=evid.first().pk).exists():
                                    evidpk = evid.first().pk
                                elif taskvar_value == 'last':
                                    evidpk = evid.last().pk
                                elif int(taskvar_value):
                                    evidpk = int(taskvar_value)
                                else:
                                    evidpk = evid.first().pk
                            else:
                                evidpk = evid.first().pk  #Task.objects.get(pk=evid.first().pk)

                            # checking for a list of all attributes which match the attribute filter in the action
                            evidobj = Evidence.objects.get(pk=evidpk)
                            curraction = Action.objects.get(pk=targettaskactionpk)
                            filterforpk = None
                            evidattrs = None
                            if curraction.scriptinputattrtypeall and curraction.scriptinput.name == 'Attribute':
                                evidattrs = evidobj.evattr_evidence.all()
                            elif not curraction.scriptinputattrtypeall and curraction.scriptinput.name == 'Attribute':
                                filterforpk = curraction.scriptinputattrtype
                                evidattrs = evidobj.evattr_evidence.filter(evattrformat=filterforpk)
                            if evidattrs:
                                for evidattr1 in evidattrs:
                                    # print("AUTOMATED: "+str(targettaskactionpk)+":"+str(targettaskinvpk)+":"+str(targettaskpk)+":"+str(evidpk))
                                    #  Call the function that has to be executed upon close
                                    run_action(
                                        pactuser=self.user,
                                        pactusername="action",
                                        pev_pk=evidpk,
                                        pevattr_pk=evidattr1.pk,
                                        ptask_pk=targettaskpk,
                                        pact_pk=targettaskactionpk,
                                        pinv_pk=targettaskinvpk,
                                        pargdyn='',
                                        pattr=''
                                    )
                            else:
                                # print("AUTOMATED: "+str(targettaskactionpk)+":"+str(targettaskinvpk)+":"+str(targettaskpk)+":"+str(evidpk))
                                #  Call the function that has to be executed upon close
                                run_action(
                                    pactuser=self.user,
                                    pactusername="action",
                                    pev_pk=evidpk,
                                    pevattr_pk=None,
                                    ptask_pk=targettaskpk,
                                    pact_pk=targettaskactionpk,
                                    pinv_pk=targettaskinvpk,
                                    pargdyn='',
                                    pattr=''
                                )

                        task_close(
                            ptaskpk=targettaskpk,
                            ptaskmoduser='action'
                        )
            # print("changed"+str(self.status))
            pass

        if self.status.name == "Completed":
            # status changed to closed
            # set investigation close date
            if self.endtime is None:
                # self.endtime = datetime.now()
                self.endtime = timezone_now()

        #  if start time is not set, set it to the investigation creation date
        if self.starttime is None:
            # self.starttime = datetime.now()
            self.starttime = timezone_now()

        if self.starttime is not None and self.endtime is not None:
            self.taskduration = timediff(self.starttime, self.endtime)
            # print(self.starttime)
            # print(self.endtime)
        else:
            self.taskduration = None
        self.description_html = misaka.html(self.description)

        # updating inv time
        if self.inv:
            if self.modified_by is None:
                pmodified_by='admin'
            else:
                pmodified_by=str(self.modified_by)
            Inv.objects.filter(pk=self.inv.pk).update(modified_at=timezone_now(), modified_by=pmodified_by)

        super(Task, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_status = self.status

    def taskdurationprint(self):
        if self.taskduration:
            tduration = self.taskduration
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
            "tasks:tsk_detail",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    @property
    def actev(self):
        """
        Returns the evidence to run the script on
        The TaskVar "ActionTarget" value should be set to:
        -"first" to use the first evidence in the task
        -"last" to use the last evidence in the task
        -"x" where x refers to the evidence ID in the Task
        Default is the first, if not defined.

        """
        try:
            if TaskVar.objects.filter(task=self.pk, name='ActionTarget', category=2):
                taskvar_obj = TaskVar.objects.filter(task=self.pk, name='ActionTarget', category=2)
                taskvar_value = taskvar_obj[0].value
                if taskvar_value == 'first' or taskvar_value == "":
                    retval = Task.objects.get(pk=self.actiontarget.pk).evidence_task.first()
                elif taskvar_value == 'last':
                    retval = Task.objects.get(pk=self.actiontarget.pk).evidence_task.last()
                else:
                    retval = int(taskvar_value)
            else:
                retval = Task.objects.get(pk=self.actiontarget.pk).evidence_task.first()
        except:
            retval = None
        return retval

    def clean(self):
        pass


def task_close(ptaskpk, ptaskmoduser):
    if Task.objects.filter(pk=ptaskpk).exists():
        task_obj = Task.objects.get(pk=ptaskpk)
        taskstatusclose = TaskStatus.objects.get(name="Completed")
        taskduration = None
        if task_obj.starttime is not None and task_obj.endtime is not None:
            task_obj.taskduration = timediff(task_obj.starttime, task_obj.endtime)
        else:
            task_obj.taskduration = None
        # task_obj.update(status=taskstatusclose, modified_by=ptaskmoduser, taskduration=taskduration)
        task_obj.status = taskstatusclose
        task_obj.modified_by = ptaskmoduser
        task_obj.taskduration = taskduration
        task_obj.save()


class EvidenceFormat(models.Model):
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
        super(EvidenceFormat, self).save(*args, **kwargs)


class Evidence(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="evidence_users")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, related_name="evidence_task")
    inv = models.ForeignKey(Inv, on_delete=models.CASCADE, null=True, blank=True, related_name="evidence_inv")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="evidence_parent")
    parentattr = models.ForeignKey('EvidenceAttr', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="evidence_parentattr")
    prevev = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="evidence_prevev")

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    evidenceformat = models.ForeignKey(EvidenceFormat, on_delete=models.SET_DEFAULT, default=1, null=False, blank=False,
                                       related_name="evidence_evidenceformat")
    mitretactic = models.ForeignKey(MitreAttck_Tactics, on_delete=models.SET_DEFAULT, default=1, null=False, blank=False,
                                       related_name="evidence_mitretactic")

    description = HTMLField()
    fileName = models.CharField(max_length=255, default="", null=True, blank=True)
    fileRef = models.FileField(upload_to=upload_to_evidence, null=True, blank=True)
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
                super(Evidence, self).save(*args, **kwargs)
                self.fileRef = file_to_save
            # kwargs.pop('force_insert')
        if self.inv:
            Inv.objects.filter(pk=self.inv.pk).update(modified_at=timezone_now(), modified_by=self.modified_by)
        if self.task:
            Task.objects.filter(pk=self.task.pk).update(modified_at=timezone_now(), modified_by=self.modified_by)

        super(Evidence, self).save(*args, **kwargs)

    def clean(self):
        if self.inv is None and self.task is None:
            raise ValidationError(_('You must select an Investigation or a Task.'))
        if self.task and Task.objects.filter(pk=self.task.pk).exists:
            if Task.objects.get(pk=self.task.pk).status.name == "Completed" or \
                 Task.objects.get(pk=self.task.pk).status.name == "Skipped":
                raise ValidationError(_('Task cannot be closed!'))
        if self.inv and Inv.objects.filter(pk=self.inv.pk).exists():
            if Inv.objects.get(pk=self.inv.pk).status.name == "Closed" or \
                Inv.objects.get(pk=self.inv.pk).status.name == "Archived":
                raise ValidationError(_('Investigation cannot be closed!'))
        super(Evidence, self).clean()


class EvidenceAttrFormat(models.Model):
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
        super(EvidenceAttrFormat, self).save(*args, **kwargs)


class EvReputation(models.Model):
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(EvReputation, self).save(*args, **kwargs)


class EvidenceAttr(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="evattr_users")
    ev = models.ForeignKey(Evidence, on_delete=models.CASCADE, null=True, blank=True, related_name="evattr_evidence")
    evattrvalue = models.CharField(max_length=2048)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    evattrformat = models.ForeignKey(EvidenceAttrFormat, on_delete=models.SET_DEFAULT, default=1, null=False,
                                     blank=False, related_name="evattr_evidenceattrformat")
    attr_automatic = models.BooleanField(default=None, null=True, blank=True)
    attr_reputation = models.ForeignKey(EvReputation, on_delete=models.SET_NULL, null=True, blank=True, related_name="evattr_evreputation")

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse(
            "tasks:evattr_detail",
            kwargs={
                # "username": self.user.username,
                # "inv_pk": '3',
                # "task_pk": '3',
                "pk": self.pk
            })

    def save(self, *args, **kwargs):
        if self.ev:
            Evidence.objects.filter(pk=self.ev.pk).update(modified_at=timezone_now(), modified_by=self.modified_by)
            if Evidence.objects.get(pk=self.ev.pk).task:
                task_pk = Evidence.objects.get(pk=self.ev.pk).task.pk
                Task.objects.filter(pk=task_pk).update(modified_at=timezone_now(), modified_by=self.modified_by)
            if Evidence.objects.get(pk=self.ev.pk).inv:
                inv_pk = Evidence.objects.get(pk=self.ev.pk).inv.pk
                Inv.objects.filter(pk=inv_pk).update(modified_at=timezone_now(), modified_by=self.modified_by)
        super(EvidenceAttr, self).save(*args, **kwargs)

    def clean(self):
        # if self.inv is None and self.task is None:
        #     raise ValidationError(_('You must select an Investigation or a Task.'))
        pass


class ExtractAttr():
    '''
    This class holds the data extractor functions
    pselector selects which data source to use
    '''

    def __init__(self, pevidence, puser, pusername, pevattr=None, pselector=1):
        self.currev = Evidence.objects.get(pk=pevidence)
        self.curruser = puser
        self.currusername = pusername
        if pevattr:
            self.currattr = EvidenceAttr.objects.get(pk=pevattr)
        self.pfile = None
        self.pselector = pselector

    def find_ipv4(self, str1):
        ipattern = re.compile(
            '(?:(?:1\d\d|2[0-5][0-5]|2[0-4]\d|0?[1-9]\d|0?0?\d)\.){3}(?:1\d\d|2[0-5][0-5]|2[0-4]\d|0?[1-9]\d|0?0?\d)')
        imatches = re.findall(ipattern, str1)
        imatches = sorted(list(set(imatches)))
        return imatches

    def find_ipv6(self, str1):
        ipattern = re.compile('(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}')
        imatches = re.findall(ipattern, str1)
        imatches = sorted(list(set(imatches)))
        return imatches

    def ip_check(self, address):
        try:
            ipver = ipaddress.ip_address(address)
            return ipver
        except:
            return False

    def find_email(self, str1):
        #  ipattern = re.compile('([^[({@|\s]+@[^@]+\.[^])}@|\s]+)')
        ipattern = re.compile('([^@":[>|<\s]+@[^@]+\.[^]>"<)\}@|\s]+)')
        imatches = re.findall(ipattern, str1)
        imatches = sorted(list(set(imatches)))
        return imatches

    def extract_ip(self):
        ip4 = None
        ip6 = None
        if self.pselector == 1:
            #  run on the evidence description
            ip4 = self.find_ipv4(self.currev.description)
            ip6 = self.find_ipv6(self.currev.description)
            pass
        elif self.pselector == 2:
            #  run on the attribute
            ip4 = self.find_ipv4(self.currattr.evattrvalue)
            ip6 = self.find_ipv6(self.currattr.evattrvalue)
            pass
        elif self.pselector == 3:
            #  run on the file attachment
            # print("file")
            pass
        # add_evattr(self, self.pevidence, self.pattr, self.pfile, 2, 1, 1)
        for oneip in ip4:
            currevattrformat = EvidenceAttrFormat.objects.get(name="IPv4")
            ip4 = ipaddress.ip_address(oneip)
            add_evattr(self.curruser, self.currev, ip4, currevattrformat, self.currusername, self.currusername)
        for oneip in ip6:
            currevattrformat = EvidenceAttrFormat.objects.get(name="IPv6")
            ip6 = ipaddress.ip_address(oneip)
            add_evattr(self.curruser, self.currev, ip6, currevattrformat, self.currusername, self.currusername)
        # add_evattr(auser, aev, aevattrvalue, aevattrformat, amodified_by, acreated_by):

    def extract_email(self):
        emails = []
        if self.pselector == 1:
            #  run on the evidence description
            emails = self.find_email(self.currev.description)
        elif self.pselector == 2:
            #  run on the attribute
            emails = self.find_email(self.currattr.evattrvalue)
        elif self.pselector == 3:
            #  run on the file attachment
            # print("file")
            pass
        for onemail in emails:
            currevattrformat = EvidenceAttrFormat.objects.get(name="Email")
            add_evattr(self.curruser, self.currev, onemail, currevattrformat, self.currusername, self.currusername)

    def extract_all(self):
        self.extract_email()
        self.extract_ip()

    def print_value(self):
        if self.pselector == 1:
            #  run on the evidence description
            print(self.currev.description)
        elif self.pselector == 2:
            #  run on the attribute
            print(self.currattr.evattrvalue)
            print(self.currattr.ev.pk)
        elif self.pselector == 3:
            #  run on the file attachment
            # print("file")
            pass

        return self.currev.description

    def print_res(self):
        pass


class ScriptOs(models.Model):
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=20)
    version = models.CharField(max_length=20, default=None, null=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.name)+" "+str(self.version)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(ScriptOs, self).save(*args, **kwargs)


class ScriptCategory(models.Model):
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(ScriptCategory, self).save(*args, **kwargs)


class ScriptType(models.Model):
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=20)
    version = models.CharField(max_length=20, default=None, null=True)
    os = models.ForeignKey(ScriptOs, on_delete=models.SET_DEFAULT, default='1', blank=False, null=False,
                           related_name="scripttype_scriptos")
    interpreter = models.CharField(max_length=255, default=None, null=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.name)+" "+str(self.version)+" "+str(self.os)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(ScriptType, self).save(*args, **kwargs)


class ScriptOutput(models.Model):
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=20)
    delimiter = models.CharField(max_length=10, default="", blank=True, null=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(ScriptOutput, self).save(*args, **kwargs)


class ScriptInput(models.Model):
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=20)
    shortname = models.CharField(max_length=4, default="")
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(ScriptInput, self).save(*args, **kwargs)


class Type(models.Model):
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(Type, self).save(*args, **kwargs)


class OutputTarget(models.Model):
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=15)
    shortname = models.CharField(max_length=4, default="")
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)
    #  to satisfy pyCharm

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(OutputTarget, self).save(*args, **kwargs)


def save_code(logfile, script_code):
    try:
        code_field = script_code
    except Exception as err:
        code_field += str(err)
    finally:
        try:
            with open(logfile, 'w') as f:
                #  replace newlines as the HTML will likely contain those...in windows format
                newdata = code_field.replace("\r\n", "\n")
                f.write(newdata)
                return 1
        except Exception as e:
            return 0


class Action(models.Model):
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="action_users")
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, blank=False, null=True, related_name="action_type")
    title = models.CharField(max_length=50, blank=False, null=False)
    version = models.CharField(max_length=20, default=None, null=True)
    script_type = models.ForeignKey(ScriptType, on_delete=models.SET_DEFAULT, default='1', blank=False, null=False,
                                    related_name="action_scripttype")
    script_category = models.ForeignKey(ScriptCategory, on_delete=models.SET_DEFAULT, default='1', blank=False,
                                        null=False, related_name="action_scriptcategory")
    scriptoutput = models.ForeignKey(ScriptOutput, on_delete=models.SET_NULL, default='1', blank=False, null=True,
                                     related_name="action_scriptoutput")
    scriptoutputtype = models.ForeignKey(EvidenceAttrFormat, on_delete=models.SET_NULL, default='1', blank=True, null=True,
                                         related_name="action_scriptoutputtype")
    scriptinput = models.ForeignKey(ScriptInput, on_delete=models.SET_NULL, default='1', blank=False, null=True,
                                     related_name="action_scriptinput")
    scriptinputattrtype = models.ForeignKey(EvidenceAttrFormat, on_delete=models.SET_NULL, default=None, blank=True,
                                       null=True, related_name="action_scriptinputattrtype")
    scriptinputattrtypeall = models.BooleanField(default=False)
    outputtarget = models.ForeignKey(OutputTarget, on_delete=models.SET_DEFAULT, default=1, blank=True, null=True,
                                     related_name="action_outputtarget")
    outputdescformat = models.ForeignKey(EvidenceFormat, on_delete=models.SET_DEFAULT, default=1, blank=True, null=True,
                                     related_name="action_outputdescformat")
    argument = models.CharField(max_length=2048, default=None, blank=True, null=True)
    timeout = models.PositiveIntegerField(default=300, null=False, blank=False)
    #  300 seconds
    code = models.TextField(editable=True, default='', blank=True)
    code_file = models.BooleanField(default=False)
    code_file_path = models.CharField(max_length=255, default=None, blank=True, null=True)
    code_file_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    fileName = models.CharField(max_length=255, default="", null=True, blank=True)
    fileRef = models.FileField(upload_to=upload_to_action, null=True, blank=True)
    filecreated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    description = HTMLField()
    description_html = models.TextField(editable=True, default='', blank=True)


    #    class Meta:
    #        ordering = ['-id']

    # class Meta:
#       ordering = ['-id']
    #  to satisfy pyCharm

    def __str__(self):
        return str(self.title)+" ("+str(self.scriptinput.shortname)+"->"+str(self.outputtarget.shortname)+")"

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)

        savepath = os.path.join(PROJECT_ROOT, 'tasks', 'actions', str(self.pk))
        pathlib.Path(savepath).mkdir(parents=True, exist_ok=True)
        filename = str(self.pk)+'_'+str(datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S'))
        self.code_file_name = filename
        savefile = os.path.join(PROJECT_ROOT, 'tasks', 'actions', str(self.pk), filename)
        self.code_file_path = savefile

        saved = save_code(savefile, self.code)
        if saved:
            self.code_file = True
        else:
            self.code_file = False

        super(Action, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "tasks:ev_detail",
            kwargs={
                # "username": self.user.username,
                # "inv_pk": '3',
                # "task_pk": '3',
                "pk": self.pk
            })

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if (self.fileRef == "") and (self.code == ""):
            # raise ValidationError(_('You must define Code or upload a script.'))
            raise ValidationError(_("You must either define Code or upload a script file!"))
        pass


class ActionGroup(models.Model):
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(ActionGroup, self).save(*args, **kwargs)


class ActionGroupMember(models.Model):
    objects = models.Manager()
    actionid = models.ForeignKey(Action, on_delete=models.CASCADE, blank=False, null=False,
                                    related_name="actiongroupmember_action")
    actiongroupid = models.ForeignKey(ActionGroup, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                    related_name="actiongroupmember_actiongroup")
    def __str__(self):
        return str(self.actionid)


class TaskTemplate(models.Model):
    objects = models.Manager()
    tasktemplatename = models.CharField(max_length=50, blank=False, null=False)
    enabled = models.BooleanField(default=True)
    # fields from Task model
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name="tasktemplate_users")
    title = models.CharField(max_length=50, blank=False, null=False)
    status = models.ForeignKey(TaskStatus, on_delete=models.SET_DEFAULT, default="1",
                               related_name="tasktemplate_status")
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_DEFAULT, default="1",
                                 related_name="tasktemplate_category")
    priority = models.ForeignKey(TaskPriority, on_delete=models.SET_NULL, null=True, default=None,
                                 related_name="tasktemplate_priority")
    type = models.ForeignKey(TaskType, on_delete=models.SET_DEFAULT, default="1",
                             related_name="tasktemplate_type")
    action = models.ForeignKey(Action, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                               related_name="tasktemplate_action")
    actiontarget = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="tasktemplate_actiontarget")
    description = HTMLField()
    description_html = models.TextField(editable=True, default='', blank=True)
    summary = models.CharField(max_length=2000, default="", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")

    # result = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return str(self.category) + " - " + str(self.title)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(TaskTemplate, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "tasks:tmp_detail",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    def clean(self):
        pass
        # Don't allow draft entries to have a pub_date.
        # if self.taskid == '':
        #     raise ValidationError(_('You must enter an Investigation ID.'))


class TaskVar(models.Model):
    objects = models.Manager()
    category = models.ForeignKey(TaskVarCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="taskvar_taskvarcategory")
    type = models.ForeignKey(TaskVarType, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name="taskvar_taskvartype")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, related_name="taskvar_task")
    tasktemplate = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="taskvar_tasktemplate")

    name = models.CharField(max_length=20)
    value = models.TextField(null=True, blank=True, default=None)
    required = models.BooleanField(default=True)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def displaytasktemplate(self):
        return str(self.tasktemplate)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(TaskVar, self).save(*args, **kwargs)

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if (self.task is None and self.tasktemplate is None) \
                or \
                (self.task is not None and self.tasktemplate is not None):
            raise ValidationError(_('You must select either a Task or a Task Template. Only one of them!'))
        super(TaskVar, self).clean()
        
        
class PlaybookTemplate(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50, default="", blank=False, null=False)
    enabled = models.BooleanField(default=True)
    version = models.CharField(max_length=20, default="", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="playbooktemplate_users")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")

    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.pk)+" - "+str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(PlaybookTemplate, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "tasks:playtmp_detail",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        # if self.prev :
        #     raise ValidationError(_('You must select a Task.'+str(self.next)))
        pass


class PlaybookTemplateItem(models.Model):
    objects = models.Manager()
    playbooktemplateid = models.ForeignKey(PlaybookTemplate, on_delete=models.CASCADE, null=False, blank=False,
                                           related_name="playbooktemplateitem_playbooktemplate")
    enabled = models.BooleanField(default=True)
    acttask = models.ForeignKey(TaskTemplate, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="playbooktemplateitem_tasktemplate_act")
    nexttask = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="playbooktemplateitem_playbooktemplateitem_next")
    prevtask = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="playbooktemplateitem_playbooktemplateitem_prev")
    itemorder = models.SmallIntegerField(default=0, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="playbooktemplateitem_users")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")

    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.pk)+" - "+str(self.acttask.title)

    def get_absolute_url(self):
        return reverse(
            "tasks:playtmp_detail",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(PlaybookTemplateItem, self).save(*args, **kwargs)

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if not self.acttask:
            raise ValidationError(_('You must select an actual Task.'))
        if self.prevtask == self.nexttask and self.prevtask is not None:
            raise ValidationError(_('Previous and Next tasks cannot be the same.'))
        pass

# #### PROCEDURES


def add_task_from_template(atitle, astatus, aplaybook, auser, ainv, aaction, aactiontarget,
                           acategory, apriority, atype, asummary, adescription,
                           amodified_by, acreated_by):
    obj = Task.objects.create(
        title=atitle,
        status=astatus,
        playbook=aplaybook,
        user=auser,
        inv=ainv,
        action=aaction,
        actiontarget=aactiontarget,
        category=acategory,
        priority=apriority,
        type=atype,
        summary=asummary,
        description=adescription,
        modified_by=amodified_by,
        created_by=acreated_by,
    )
    return obj


def new_evidence(puser, ptask, pinv, pcreated_by, pmodified_by, pdescription, pfilename=None, pfileref=None,
                 pevformat=None, pforce=False, pparent=None, pparentattr=None):
    newev = None
    if pevformat is None:
        pevformat = EvidenceFormat.objects.get(pk=1)
    if pforce is False:
        newev = Evidence.objects.update_or_create(
            user=puser,
            task=ptask,
            inv=pinv,
            created_by=pcreated_by,
            modified_by=pmodified_by,
            description=pdescription,
            evidenceformat=pevformat,
            parent=pparent,
            parentattr=pparentattr,
            # fileName=pfilename,
            # fileRef=pfileref
        )
        # Saving the file attachments
        if pfilename and pfileref:
            newev[0].fileName=pfilename
            newev[0].fileRef.save(pfilename, pfileref)
            # chunked upload
            # save_relpath = upload_to_evidence(evidence_obj, cfileref.name)
            # save_path = path.join(MYMEDIA_ROOT, str(save_relpath))
            # handle_uploaded_file_chunks(cfileref , save_path)
            # evidence_obj.fileRef=save_relpath
            # evidence_obj.fileName=cfileref.name
            # evidence_obj.save()

        newev = newev[0]
    else:
        newev = Evidence.objects.create(
            user=puser,
            task=ptask,
            inv=pinv,
            created_by=pcreated_by,
            modified_by=pmodified_by,
            description=pdescription,
            evidenceformat=pevformat,
            parent=pparent,
            parentattr=pparentattr,
            # fileName=pfilename,
            # fileRef=pfileref
        )
        # Saving the file attachments
        if pfilename and pfileref:
            newev.fileName = pfilename
            newev.fileRef.save(pfilename, pfileref)
    return newev


def add_evattr(auser, aev, aevattrvalue, aevattrformat, amodified_by, acreated_by, aattr_reputation=None,
               aattr_automatic=None, aforce=False):
    newevattr = None
    if aforce is False:
        new_evattr = EvidenceAttr.objects.update_or_create(
            user=auser,
            ev=aev,
            evattrvalue=aevattrvalue,
            evattrformat=aevattrformat,
            modified_by=amodified_by,
            created_by=acreated_by,
            attr_reputation=aattr_reputation,
            attr_automatic=aattr_automatic,
        )
        new_evattr = new_evattr[0]
    else:
        new_evattr = EvidenceAttr.objects.create(
            user=auser,
            ev=aev,
            evattrvalue=aevattrvalue,
            evattrformat=aevattrformat,
            modified_by=amodified_by,
            created_by=acreated_by,
            attr_reputation=aattr_reputation,
            attr_automatic=aattr_automatic,
        )
    return new_evattr

# Replace/delete files
@receiver(models.signals.post_delete, sender=Evidence)
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


@receiver(models.signals.post_save, sender=Evidence)
def auto_make_readonly(sender, instance, **kwargs):
    """
    Make evidences read-only on the filesystem
    """
    if instance.fileRef:
        if os.path.isfile(instance.fileRef.path):
            #  This makes the files readonly
            os.chmod(instance.fileRef.path, S_IREAD | S_IRGRP | S_IROTH)

            # this one calculates the hash for the file
            res_md5 = FileHashCalc().md5sum(instance.fileRef.path)
            add_evattr(
                auser=instance.user,
                aev=Evidence.objects.get(pk=instance.pk),
                aevattrvalue=res_md5,
                aevattrformat=EvidenceAttrFormat.objects.get(pk=9),
                amodified_by=instance.user.username,
                acreated_by=instance.user.username,
                attr_automatic=True,
                aattr_reputation=None,
                aforce=False
            )
            res_sha1 = FileHashCalc().sha1sum(instance.fileRef.path)
            add_evattr(
                auser=instance.user,
                aev=Evidence.objects.get(pk=instance.pk),
                aevattrvalue=res_sha1,
                aevattrformat=EvidenceAttrFormat.objects.get(pk=10),
                amodified_by=instance.user.username,
                acreated_by=instance.user.username,
                attr_automatic=True,
                aattr_reputation=None,
                aforce=False
            )
            res_sha256 = FileHashCalc().sha256sum(instance.fileRef.path)
            add_evattr(
                auser=instance.user,
                aev=Evidence.objects.get(pk=instance.pk),
                aevattrvalue=res_sha256,
                aevattrformat=EvidenceAttrFormat.objects.get(pk=11),
                amodified_by=instance.user.username,
                acreated_by=instance.user.username,
                attr_automatic=True,
                aattr_reputation=None,
                aforce=False
            )
            res_sha512 = FileHashCalc().sha512sum(instance.fileRef.path)
            add_evattr(
                auser=instance.user,
                aev=Evidence.objects.get(pk=instance.pk),
                aevattrvalue=res_sha512,
                aevattrformat=EvidenceAttrFormat.objects.get(pk=12),
                amodified_by=instance.user.username,
                acreated_by=instance.user.username,
                attr_automatic=True,
                aattr_reputation=None,
                aforce=False
            )

@receiver(models.signals.pre_save, sender=Evidence)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `InvestigationDetails` object is changed.
    """
    if not instance.pk:
        return False

    try:
        old_file = Evidence.objects.get(pk=instance.pk).fileRef
    except Evidence.DoesNotExist:
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


class OutputProcessor():

    def __init__(self):
        pass

    def split_delimiter(self, pstring, pdelimiter):
        retval = str(pstring).split(pdelimiter)
        return retval


def remove_html_markup(s):
    tag = False
    quote = False
    out = ""
    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif (c == '"' or c == "'") and tag:
            quote = not quote
        elif not tag:
            out = out + c
    return out


def run_action(pactuser, pactusername, pev_pk, pevattr_pk, ptask_pk, pact_pk, pinv_pk, pargdyn, pattr):
    actuser = pactuser  #  self.request.user
    actusername = pactusername  # self.request.user.get_username()
    oldev_file = None
    oldev_file_name = None
    task_obj = None
    ev_pk = pev_pk
    oldev_obj = None
    oldev_id = None
    evattr_pk = None
    if pevattr_pk:
        evattr_pk = int(pevattr_pk)
    evattr_obj = None
    ismalicious = None
    if evattr_pk != 0 and evattr_pk is not None:
        evattr_obj = EvidenceAttr.objects.get(pk=evattr_pk)

    if ev_pk == '0' or ev_pk == None:
        oldev_id = None
        oldev_obj = None
    else:
        oldev_id = ev_pk
        oldev_obj = Evidence.objects.get(pk=oldev_id)
        if oldev_obj.fileRef:
            oldev_file = str(oldev_obj.fileRef)
            oldev_file_name = str(oldev_obj.fileName)
        else:
            oldev_file = None
            oldev_file_name = None

    if ptask_pk == '0' or ptask_pk == None:
        task_id = None
        task_obj = None
    else:
        task_id = ptask_pk
        task_obj = Task.objects.get(pk=task_id)
    if pact_pk != '0':
        actionid = pact_pk
    else:
        actionid = 0
    if pinv_pk == '0' or pinv_pk == None:
        inv_id = None
        inv_obj = None
    else:
        inv_id = pinv_pk
        inv_obj = Inv.objects.get(pk=inv_id)

    #  get the interpreter from the related table
    act_id = pact_pk
    action_obj = Action.objects.get(pk=act_id)
    action_outputtarget = action_obj.outputtarget.pk
    interpreter = ScriptType.objects.filter(action_scripttype__pk=act_id)[0].interpreter
    cmd = Action.objects.get(pk=act_id).code_file_path
    # actioncode = Action.objects.get(pk=act_id).code
    timeout = Action.objects.get(pk=act_id).timeout
    argumentm = str(Action.objects.get(pk=act_id).argument)
    argumentdynamic = str(pargdyn)
    # dynamic argument parameters can be submitted via POST/GET
    # argumentattr = str(pattr)
    argumentattr = evattr_pk
    #  attribute defines if the output should go to an attribute or to an evidence field
    #  argumentoutput = str(self.request.GET.get('attrout'))
    argument = ""
    if argumentdynamic != "None":
        argument = argumentm + " " + argumentdynamic
    else:
        argument = argumentm
    argument_cleartext = ""
    # this is needed to be able to display it and save it clear-text
    # 1. create temp folder
    tempfile.tempdir = path.join(MEDIA_ROOT, "tmp")
    destoutdirname = None
    mytempdir = None

    if argument != "None":
        if action_obj.scriptinput.pk == 1 or action_obj.scriptinput.pk == 3:
            # 1 represents description field as the input
            # 3 represents attribute field as the input
            desc = ""
            if action_obj.scriptinput.pk == 3 and evattr_obj and evattr_obj.evattrvalue:
                # desc = EvidenceAttr.objects.get(pk=argumentattr).evattrvalue
                desc = evattr_obj.evattrvalue
            else:
                if oldev_obj:
                    if oldev_obj.evidenceformat.pk == 1:
                        #  if it's in raw format, simply use the value
                        desc = oldev_obj.description
                    elif oldev_obj.evidenceformat.pk == 2:
                        #  if it is in HTML format, try to clean it...
                        desc = remove_html_markup(oldev_obj.description)
                    else:
                        #  if it is in an unknown format, just use it
                        desc = oldev_obj.description
            #  replace the $EVIDENCES$ with the description value
            if action_obj.type.pk == 4:
                #  b64 encrypted values
                argument_cleartext = argument.replace('$EVIDENCE$', desc)
                argument = argument.replace('$EVIDENCE$', b64encode(desc.encode()).decode())
            else:
                argument = argument.replace('$EVIDENCE$', desc)
                argument_cleartext = argument
            if action_obj.outputtarget.name == 'File':
                # this means the output is a file
                #  generate a random folder with some prefix:
                myprefix = "EV-" + str(ev_pk) + "-"
                mytempdir = tempfile.TemporaryDirectory(prefix=myprefix)
                #  make the tempdir the temp root
                tempfile.tempdir = mytempdir.name
                # with tempfile.TemporaryDirectory() as directory:
                destdir = mytempdir.name
                # argument replace the $OUTDIR$ with the standard dir where output files will be stored
                destoutdir = tempfile.mkdtemp()
                destoutdirname = str(destoutdir) + "/"
                argument = argument.replace('$OUTDIR$', destoutdirname)
        elif action_obj.scriptinput.pk == 2 and oldev_file:
            #  this represents file type so reads the file from the evidence
            #  need to have a file to work on, that's "2"
            #  create a temporary file so the original remains intact
            #  generate a random folder with some prefix:
            myprefix = "EV-"+str(ev_pk)+"-"
            mytempdir = tempfile.TemporaryDirectory(prefix=myprefix)
            #  make the tempdir the temp root
            tempfile.tempdir = mytempdir.name
            # with tempfile.TemporaryDirectory() as directory:
            # 2. copy file into temp folder
            srcfile = path.join(MEDIA_ROOT, oldev_file)
            destdir = mytempdir.name
            # destfile_clean = os.path.join(destdir, re.escape(oldev_file_name))
            # destfile = os.path.join(destdir, oldev_file_name)
            # I have used the renamed file because the Popen had issues with the special chars
            # and spaces in filenames...
            destfile = os.path.join(destdir, os.path.basename(oldev_file))
            copy(srcfile, destfile)
            # argument = argument.replace('$FILE$', path.join(MEDIA_ROOT, oldev_file))

            # argument = argument.replace('$FILE$', destfile_clean)
            argument = argument.replace('$FILE$', destfile)
            # argument replace the $OUTDIR$ with the standard dir where output files will be stored
            # destoutdir = os.path.join(destdir, "bcirtoutdir")
            destoutdir = tempfile.mkdtemp()
            destoutdirname = str(destoutdir) + "/"
            argument = argument.replace('$OUTDIR$', destoutdirname)

        cmdin = [interpreter, cmd, argument]
    else:
        cmdin = [interpreter, cmd]
    scripttype = action_obj.script_type
    actionq_startid = None
    results = ""
    if action_obj.type.pk == 1:  # Command
        # /bin/bash -c "`cat /tmp/cmd` -c3 8.8.8.8"
        # need to run as a command, later probably need to use interpreter...or something
        cmd = action_obj.code
        results = run_script_class("", cmd, argument, timeout).runcmd()
        pass
    elif action_obj.type.pk == 2:  # Executable
        pass
    elif action_obj.type.pk == 3:  # Script
        results = run_script_class(interpreter, cmd, argument, timeout).runscript()
    elif action_obj.type.pk == 4:  # Script with b64 encrypted values to pass over
        results = run_script_class(interpreter, cmd, argument, timeout).runscript()
    elif action_obj.type.pk == 5:  # Internal command
        from tasks.scripts import String_Parser
        sp1 = String_Parser.StringParser
        afuncoutput = getattr(sp1, action_obj.code)('',argument)
        if action_obj.code == "check_malicious":
            ismalicious = afuncoutput
            if action_obj.scriptinput.pk == 1:
                # description input
                # add_evattr(
                #     auser=actuser,
                #     aev=oldev_obj,
                #     aevattrvalue=afuncoutput,
                #     aevattrformat=EvidenceAttrFormat.objects.get(name='Reputation'),
                #     amodified_by=actusername,
                #     acreated_by=actusername,
                #     aattr_automatic=None
                # )
                pass
            elif action_obj.scriptinput.pk == 2:
                # file input
                pass
            elif action_obj.scriptinput.pk == 3:
                # attribute input
                # EvidenceAttr.objects.filter(pk=evattr_pk).update(attr_reputation = EvReputation.objects.get(pk=1))
                pass
        results = {"command": str(cmd), "status": "1", "error": "0", "output": afuncoutput, "pid": 1}
        # if True: # SUCCESS
        #     results = {"command": str(cmd), "status": "1", "error": "0", "output": afuncoutput, "pid": 1}
        # else: # FAIL
        #     results = {"command": str(cmd), "status": "0", "error": "1", "output": afuncoutput, "pid": 1}

        # ExtractAttr(4, self.request.user, self.request.user.get_username(), 2, 2).extract_ip()
        pass

    rescommand = results.get('command')
    reserror = results.get('error')
    resstatus = results.get('status')
    resoutput = results.get('output')
    respid = results.get('pid')
    resoutputl = None
    if action_obj.scriptoutput:
        if action_obj.scriptoutput.name == "List":
            from ast import literal_eval
            resoutput = literal_eval(resoutput)
        if action_obj.scriptoutput.delimiter:
            resoutput = OutputProcessor().split_delimiter(resoutput, action_obj.scriptoutput.delimiter)
    # save action to the actionQ

    actionq_stopid=None
    evid = None
    actq = None
    # if argumentoutput == "None":
    if action_outputtarget == 1:
        # Description is target for output
        # create the actionQ items
        actionq_startid = new_actionq(actuser, action_obj, task_obj, inv_obj, oldev_obj, None, action_obj.title,
                                      scripttype, cmdin, argument_cleartext, argumentdynamic, None, None, None, None,
                                      ActionQStatus.objects.get(name="Started"), actuser)

        actionq_stopid = new_actionq(actuser, action_obj, task_obj, inv_obj, oldev_obj, actionq_startid,
                                     action_obj.title, scripttype, rescommand, argument_cleartext, argumentdynamic,
                                     reserror, resstatus, resoutput, respid,
                                     ActionQStatus.objects.get(name="Finished"), actuser)
        # update the actionQ with the parent value
        ActionQ.objects.filter(pk=actionq_startid.pk).update(parent=actionq_stopid)

        #  Output to Description field in new evidence
        evid = new_evidence(
            puser=actuser,
            ptask=task_obj,
            pinv=inv_obj,
            pcreated_by=actusername,
            pmodified_by=actusername,
            pdescription=resoutput,
            pparent=oldev_obj,
            pparentattr=evattr_obj
        )
        # Add an attribute with reputation
        if ismalicious:
            if EvReputation.objects.get(name=ismalicious):
                attr_rep = EvReputation.objects.get(name=ismalicious)
            else:
                attr_rep = None
            evidattr = add_evattr(
                auser=actuser,
                aev=evid,
                aevattrvalue=ismalicious,
                aevattrformat=EvidenceAttrFormat.objects.get(name='Reputation'),
                amodified_by=actusername,
                acreated_by=actusername,
                aattr_reputation=attr_rep,
                aforce=False
            )
            # Creating a clone for the attribute item inspected
            if oldev_obj.parentattr:
                cloneevidattr = oldev_obj.parentattr
                cloneevidattr.pk = None
                cloneevidattr.attr_reputation = attr_rep
                newclone = cloneevidattr.save()

        ActionQ.objects.filter(pk=actionq_stopid.pk).update(evid=evid.pk)

        if oldev_obj:
            Evidence.objects.filter(pk=evid.pk).update(prevev=oldev_obj.pk)

        actq = actionq_stopid.pk
    elif action_outputtarget == 2:
        # Attribute is target for output
        # create the actionQ item
        actionq_startid = new_actionq(actuser, action_obj, task_obj, inv_obj, oldev_obj, None, action_obj.title,
                                      scripttype, cmdin, argument_cleartext, argumentdynamic, None, None, None, None,
                                      ActionQStatus.objects.get(name="Started"), actuser)
        actionq_stopid = new_actionq(actuser, action_obj, task_obj, inv_obj, oldev_obj, actionq_startid,
                                     action_obj.title, scripttype, rescommand, argument_cleartext, argumentdynamic,
                                     reserror, resstatus, resoutput, respid,
                                     ActionQStatus.objects.get(name="Finished"), actuser)
        # update the actionQ with the parent value
        ActionQ.objects.filter(pk=actionq_startid.pk).update(parent=actionq_stopid)
        #  Output to the attribute in the same evidence
        ActionQ.objects.filter(pk=actionq_stopid.pk).update(evid=oldev_obj.pk)
        if action_obj.code == 'check_malicious':
            currevattrformat = EvidenceAttrFormat.objects.get(name='Reputation')
        else:
            currevattrformat = EvidenceAttrFormat.objects.get(name='Unknown')
            if action_obj.scriptoutputtype:
                currevattrformat = EvidenceAttrFormat.objects.get(pk=action_obj.scriptoutputtype.pk)

        # if EvidenceAttrFormat.objects.get(name=argumentoutput):
        #     currevattrformat = EvidenceAttrFormat.objects.get(name=argumentoutput)
        # resoutput.split()
        # OUTPUT DELIMITER needs to be defined in the model - if empty, don't split...TBD
        if isinstance(resoutput,list) or isinstance(resoutput,tuple):
            # list type output
            for item1 in resoutput:
                attr_rep = None
                if ismalicious:
                    if EvReputation.objects.get(name=ismalicious):
                        attr_rep = EvReputation.objects.get(name=ismalicious)
                    else:
                        attr_rep = None
                add_evattr(
                    auser=actuser,
                    aev=oldev_obj,
                    aevattrvalue=item1,
                    aevattrformat=currevattrformat,
                    amodified_by=actusername,
                    acreated_by=actusername,
                    aattr_reputation=attr_rep,
                    aforce=False
                )
                # Creating a clone for the attribute item inspected
                if oldev_obj.parentattr:
                    cloneevidattr = oldev_obj.parentattr
                    cloneevidattr.pk = None
                    cloneevidattr.attr_reputation = attr_rep
                    newclone = cloneevidattr.save()


        elif (isinstance(resoutput,str)):
            for item1 in resoutput.splitlines():
                # add_evattr(actuser, oldev_obj, item1, currevattrformat, actusername, actusername)
                attr_rep = None
                if ismalicious:
                    if EvReputation.objects.get(name=ismalicious):
                        attr_rep = EvReputation.objects.get(name=ismalicious)
                    else:
                        attr_rep = None
                add_evattr(
                    auser=actuser,
                    aev=oldev_obj,
                    aevattrvalue=item1,
                    aevattrformat=currevattrformat,
                    amodified_by=actusername,
                    acreated_by=actusername,
                    aattr_reputation=attr_rep,
                    aforce=False
                )

                # Creating a clone for the attribute item inspected
                if oldev_obj.parentattr:
                    cloneevidattr = oldev_obj.parentattr
                    cloneevidattr.pk = None
                    cloneevidattr.attr_reputation = attr_rep
                    newclone = cloneevidattr.save()

        actq = actionq_stopid.pk
    elif action_outputtarget == 3:
        # File attachment is target for output
        # list of files to be saved
        outputfiles = os.listdir(destoutdirname)
        if outputfiles:
            for fname in outputfiles:
                actionq_startid = new_actionq(actuser, action_obj, task_obj, inv_obj, oldev_obj, None, action_obj.title,
                                              scripttype, cmdin, argument_cleartext, argumentdynamic, None, None, None,
                                              None,
                                              ActionQStatus.objects.get(name="Started"), actuser)
                # create the actionQ item
                actionq_stopid = new_actionq(actuser, action_obj, task_obj, inv_obj, oldev_obj, actionq_startid,
                                             action_obj.title, scripttype, rescommand, argument_cleartext, argumentdynamic,
                                             reserror, resstatus, resoutput, respid,
                                             ActionQStatus.objects.get(name="Finished"), actuser)
                # update the actionQ with the parent value
                ActionQ.objects.filter(pk=actionq_startid.pk).update(parent=actionq_stopid)

                # copy files to the evidences folder
                evfolder = 'uploads/evidences'
                srcfilename1 = os.path.join(destoutdirname,fname)
                dstfilename1 = os.path.join(MEDIA_ROOT, evfolder, fname)
                # if os.path.isfile(srcfilename1):
                #     copy(srcfilename1, dstfilename1)
                # copy(srcfilename1,dstfilename1)
                from django.core.files import File
                # dstfileref = os.path.join(evfolder,fname)
                dstfileref = File(open(srcfilename1, 'rb'))
                olddesc = "Automatic file output from evidence: "+str(oldev_obj.pk)
                evfid = new_evidence(
                    puser=actuser,
                    ptask=task_obj,
                    pinv=inv_obj,
                    pcreated_by=actusername,
                    pmodified_by=actusername,
                    pdescription=olddesc,
                    pforce=True,
                    pparent=oldev_obj,
                    pevformat=EvidenceFormat.objects.get(pk=2),
                    pparentattr=evattr_obj
                    # pfilename=fname,
                    # pfileref=dstfileref
                )
                if ismalicious:
                    if EvReputation.objects.get(name=ismalicious):
                        attr_rep = EvReputation.objects.get(name=ismalicious)
                    else:
                        attr_rep = None
                    evfidattr = add_evattr(
                        auser=actuser,
                        aev=evfid,
                        aevattrvalue=ismalicious,
                        aevattrformat=EvidenceAttrFormat.objects.get(name='Reputation'),
                        amodified_by=actusername,
                        acreated_by=actusername,
                        aattr_reputation=attr_rep,
                        aforce=False
                    )
                    # Creating a clone for the attribute item inspected
                    if oldev_obj.parentattr:
                        cloneevidattr = oldev_obj.parentattr
                        cloneevidattr.pk = None
                        cloneevidattr.attr_reputation = attr_rep
                        newclone = cloneevidattr.save()

                # EvidenceAttr.objects.filter(pk=evfidattr).update(attr_reputation=EvidenceAttrFormat.objects.get(name=ismalicious))
                evfid.fileRef.save(fname, dstfileref)
                Evidence.objects.filter(pk=evfid.pk).update(fileName=fname)

                imgurl1 = str(Evidence.objects.get(pk=evfid.pk).fileRef)
                imgpath = str(os.path.join("../../../../media/", imgurl1))
                # Check if the uploaded file is an image and put it in the description
                if check_file_type(os.path.join(MEDIA_ROOT,imgurl1)) == 'image':
                    imgtag = '<p><img src="'+imgpath+'" alt="'+fname+'" width="1024" height="768" border="2" /></p>'
                    newdesc = olddesc + "<br>" + imgtag
                    Evidence.objects.filter(pk=evfid.pk).update(description=newdesc)
                if os.path.isfile(dstfilename1):
                    #  This makes the files readonly
                    os.chmod(dstfilename1, S_IREAD | S_IRGRP | S_IROTH)
                # manage the actionQ
                ActionQ.objects.filter(pk=actionq_stopid.pk).update(evid=evfid.pk)

                if oldev_obj:
                    Evidence.objects.filter(pk=evfid.pk).update(prevev=oldev_obj.pk)

                actq = actionq_stopid.pk
        else:
            actionq_startid = new_actionq(actuser, action_obj, task_obj, inv_obj, oldev_obj, None, action_obj.title,
                                          scripttype, cmdin, argument_cleartext, argumentdynamic, None, None, None,
                                          None,
                                          ActionQStatus.objects.get(name="Started"), actuser)
            # create the actionQ item
            actionq_stopid = new_actionq(actuser, action_obj, task_obj, inv_obj, oldev_obj, actionq_startid,
                                         action_obj.title, scripttype, rescommand, argument_cleartext, argumentdynamic,
                                         reserror, resstatus, resoutput, respid,
                                         ActionQStatus.objects.get(name="Finished"), actuser)
            # update the actionQ with the parent value
            ActionQ.objects.filter(pk=actionq_startid.pk).update(parent=actionq_stopid)
            #  Output to the attribute in the same evidence
            ActionQ.objects.filter(pk=actionq_stopid.pk).update(evid=oldev_obj.pk)
            actq = actionq_stopid.pk

    else:
        # Output to be dropped
        pass
    # actq = actionq_stopid.pk
    return actq


class ActionQStatus(models.Model):
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(ActionQStatus, self).save(*args, **kwargs)


def new_actionq(pactuser, pactionid, ptaskid, pinvid, poldevid, pparent, ptitle, pscripttype,
                pcommand, pargument, pargumentdynamic,
                pcmderror, pcmdstatus, pcmdoutput, pcmdpid,
                pstatus, pcreated_by):
    newactionq = ActionQ.objects.create(
        user=pactuser,
        actionid=pactionid,
        taskid=ptaskid,
        invid=pinvid,
        oldevid=poldevid,
        parent=pparent,
        title=ptitle,
        scripttype=pscripttype,
        command=pcommand,
        argument=pargument,
        argumentdynamic=pargumentdynamic,
        cmderror=pcmderror,
        cmdstatus=pcmdstatus,
        cmdoutput=pcmdoutput,
        cmdpid=pcmdpid,
        status=pstatus,
        created_by=pcreated_by
    )

    return newactionq


class ActionQ(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, blank=True, null=True,
                             related_name="actionq_users")
    actionid = models.ForeignKey(Action, on_delete=models.SET_NULL, default=None, blank=True, null=True,
                                 related_name="actionq_action")
    taskid = models.ForeignKey(Task, on_delete=models.SET_NULL, default=None, blank=True, null=True,
                               related_name="actionq_task")
    evid = models.ForeignKey(Evidence, on_delete=models.SET_NULL, default=None, blank=True, null=True,
                             related_name="actionq_evidence")
    oldevid = models.ForeignKey(Evidence, on_delete=models.SET_NULL, default=None, blank=True, null=True,
                                related_name="actionq_oldevidence")
    invid = models.ForeignKey(Inv, on_delete=models.SET_NULL, default=None, blank=True, null=True,
                              related_name="actionq_inv")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="actionq_parent")
    title = models.CharField(max_length=50, default=None, blank=True, null=True)
    scripttype = models.CharField(max_length=60, blank=False, null=False)
    command = models.CharField(max_length=2048, blank=False, null=False)
    argument = models.CharField(max_length=2048, default=None, blank=True, null=True)
    argumentdynamic = models.CharField(max_length=255, default=None, blank=True, null=True)
    cmderror = models.TextField(default=None, blank=True, null=True)
    cmdstatus = models.TextField(default=None, blank=True, null=True)
    cmdoutput = models.TextField(default=None, blank=True, null=True)
    cmdpid = models.TextField(default=None, blank=True, null=True)
    status = models.ForeignKey(ActionQStatus, on_delete=models.SET_NULL, default=None,
                               blank=True, null=True, related_name="actionq_actionqstatus")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=40, blank=False, null=False)

    def __str__(self):
        return str(self.pk)


class FileHashCalc():
    def __init__(self):
        # self.myfile=pfile
        pass

    def md5sum(self, filename):
        h  = hashlib.md5()
        b  = bytearray(128*1024)
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda : f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()

    def sha1sum(self, filename):
        h  = hashlib.sha1()
        b  = bytearray(128*1024)
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda : f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()

    def sha256sum(self, filename):
        h  = hashlib.sha256()
        b  = bytearray(128*1024)
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda : f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()

    def sha512sum(self, filename):
        h  = hashlib.sha512()
        b  = bytearray(128*1024)
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda : f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()

    #res_md5 = FileHashCals().md5sum('FilePath')

# def add_to_profile(pevattr):
#     print(pevattr)


# managing chunked uploads
# def handle_uploaded_file_chunks(pfile, ppath):
#     with open(ppath, 'wb+') as destination:
#         for chunk in pfile.chunks():
#             destination.write(chunk)