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
# 2019.08.13  Lendvay     2      Added temp folder for each action and connections, removed action file
# 2019.08.30  Lendvay     3      Added playbooktemplate graph
# 2019.09.03  Lendvay     4      Fixed add new playbook
# 2020.05.16  Lendvay     5      autorun automation on attribute save
# **********************************************************************;
from django.conf import settings
from django.db import models
from django.urls import reverse
import tempfile
import json
from django.db.models import Q
from django.db import transaction
# HTML renderer
import misaka
from invs.models import Inv
from tinymce.models import HTMLField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from datetime import datetime
from django.dispatch import receiver
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR, S_IWGRP
import ipaddress
import re
import pydot
from tasks.scripts.String_Parser import StringParser
from django.db import transaction

# import pathlib
# from bCIRT.settings import PROJECT_ROOT
from django.utils.timezone import now as timezone_now
from datetime import datetime
# from django.conf import settings
from django.utils.timezone import make_aware
from configuration.models import SettingsSystem
import random
import string
import magic
import os
from os import path
import hashlib
from shutil import copy
from base64 import b64encode
from bCIRT.settings import MEDIA_ROOT
from configuration.models import ConnectionItem, ConnectionItemField, decrypt_string
from .scriptmanager.run_script import run_script_class
import logging
logger = logging.getLogger('log_file_verbose')

# Get the user so we can use this
from django.contrib.auth import get_user_model
from django import template
User = get_user_model()
# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
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
        # minutes = (diff.seconds % 3600) // 60
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
    description_html = models.TextField(max_length=750, editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(MitreAttck_Tactics, self).save(*args, **kwargs)


class MitreAttck_Techniques(models.Model):
    objects = models.Manager()
    matacref = models.ForeignKey(MitreAttck_Tactics, on_delete=models.SET_DEFAULT, default=None,
                                 related_name="matec_matac")
    matecid = models.CharField(max_length=6, blank=False, null=False)
    name = models.CharField(max_length=25, blank=False, null=False)
    enabled = models.BooleanField(default=True)
    description = models.TextField(max_length=500, default="")
    description_html = models.TextField(max_length=750, editable=True, default='', blank=True)

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
    description_html = models.TextField(max_length=750, editable=True, default='', blank=True)

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
    description_html = models.TextField(max_length=750, editable=True, default='', blank=True)

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
    description_html = models.TextField(max_length=750, editable=True, default='', blank=True)
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
    description_html = models.TextField(max_length=750, editable=True, default='', blank=True)

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
    description_html = models.TextField(max_length=750, editable=True, default='', blank=True)

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
    description_html = models.TextField(max_length=750, editable=True, default='', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(TaskVarCategory, self).save(*args, **kwargs)


class Playbook(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50, default="", blank=False, null=False)
    version = models.CharField(max_length=20, default="", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True, related_name="playbook_users")
    inv = models.ForeignKey(Inv, on_delete=models.CASCADE, default=None, null=True, blank=True,
                            related_name="playbook_inv")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")

    # description = models.TextField(max_length=500, default="")
    description = HTMLField()
    # description_html = models.TextField(max_length=750, editable=True, default='', blank=True)
    description_html = HTMLField()

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


@transaction.atomic
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
    pbtmpitem_list = pplaybooktemplate.playbooktemplateitem_playbooktemplate.all().order_by('itemorder')
    for tmp_item in pbtmpitem_list:
        tmp_to_copy = TaskTemplate.objects.get(pk=tmp_item.acttask.pk)
        # logger.info("01 tmp_item:%s"%(tmp_item))
        # logger.info("02 tmp_to_copy:%d %s"%(tmp_to_copy.pk, tmp_to_copy))
        # if the playbooktemplateitem refers to a previous item, we need to
        # find the pk of the newly created previous item matching the previous reference
        if tmp_item.prevtask:
            # logger.info("11 IF tmp_item.prevtask:%s" % (tmp_item.prevtask))
            # logger.info("X:%s" % (tmp_item.prevtask.pk))
            # tmp_item_prevtaskpk = TaskTemplate.objects.get(pk=tmp_item.prevtask.pk).pk
            tmp_item_prevtaskpk = PlaybookTemplateItem.objects.get(pk=tmp_item.prevtask.pk).pk
            # logger.info("12 IF tmp_item_prevtaskpk:%s" % (tmp_item_prevtaskpk))
            # print(str(tmp_item.pk)+"->"+str(tmp_item_prevtaskpk))
            # logger.info("13 IF item_mapping")
            # logger.info(item_mapping)
            tmp_item_prevtask = Task.objects.get(pk=item_mapping[tmp_item_prevtaskpk])
            # logger.info("14 IF tmp_item_prevtask:%s" % (tmp_item_prevtask))
            # print(tmp_item_prevtask)
        else:
            # logger.info("21 ELSE tmp_item_prevtask_none")
            tmp_item_prevtask = None
        # if tmp_item.prevtask:
        #     tmp_item_prevtask=TaskTemplate.objects.get(pk=tmp_item.prevtask.pk)
        # else:
        #     tmp_item_prevtask = None
        # tmp_item_prevtask = None
        # logger.info("31 NEW TASK:%s" % (tmp_item_prevtask))
        new_task = add_task_from_template(
            atitle=tmp_to_copy.title,
            astatus=tmp_to_copy.status,
            aplaybook=playbook_obj,
            # auser=tmp_to_copy.user,
            auser=puser,
            ainv=pinv,
            aaction=tmp_to_copy.action,
            aactiontarget=tmp_item_prevtask,
            acategory=tmp_to_copy.category,
            apriority=tmp_to_copy.priority,
            atype=tmp_to_copy.type,
            asummary=tmp_to_copy.summary,
            adescription=tmp_to_copy.description,
            arequiresevidence=tmp_to_copy.requiresevidence,
            amodified_by=str(puser),
            acreated_by=str(puser)
        )

        if TaskVar.objects.filter(tasktemplate=tmp_to_copy.pk):
            taskvars = TaskVar.objects.filter(tasktemplate=tmp_to_copy.pk)
            for taskvaritem in taskvars:
                # clone taskvar item
                cloneobj = taskvaritem
                cloneobj.pk = None
                cloneobj.tasktemplate = None
                cloneobj.task = new_task
                cloneobj.save()
        # print(str(new_task)+"->->"+str(tmp_item_prevtask))
        #  here I need to map the template pks to the new pks so I can assign the proper actions
        item_mapping.update({tmp_item.pk: new_task.pk})
    # to run the post-save function:
    playbook_obj.save()
    return playbook_obj

# Create your models here.


class Task(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="task_users")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="task_parent")
    inputfrom = models.ForeignKey('self', on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                  related_name="task_inputfrom")
    inv = models.ForeignKey(Inv, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="task_inv")
    #  this is circular reference...could cause issues...lazy relationship
    action = models.ForeignKey('tasks.Action', on_delete=models.SET_NULL, default=None, null=True, blank=True,
                               related_name="task_action")
    actiontarget = models.ForeignKey('self', on_delete=models.SET_NULL, default=None,  null=True, blank=True,
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
    # description_html = models.TextField(editable=True, default='', blank=True)
    description_html = HTMLField()

    requiresevidence = models.BooleanField(default=False, null=False, blank=False)

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

    def readonly(self):
        # print(self.status.name)
        if self.status.name == 'Completed' or self.status.name == 'Skipped':
            return True
        else:
            return False

    @transaction.atomic
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        #  this is to check if the status record has been changed or not
        if self.status != self.__original_status:
            if self.status.name == "Completed":
                if self.requiresevidence and (not self.evidence_task.all() and self.type == 2):
                    raise ValidationError(_('You must create an evidence to be able to close the task.'))

                # if status changed do something here
                # check for tasks which are target of any action and are automatic tasks (type=1) and not closed
                # exclude tasks that are already completed (pk=2,4)
                if Task.objects.filter(actiontarget=self.pk, type=1).exclude(status=2).exclude(status=4).exists():
                    targettasks = Task.objects.filter(actiontarget=self.pk, type=1)\
                        .exclude(status=2)\
                        .exclude(status=4)\
                        .order_by('pk')
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
                            # here we need to find the proper evidence...
                            sourcetask = Task.objects.get(pk=self.pk)
                            evid = sourcetask.evidence_task.all()
                            # evattrs = None
                            # here we will need a nested for loop
                            if TaskVar.objects.filter(task=sourcetask, name='ActionTarget', category=2).exists():
                                taskvar_obj = TaskVar.objects.get(task=sourcetask, name='ActionTarget', category=2)
                                taskvar_value = taskvar_obj.value
                                # print(taskvar_value)
                                if taskvar_value == 'first' or taskvar_value == "" and \
                                        Task.objects.filter(pk=evid.first().pk).exists():
                                    evidpk = evid.first().pk
                                elif taskvar_value == 'last':
                                    evidpk = evid.last().pk
                                elif int(taskvar_value):
                                    evidpk = int(taskvar_value)
                                else:
                                    if evid.first():
                                        evidpk = evid.first().pk  # Task.objects.get(pk=evid.first().pk)
                                    else:
                                        evidpk = None
                            else:
                                if evid.first():
                                    evidpk = evid.first().pk  # Task.objects.get(pk=evid.first().pk)
                                else:
                                    evidpk = None
                            if evidpk:
                                # checking for a list of all attributes which match the attribute filter in the action
                                evidobj = Evidence.objects.get(pk=evidpk)
                                curraction = Action.objects.get(pk=targettaskactionpk)
                                filterforpk = None
                                evidattrs = None
                                if curraction.scriptinputattrtypeall and curraction.scriptinput.name == 'Attribute':
                                    evidattrs = evidobj.evattr_evidence.all()
                                elif not curraction.scriptinputattrtypeall and \
                                        curraction.scriptinput.name == 'Attribute':
                                    filterforpk = curraction.scriptinputattrtype
                                    evidattrs = evidobj.evattr_evidence.filter(evattrformat=filterforpk)
                                if evidattrs:
                                    for evidattr1 in evidattrs:
                                        # print("AUTOMATED: "+str(targettaskactionpk)+":"+str(targettaskinvpk)+":"+
                                        #  str(targettaskpk)+":"+str(evidpk))
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
                                    # print("AUTOMATED: "+str(targettaskactionpk)+":"+str(targettaskinvpk)+":"+
                                    #  str(targettaskpk)+":"+str(evidpk))
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
                pmodified_by = 'admin'
            else:
                pmodified_by = str(self.modified_by)
            Inv.objects.filter(pk=self.inv.pk).update(modified_at=timezone_now(), modified_by=pmodified_by)

        super(Task, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_status = self.status

    def clean(self):
        if self.inv and self.inv.readonly():
            raise ValidationError(_('The Investigation is Read-Only!'))

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
        except Exception:
            retval = None
        return retval

@transaction.atomic
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True, related_name="evidence_users")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="evidence_task")
    inv = models.ForeignKey(Inv, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="evidence_inv")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="evidence_parent")
    parentattr = models.ForeignKey('EvidenceAttr', on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                   related_name="evidence_parentattr")
    prevev = models.ForeignKey('self', on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="evidence_prevev")

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    evidenceformat = models.ForeignKey(EvidenceFormat, on_delete=models.SET_DEFAULT, default=1, null=False,
                                       blank=False, related_name="evidence_evidenceformat")
    mitretactic = models.ForeignKey(MitreAttck_Tactics, on_delete=models.SET_DEFAULT, default=1, null=False,
                                    blank=False, related_name="evidence_mitretactic")

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
                super(Evidence, self).save(*args, **kwargs)
                self.fileRef = file_to_save
            # kwargs.pop('force_insert')
        if self.inv:
            Inv.objects.filter(pk=self.inv.pk).\
                update(modified_at=timezone_now(), modified_by=self.modified_by)
        if self.task:
            Task.objects.filter(pk=self.task.pk).\
                update(modified_at=timezone_now(), modified_by=self.modified_by)

        # checking for maliciousness and setting the attributes accordingly
        if self.description:
            ismalicious = StringParser().check_malicious(self.description)

            if ismalicious:
                # setobservable = False
                if EvReputation.objects.get(name=ismalicious):
                    attr_rep = EvReputation.objects.get(name=ismalicious)
                else:
                    attr_rep = None
                # if self.pk:
                #     ev_obj = Evidence.objects.get(pk=self.pk)
                #     evidattr = add_evattr(
                #         auser=self.user,
                #         aev=ev_obj,
                #         aevattrvalue=ismalicious,
                #         aevattrformat=EvidenceAttrFormat.objects.get(name='Reputation'),
                #         amodified_by=str(self.user),
                #         acreated_by=str(self.user),
                #         aattr_reputation=attr_rep,
                #         aforce=False
                #     )
                # Creating a clone for the attribute item inspected
                # print("XXX broke here the loop, need to add reputation to the intel table instead")
                # if self.parentattr and "xxx"=="aaa":
                #     if self.parentattr:
                #         # cloneevidattr = EvidenceAttr.objects.get(pk=self.parentattr.pk)
                #         cloneevidattr = self.parentattr
                #         cloneevidattr.attr_reputation = attr_rep
                #         if cloneevidattr.attr_reputation.name == 'Suspicious' \
                #                 or cloneevidattr.attr_reputation.name == 'Malicious':
                #             cloneevidattr.observable = True
                #         cloneevidattr.pk = None
                #         newclone = cloneevidattr.save()
        super(Evidence, self).save(*args, **kwargs)

    def clean(self):
        if self.inv is None and self.task is None:
            raise ValidationError(_('You must select an Investigation or a Task.'))
        if self.task and Task.objects.filter(pk=self.task.pk).exists:
            # if Task.objects.get(pk=self.task.pk).status.name == "Completed" or \
            #      Task.objects.get(pk=self.task.pk).status.name == "Skipped":
            if self.task and Task.objects.get(pk=self.task.pk).readonly():
                raise ValidationError(_('Task cannot be closed!'))
        if self.inv and Inv.objects.filter(pk=self.inv.pk).exists():
            # if Inv.objects.get(pk=self.inv.pk).status.name == "Closed" or \
            #     Inv.objects.get(pk=self.inv.pk).status.name == "Archived":
            if self.task and Task.objects.get(pk=self.task.pk).readonly():
                raise ValidationError(_('Investigation cannot be closed!'))
        super(Evidence, self).clean()

    def myattributes(self):
        retval = EvidenceAttr.objects.filter(ev=self).select_related('attr_reputation')
        return retval


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True, related_name="evattr_users")
    ev = models.ForeignKey(Evidence, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="evattr_evidence")
    evattrvalue = models.CharField(max_length=2048)
    observable = models.BooleanField(default=False, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    evattrformat = models.ForeignKey(EvidenceAttrFormat, on_delete=models.SET_DEFAULT, default=1, null=False,
                                     blank=False, related_name="evattr_evidenceattrformat")
    attr_automatic = models.BooleanField(default=None, null=True, blank=True)
    attr_reputation = models.ForeignKey(EvReputation, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="evattr_evreputation")

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

    @transaction.atomic
    def save(self, *args, **kwargs):
        # if the attribute is malicious, make the attribute an observable
        if self.attr_reputation:
            if self.evattrformat.name != 'Reputation' and \
                    (self.attr_reputation.name == 'Suspicious' or self.attr_reputation.name == 'Malicious'):
                self.observable = True
        if self.ev:
            Evidence.objects.filter(pk=self.ev.pk).update(modified_at=timezone_now(), modified_by=self.modified_by)
            if Evidence.objects.get(pk=self.ev.pk).task:
                task_pk = Evidence.objects.get(pk=self.ev.pk).task.pk
                Task.objects.filter(pk=task_pk).update(modified_at=timezone_now(), modified_by=self.modified_by)
            if Evidence.objects.get(pk=self.ev.pk).inv:
                inv_pk = Evidence.objects.get(pk=self.ev.pk).inv.pk
                Inv.objects.filter(pk=inv_pk).update(modified_at=timezone_now(), modified_by=self.modified_by)
        super(EvidenceAttr, self).save(*args, **kwargs)

    def get_sameitems_inv(self):
        # similar_evattr = EvidenceAttr.objects.\
        # filter(evattrvalue__icontains=self.evattrvalue).exclude(ev__pk=self.ev.pk)
        exclusion_list = SettingsSystem.objects.filter(Q(settingname="excl.attr.alreadyseen") & Q(enabled=True))\
            .values('settingvalue')
        similar_evattr = EvidenceAttr.objects.filter(evattrvalue=self.evattrvalue)\
            .exclude(ev=self.ev)\
            .exclude(evattrvalue__in=exclusion_list)
        # similar_evattr = EvidenceAttr.objects.filter(evattrvalue=self.evattrvalue)\
        #     .exclude(ev=self.ev)
            # .exclude(evattrvalue='d41d8cd98f00b204e9800998ecf8427e')\
            # .exclude(evattrvalue='da39a3ee5e6b4b0d3255bfef95601890afd80709')\
            # .exclude(evattrvalue='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')

        similar_evs = set()
        # print(similar_evattr)
        for similar_evattritem in similar_evattr:
            similar_evs.add(similar_evattritem.ev)
        similar_invs = set()
        for similar_evinv in similar_evs:
            if similar_evinv.inv:
                similar_invs.add(similar_evinv.inv)
        # print(list(similar_invs)[0])
        # print(similar_invs)
        return similar_invs

    def get_sameitems_inv_values(self):
        # similar_evattr = EvidenceAttr.objects.\
        # filter(evattrvalue__icontains=self.evattrvalue).exclude(ev__pk=self.ev.pk)
        # similar_evattr = EvidenceAttr.objects.filter(evattrvalue=self.evattrvalue)\
        #     .exclude(ev=self.ev)\
        #     .exclude(evattrvalue='d41d8cd98f00b204e9800998ecf8427e')\
        #     .exclude(evattrvalue='da39a3ee5e6b4b0d3255bfef95601890afd80709')\
        #     .exclude(evattrvalue='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')\
        #     .select_related('user')\
        #     .select_related('ev')\
        #     .select_related('inv')
            # .values('pk', 'user__username', 'ev', 'ev__pk')
        exclusion_list = SettingsSystem.objects.filter(Q(settingname="excl.attr.alreadyseen") & Q(enabled=True))\
            .values('settingvalue')
        similar_evattr = EvidenceAttr.objects.filter(evattrvalue=self.evattrvalue)\
            .exclude(ev=self.ev)\
            .exclude(evattrvalue__in=exclusion_list)\
            .select_related('user')\
            .select_related('ev')\
            .select_related('inv')

        similar_evs = set()
        # print(similar_evattr)
        for similar_evattritem in similar_evattr:
            similar_evs.add(similar_evattritem.ev)
        similar_invs = set()
        for similar_evinv in similar_evs:
            if similar_evinv.inv:
                similar_invs.add(similar_evinv.inv)
        # print(list(similar_invs)[0])
        # print(similar_invs)
        return similar_invs

    def clean(self):
        # if self.inv is None and self.task is None:
        #     raise ValidationError(_('You must select an Investigation or a Task.'))
        # if self.ev.task and Task.objects.filter(pk=self.ev.task.pk).exists:
        #     if Task.objects.get(pk=self.ev.task.pk).status.name == "Completed" or \
        #          Task.objects.get(pk=self.ev.task.pk).status.name == "Skipped":
        #         raise ValidationError(_('Task cannot be closed!'))
        inv_pk = None
        if self.ev.inv and Inv.objects.filter(pk=self.ev.inv.pk).exists():
            inv_pk = self.ev.inv.pk
            if Inv.objects.get(pk=self.ev.inv.pk).status.name == "Closed" or \
                    Inv.objects.get(pk=self.ev.inv.pk).status.name == "Archived":
                raise ValidationError(_('Investigation cannot be closed!'))
            elif self.pk:
                # Submitting to any threat intel collection tools
                # submit somehow....iterate through the items
                # This will read the system parameters and replace the $ATTRIBUTE$ string
                # with the attribute value in the system settings value and will call a script
                # there is also a check on post_save
                run_auto_action_on_attribute(self)
        pass

    class Meta:
        indexes = [
            models.Index(fields=['evattrvalue'], name='evattrvalue_idx'),
        ]


class EvidenceAttrIntel(models.Model):
    objects = models.Manager()
    severity = models.CharField(max_length=10, default=None, blank=True, null=True)
    confidence = models.SmallIntegerField(default=None, blank=True, null=True)
    state = models.CharField(max_length=10, default=None, blank=True, null=True)
    #date_last = models.CharField(max_length=20)
    date_last = models.DateTimeField(default=None, blank=True, null=True)
    itype = models.CharField(max_length=20, default=None, blank=True, null=True)
    source = models.CharField(max_length=100, default=None, blank=True, null=True)
    intelvalue = models.CharField(max_length=255, default=None, blank=True, null=True)
    evidenceattr = models.ForeignKey(EvidenceAttr, on_delete=models.CASCADE, default=None, blank=True, null=True,
                           related_name="evidenceattrintel_evidenceattr")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    intelsource = models.CharField(max_length=100, default="unknown")

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super(EvidenceAttrIntel, self).save(*args, **kwargs)


def run_auto_action_on_attribute(self):
    if Action.objects.filter(enabled=True).filter(runonsaveattr=True).exists():
        actionslist = Action.objects.filter(enabled=True).filter(runonsaveattr=True)
        for actionitem in actionslist:
            # print(actionitem)
            if actionitem.scriptinputattrtype == self.evattrformat \
                    or actionitem.scriptinputattrtype is None:
                runaction = True
                if actionitem.reputationregex:
                    regexp = re.compile(r'%s' % actionitem.reputationregex)
                    # regexp = re.compile(r'[a-zA-Z-.]@example.com$')
                    if regexp.search(str(self.attr_reputation)):
                        # adding if matches
                        runaction = True
                    else:
                        # blocking action if doesn't match reputation
                        runaction = False
                else:
                    runaction = True
                if actionitem.skipregex:
                    regexp = re.compile(r'%s' % actionitem.skipregex)
                    # regexp = re.compile(r'[a-zA-Z-.]@example.com$')
                    if regexp.search(self.evattrvalue):
                        # skipping since it's whitelisted
                        runaction = False
                if runaction:
                    run_action(
                        pactuser=self.user,
                        pactusername="action",
                        pev_pk=self.ev.pk,
                        pevattr_pk=self.pk,
                        ptask_pk=None,
                        pact_pk=actionitem.pk,
                        pinv_pk=self.ev.inv.pk,
                        pargdyn='',
                        pattr='',
                        pcheckmalicious=False,
                        paddevattrintel=actionitem.intelfeed,
                        pnoclone=True
                    )


def get_evidencesameitems_inv_values(pk):
    pk=int(pk)
    # similar_evattr = EvidenceAttr.objects.filter(evattrvalue__icontains=self.evattrvalue).exclude(ev__pk=self.ev.pk)
    # myattrvalue = EvidenceAttr.objects.filter(pk=pk).values('evattrvalue')[:1]
    # similar_evattr = EvidenceAttr.objects.exclude(pk=pk) \
    #     .filter(evattrvalue=myattrvalue)\
    #     .exclude(evattrvalue='d41d8cd98f00b204e9800998ecf8427e') \
    #     .exclude(evattrvalue='da39a3ee5e6b4b0d3255bfef95601890afd80709') \
    #     .exclude(evattrvalue='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')\
    #     .select_related('user__username')\
    #     .select_related('attr_reputation__pk') \
    #     .select_related('evattrformat__name') \
    #     .select_related('evattrformat__pk') \
    #     .select_related('ev__inv__pk') \
    #     .values('pk', 'attr_reputation__pk', 'evattrformat__name', 'evattrformat__pk', 'observable', 'evattrvalue',
    #             'user__username', 'ev__inv__pk')

    exclusion_list = SettingsSystem.objects.filter(Q(settingname="excl.attr.alreadyseen") & Q(enabled=True))\
        .values('settingvalue')

    myattrvalue = EvidenceAttr.objects.filter(pk=pk).values('evattrvalue')[:1]
    similar_evattr = EvidenceAttr.objects.exclude(pk=pk) \
        .filter(evattrvalue=myattrvalue) \
        .exclude(evattrvalue__in=exclusion_list) \
        .select_related('user__username')\
        .select_related('attr_reputation__pk') \
        .select_related('evattrformat__name') \
        .select_related('evattrformat__pk') \
        .select_related('ev__inv__pk') \
        .values('pk', 'attr_reputation__pk', 'evattrformat__name', 'evattrformat__pk', 'observable', 'evattrvalue',
                'user__username', 'ev__inv__pk')

    # similar_evs = set()
    # # print(similar_evattr)
    # for similar_evattritem in similar_evattr:
    #     similar_evs.add(similar_evattritem.ev)
    # similar_invs = set()
    # for similar_evinv in similar_evs:
    #     if similar_evinv.inv:
    #         similar_invs.add(similar_evinv.inv)
    # # print(list(similar_invs)[0])
    # # print(similar_invs)
    return similar_evattr


@transaction.atomic
def evidenceattrobservabletoggle(pattrpk):
    evattr_obj = EvidenceAttr.objects.get(pk=pattrpk)
    evattr_obj.observable = not evattr_obj.observable
    evattr_obj.save()


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
        except Exception:
            return False

    def find_email(self, str1):
        #  ipattern = re.compile('([^[({@|\s]+@[^@]+\.[^])}@|\s]+)')
        # ipattern = re.compile('([^@":[>|<\s]+@[^@]+\.[^]>"<)\}@|\s]+)')
        #https://www.regular-expressions.info/refunicode.html
        ipattern = re.compile(r'([\\p{L}\\p{M}\\p{S}\\p{N}\\p{P}a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', re.UNICODE)
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


# def save_code(logfile, script_code):
#     try:
#         code_field = script_code
#     except Exception as err:
#         code_field += str(err)
#     finally:
#         try:
#             with open(logfile, 'w') as f:
#                 #  replace newlines as the HTML will likely contain those...in windows format
#                 newdata = code_field.replace("\r\n", "\n")
#                 f.write(newdata)
#                 return 1
#         except Exception as e:
#             return 0

class Automation(models.Model):
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True, related_name="automation_users")
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, default=None, blank=False, null=True, related_name="automation_type")
    name = models.CharField(max_length=50, blank=False, null=False)
    version = models.CharField(max_length=20, default=None, null=True)
    script_type = models.ForeignKey(ScriptType, on_delete=models.SET_DEFAULT, default='1', blank=False, null=False,
                                    related_name="automation_scripttype")
    script_category = models.ForeignKey(ScriptCategory, on_delete=models.SET_DEFAULT, default='1', blank=False,
                                        null=False, related_name="automation_scriptcategory")
    code = models.TextField(editable=True, default='', blank=True)
    autorequirements = models.TextField(editable=True, default='', blank=True, null=True)
    fileName = models.CharField(max_length=255, default="", null=True, blank=True)
    fileRef = models.FileField(upload_to=upload_to_action, null=True, blank=True)
    filecreated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    description = HTMLField()
    # description_html = models.TextField(editable=True, default='', blank=True)
    description_html = HTMLField()

    # class Meta:
#       ordering = ['-id']
    #  to satisfy pyCharm

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(Automation, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "tasks:auto_detail",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if (self.fileRef == "") and (self.code == ""):
            # raise ValidationError(_('You must define Code or upload a script.'))
            raise ValidationError(_("You must either define Code or upload a script file!"))
        pass


class Action(models.Model):
    objects = models.Manager()
    enabled = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True, related_name="action_users")
    title = models.CharField(max_length=50, blank=False, null=False)
    version = models.CharField(max_length=20, default=None, null=True)
    automationid = models.ForeignKey(Automation, on_delete=models.SET_NULL, default=None, blank=False, null=True,
                                     related_name="action_automation")
    scriptoutput = models.ForeignKey(ScriptOutput, on_delete=models.SET_NULL, default='1', blank=False, null=True,
                                     related_name="action_scriptoutput")
    scriptoutputtype = models.ForeignKey(EvidenceAttrFormat, on_delete=models.SET_NULL, default='1', blank=True,
                                         null=True, related_name="action_scriptoutputtype")
    scriptinput = models.ForeignKey(ScriptInput, on_delete=models.SET_NULL, default='1', blank=False, null=True,
                                    related_name="action_scriptinput")
    scriptinputattrtype = models.ForeignKey(EvidenceAttrFormat, on_delete=models.SET_NULL, default=None, blank=True,
                                            null=True, related_name="action_scriptinputattrtype")
    runonsaveattr = models.BooleanField(default=False)
    skipregex = models.CharField(max_length=255, default=None, blank=True, null=True)
    reputationregex = models.CharField(max_length=255, default=None, blank=True, null=True)
    intelfeed = models.BooleanField(default=False)
    scriptinputattrtypeall = models.BooleanField(default=False)
    outputtarget = models.ForeignKey(OutputTarget, on_delete=models.SET_DEFAULT, default=1, blank=True, null=True,
                                     related_name="action_outputtarget")
    outputdescformat = models.ForeignKey(EvidenceFormat, on_delete=models.SET_DEFAULT, default=1, blank=True, null=True,
                                         related_name="action_outputdescformat")
    argument = models.CharField(max_length=4096, default=None, blank=True, null=True)
    connectionitemid = models.ForeignKey(ConnectionItem, on_delete=models.SET_NULL, default=None, blank=True, null=True,
                                         related_name="action_connectionitem")

    timeout = models.PositiveIntegerField(default=300, null=False, blank=False)
    #  300 seconds
    fileName = models.CharField(max_length=255, default="", null=True, blank=True)
    fileRef = models.FileField(upload_to=upload_to_action, null=True, blank=True)
    filecreated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    description = HTMLField()
    # description_html = models.TextField(editable=True, default='', blank=True)
    description_html = HTMLField()

    # class Meta:
#       ordering = ['-id']
    #  to satisfy pyCharm

    def __str__(self):
        return str(self.title)+" ("+str(self.scriptinput.shortname)+"->"+str(self.outputtarget.shortname)+")"

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.automationid:
            # print(self.automationid)
            self.enabled = False

        self.description_html = misaka.html(self.description)
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
        # if (self.fileRef == "") and (self.code == ""):
        #     raise ValidationError(_('You must define Code or upload a script.'))
        #     raise ValidationError(_("You must either define Code or upload a script file!"))
        pass


@transaction.atomic
def clone_action(paction_pk):
    cloneobj = Action.objects.get(pk=paction_pk)
    if cloneobj:
        cloneobj.pk = None
        # length comes from the model max length - _clone
        if len(cloneobj.title) >= 44:
            cloneobj.title = "%s_clone" % cloneobj.title[:-6]
        else:
            cloneobj.title = "%s_clone" % cloneobj.title
        cloneobj.save()
        return True
    return False


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

def actiongroupmember_items():
    actiongroups_file = set()
    actiongroups_desc = set()
    actiongroups_attr = set()
    actiongroupmember_all = ActionGroupMember.objects.all() \
        .select_related('actionid')
    # .select_related('actionid__scriptinput')\
    # .values('pk', 'actionid__enabled', 'actionid__scriptinput', 'actiongroupid')
    if actiongroupmember_all:
        for actgrpmember in actiongroupmember_all:
            # input is description scriptinput=1:
            if actgrpmember.actionid.enabled is True and actgrpmember.actionid.scriptinput.pk == 1:
                # actiongrmember_desc.add(actgrpmember.actionid)
                actiongroups_desc.add(actgrpmember.actiongroupid)
            # input is file scriptinput=2:
            elif actgrpmember.actionid.enabled is True and actgrpmember.actionid.scriptinput.pk == 2:
                # actiongrmember_file.add(actgrpmember.actionid)
                actiongroups_file.add(actgrpmember.actiongroupid)
            # input is attribute scriptinput=1:
            elif actgrpmember.actionid.enabled is True and actgrpmember.actionid.scriptinput.pk == 3:
                # actiongrmember_attr.add(actgrpmember.actionid)
                actiongroups_attr.add(actgrpmember.actiongroupid)
            # input is none of the above:
            else:
                # print(actgrpmember.actionid.scriptinput.pk)
                pass
    retval = dict()
    retval['actiongroups_desc'] = actiongroups_desc
    retval['actiongroups_file'] = actiongroups_file
    retval['actiongroups_attr'] = actiongroups_attr
    return retval


class TaskTemplate(models.Model):
    objects = models.Manager()
    tasktemplatename = models.CharField(max_length=50, blank=False, null=False)
    enabled = models.BooleanField(default=True)
    # fields from Task model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True, blank=True,
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
    actiontarget = models.ForeignKey('self', on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                     related_name="tasktemplate_actiontarget")
    description = HTMLField()
    # description_html = models.TextField(editable=True, default='', blank=True)
    description_html = HTMLField()

    requiresevidence = models.BooleanField(default=False, null=False, blank=False)

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
        # Don't allow automated tasks without an action.
        if self.type.pk == 1 and self.action is None: # or self.actiontarget is None):
            raise ValidationError(_('You must povide an action for an Automated task.'))


class TaskVar(models.Model):
    objects = models.Manager()
    category = models.ForeignKey(TaskVarCategory, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                 related_name="taskvar_taskvarcategory")
    type = models.ForeignKey(TaskVarType, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                             related_name="taskvar_taskvartype")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="taskvar_task")
    tasktemplate = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, default=None, null=True, blank=True,
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


def add_taskvar(acategory, atype, atask, atasktemplate, aname, avalue, adescription,
                amodified_by, acreated_by, arequired=True, aenabled=True,):
    obj = TaskVar.objects.create(
        category=acategory,
        type=atype,
        task=atask,
        tasktemplate=atasktemplate,
        name=aname,
        value=avalue,
        description=adescription,
        modified_by=amodified_by,
        created_by=acreated_by,
        required=arequired,
        enabled=aenabled,
    )


class PlaybookTemplate(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50, default="", blank=False, null=False)
    enabled = models.BooleanField(default=True)
    version = models.CharField(max_length=20, default="", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True, related_name="playbooktemplate_users")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")

    # description = models.TextField(max_length=500, default="")
    # description_html = models.TextField(editable=True, default='', blank=True)
    description = HTMLField()
    description_html = HTMLField()

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
    playbooktemplateid = models.ForeignKey(PlaybookTemplate, on_delete=models.CASCADE, default=None, null=False,
                                           blank=False, related_name="playbooktemplateitem_playbooktemplate")
    enabled = models.BooleanField(default=True)
    acttask = models.ForeignKey(TaskTemplate, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                related_name="playbooktemplateitem_tasktemplate_act")
    nexttask = models.ForeignKey('self', on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                 related_name="playbooktemplateitem_playbooktemplateitem_next")
    prevtask = models.ForeignKey('self', on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                 related_name="playbooktemplateitem_playbooktemplateitem_prev")
    itemorder = models.SmallIntegerField(default=0, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, null=True, related_name="playbooktemplateitem_users")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")

    # description = models.TextField(max_length=500, default="")
    # description_html = models.TextField(editable=True, default='', blank=True)
    description = HTMLField()
    description_html = HTMLField()

    def __str__(self):
        return str(self.pk) + " - " + str(self.acttask.title)

    def get_absolute_url(self):
        return reverse(
            "tasks:playtmp_detail",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        # PlaybookTemplate.objects.filter(pk=self.playbooktemplateid.pk).update(modified_at=timezone_now(),
        # smodified_by=self.modified_by)
        playbooktemplate_obj = PlaybookTemplate.objects.filter(pk=self.playbooktemplateid.id)
        playbooktemplate_obj.update(modified_at=timezone_now(), modified_by=self.modified_by)
        playbooktemplate_obj[0].save()
        # PlaybookTemplate.objects.get(pk=self.playbooktemplateid.pk).save()
        super(PlaybookTemplateItem, self).save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.playbooktemplateid.playbooktemplateitem_playbooktemplate.filter(prevtask=self.pk):
            reftasks = self.playbooktemplateid.playbooktemplateitem_playbooktemplate.filter(prevtask=self.pk)
            reftaskout = list()
            for i in reftasks:
                reftaskout.append(i.pk)
            raise ValidationError("Task #%s is providing input for other tasks: #%s" % (self.pk, reftaskout))
        super(PlaybookTemplateItem, self).delete(*args, **kwargs)

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if not self.acttask:
            raise ValidationError(_('You must select an actual Task.'))
        # Check for duplicate itemorder
        if self.playbooktemplateid.playbooktemplateitem_playbooktemplate:
            if self.playbooktemplateid.playbooktemplateitem_playbooktemplate.\
                    filter(itemorder=self.itemorder).\
                    exclude(pk=self.pk):
                raise ValidationError(_('The Itemorder is already in use.'))
        # check if the previous task is a later task in the queue or if it is the same as the nexttask
        if self.prevtask:
            if self.prevtask == self.nexttask and self.prevtask is not None:
                raise ValidationError(_('Previous and Next tasks cannot be the same.'))
            if self.prevtask.itemorder > self.itemorder:
                raise ValidationError(_('Previous Task ID cannot be lower than the Actual Task ID.'))
        # pass


# #### PROCEDURES
def playbooktemplateitem_check_delete_condition(ptmpitem_pk):
    reftaskout = list()
    ptmpitem_obj = PlaybookTemplateItem.objects.get(pk=ptmpitem_pk)
    # print(ptmpitem_obj.playbooktemplateid.playbooktemplateitem_playbooktemplate)
    if ptmpitem_obj.playbooktemplateid.playbooktemplateitem_playbooktemplate.filter(prevtask=ptmpitem_pk):
        reftasks = ptmpitem_obj.playbooktemplateid.playbooktemplateitem_playbooktemplate.filter(prevtask=ptmpitem_pk)
        for i in reftasks:
            reftaskout.append(i.pk)
    return reftaskout


@receiver(models.signals.post_save, sender=PlaybookTemplate)
@transaction.atomic
def generate_graph_PlaybookTemplate(sender, instance, **kwargs):
    """
    Generate playbooktemplate graph
    """
    curr_pk = instance.pk
    graphfilecontents = "digraph demo1 {\nsubgraph cluster_p {\nlabel = \"PlaybookTemplate #" + str(curr_pk) + " - " + \
                        instance.name+"\"; \n" \
                        "node [shape=record fontname=Arial];\nStart [shape=circle]\n"
    # ptmpitem_related_obj = PlaybookTemplateItem.objects.filter(playbooktemplateid=instance.pk)
    ptmpitem_related_obj =  instance.playbooktemplateitem_playbooktemplate.all()
    # print("Steps:%d"%(len(ptmpitem_related_obj)))
    for pbtmpitem in ptmpitem_related_obj:
        if pbtmpitem.prevtask:
            prevtask = pbtmpitem.prevtask.pk
        else:
            prevtask = "Start"
        if pbtmpitem.acttask:
            taskinfo = "%d - %s" % (pbtmpitem.pk, pbtmpitem.acttask.title)
        else:
            taskinfo = "%d - %s" % (pbtmpitem.pk, "N/A")
        # print("%s - %d - %d"%(taskinfo,pbtmpitem.itemorder,prevtask))
        alabel = "  %d [label=\"#%d: %s\"]\n" % (pbtmpitem.pk, pbtmpitem.itemorder, taskinfo)
        aitem = "  %s -> %s\n" % (prevtask, pbtmpitem.pk)
        graphfilecontents += alabel
        graphfilecontents += aitem
    graphfilecontents += "\n}\n}"
    # https://renenyffenegger.ch/notes/tools/Graphviz/examples/index
    try:
        (graph,) = pydot.graph_from_dot_data(graphfilecontents)
        pngfile = "pbtmp_%s.png"%(curr_pk)
        pngfilepath = path.join(MEDIA_ROOT, "graphs", pngfile)
        graph.write_png(pngfilepath)
        # print("H1")
    except Exception:
        errormsg = "Graphcreate exception %s" % (str(Exception))
        logger.error(errormsg)


@receiver(models.signals.post_delete, sender=PlaybookTemplateItem)
@transaction.atomic
def auto_save_PlaybookTemplate(sender, instance, **kwargs):
    playbooktemplate_obj=instance.playbooktemplateid
    playbooktemplate_obj.save()


@receiver(models.signals.post_save, sender=Playbook)
@transaction.atomic
def generate_graph_Playbook(sender, instance, **kwargs):
    """
    Generate playbooktemplate graph
    """
    curr_pk = instance.pk
    graphfilecontents = "digraph demo1 {\nsubgraph cluster_p {\nlabel = \"Playbook #"+str(curr_pk)+" - "+instance.name+"\"; \nnode [shape=record fontname=Arial];\nStart [shape=circle]\n"

    # ptmpitem_related_obj = PlaybookTemplateItem.objects.filter(playbooktemplateid=instance.pk)
    pitem_related_obj = instance.task_playbook.all()
    # print("Steps:%d" % (len(ptmpitem_related_obj)))
    for pitem in pitem_related_obj:
        if pitem.actiontarget:
            prevtask = pitem.actiontarget.pk
        else:
            prevtask = "Start"
        taskinfo = "%d - %s" % (pitem.pk, pitem.title)
        # print("%s - %d - %d" % (taskinfo,pbtmpitem.itemorder,prevtask))
        alabel = "  %d [label=\"%s\"]\n" % (pitem.pk, taskinfo)
        aitem = "  %s -> %s\n" % (prevtask, pitem.pk)
        graphfilecontents += alabel
        graphfilecontents += aitem
    graphfilecontents += "\n}\n}"
    # https://renenyffenegger.ch/notes/tools/Graphviz/examples/index
    try:
        (graph,) = pydot.graph_from_dot_data(graphfilecontents)
        pngfile = "pb_%s.png" % (curr_pk)
        pngfilepath = path.join(MEDIA_ROOT, "graphs", pngfile)
        graph.write_png(pngfilepath)
    except Exception:
        logger.error(Exception)


def add_task_from_template(atitle, astatus, aplaybook, auser, ainv, aaction, aactiontarget,
                           acategory, apriority, atype, asummary, adescription, arequiresevidence,
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
        requiresevidence=arequiresevidence,
        modified_by=amodified_by,
        created_by=acreated_by,
    )

    return obj


@transaction.atomic
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
            # save_relpath = upload_to_evidence(newev, pfilename)
            # save_path = path.join(MEDIA_ROOT, str(save_relpath))
            # handle_uploaded_file_chunks(pfileref , save_path)
            # newev.fileRef=save_relpath
            # newev.fileName=pfileref.name
            # newev.save()

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
            # save_relpath = upload_to_evidence(newev, pfilename)
            # save_path = path.join(MEDIA_ROOT, str(save_relpath))
            # handle_uploaded_file_chunks(pfileref , save_path)
            # newev.fileRef=save_relpath
            # newev.fileName=pfileref.name
            # newev.save()

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


def add_evattrintel(aseverity=None, aconfidence=None, astate=None, adate_last=None, aitype=None, asource=None,
                    aintelvalue=None, aevidenceattr=None, aintelsource=None, aforce=False):
    new_evattrintel = None
    if aforce is False:
        new_evattrintel = EvidenceAttrIntel.objects.update_or_create(
            severity=aseverity,
            confidence=aconfidence,
            state=astate,
            date_last=adate_last,
            itype=aitype,
            source=asource,
            intelvalue=aintelvalue,
            evidenceattr=aevidenceattr,
            intelsource=aintelsource
        )
        new_evattrintel = new_evattrintel[0]
    else:
        new_evattrintel = EvidenceAttrIntel.objects.create(
            severity=aseverity,
            confidence=aconfidence,
            state=astate,
            date_last=adate_last,
            itype=aitype,
            source=asource,
            intelvalue=aintelvalue,
            evidenceattr=aevidenceattr,
            intelsource=aintelsource
        )
    return new_evattrintel


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

@receiver(models.signals.post_save, sender=EvidenceAttr)
def check_ifcreated(sender, instance, **kwargs):
    created = False
    #Workaround to signal being emitted twice on create and save
    if 'created' in kwargs:
        if kwargs['created']:
            created=True
            # print("XXX created")
            run_auto_action_on_attribute(instance)
    #If signal is from object creation, return
    if created:
        return

# @receiver(models.signals.post_save, sender=Evidence)
# def check_if_malicious(sender, instance, **kwargs):
#     auser = instance.user
#     aactusername = str(instance.user)
#     aev_pk = instance.pk
#     aaevattr_pk = None
#     atask_pk = None
#     if instance.task:
#         atask_pk = instance.task.pk
#     else:
#         atask_pk = None
#     ainv_pk = None
#     if instance.inv:
#         ainv_pk = instance.inv.pk
#     else:
#         ainv_pk = None
#     aargdyn = kwargs.get('argdyn')
#     apattr = None
#     if Action.objects.get(title='Is Malicious?'):
#         aact_pk = Action.objects.get(title='Is Malicious?').pk
#         run_action(
#             pactuser=auser,
#             pactusername=aactusername,
#             pev_pk=aev_pk,
#             pevattr_pk=aaevattr_pk,
#             ptask_pk=atask_pk,
#             pact_pk=aact_pk,
#             pinv_pk=ainv_pk,
#             pargdyn=aargdyn,
#             pattr=apattr
#         )


@receiver(models.signals.post_save, sender=Evidence)
@transaction.atomic
def auto_make_readonly(sender, instance, **kwargs):
    """
    Make evidences read-only on the filesystem
    """
    if instance.fileRef:
        if os.path.isfile(instance.fileRef.path):
            #  This makes the files readonly
            os.chmod(instance.fileRef.path, S_IREAD | S_IRGRP | S_IROTH)

            # save filename
            # add_evattr(
            #     auser=instance.user,
            #     aev=Evidence.objects.get(pk=instance.pk),
                # aevattrvalue=instance.fileName,
                # aevattrformat=EvidenceAttrFormat.objects.get(pk=8),
                # amodified_by=instance.user.username,
                # acreated_by=instance.user.username,
                # aattr_automatic=True,
                # aattr_reputation=None,
                # aforce=False
            # )

            # add filename
            if instance.fileName:
                add_evattr(
                    auser=instance.user,
                    aev=Evidence.objects.get(pk=instance.pk),
                    aevattrvalue=instance.fileName,
                    aevattrformat=EvidenceAttrFormat.objects.get(pk=8),
                    amodified_by=instance.user.username,
                    acreated_by=instance.user.username,
                    aattr_automatic=True,
                    aattr_reputation=None,
                    aforce=False
                )
            # this one calculates the hash for the file
            res_md5 = FileHashCalc().md5sum(instance.fileRef.path)
            add_evattr(
                auser=instance.user,
                aev=Evidence.objects.get(pk=instance.pk),
                aevattrvalue=res_md5,
                aevattrformat=EvidenceAttrFormat.objects.get(pk=9),
                amodified_by=instance.user.username,
                acreated_by=instance.user.username,
                aattr_automatic=True,
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
                aattr_automatic=True,
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
                aattr_automatic=True,
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
                aattr_automatic=True,
                aattr_reputation=None,
                aforce=False
            )

# @receiver(models.signals.post_save, sender=EvidenceAttr)
# def auto_submit_ioc(sender, instance, **kwargs):
#     print("XXXX")


@receiver(models.signals.pre_save, sender=Evidence)
@transaction.atomic
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


@transaction.atomic
def run_action(pactuser, pactusername, pev_pk, pevattr_pk, ptask_pk, pact_pk, pinv_pk, pargdyn, pattr,
               pcheckmalicious=True, paddevattrintel=False, pnoclone=False):
    # print("XXXX %s "%paddevattrintel)
    actuser = pactuser  # self.request.user
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
    # if ev_pk == '0' or ev_pk == None:
    if ev_pk == '0' or ev_pk is None:
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

    # if ptask_pk == '0' or ptask_pk == None:
    if ptask_pk == '0' or ptask_pk is None:
        task_id = None
        task_obj = None
    else:
        task_id = ptask_pk
        task_obj = Task.objects.get(pk=task_id)
    if pact_pk != '0':
        actionid = pact_pk
    else:
        actionid = 0
    # if pinv_pk == '0' or pinv_pk == None:
    if pinv_pk == '0' or pinv_pk is None:
        inv_id = None
        inv_obj = None
    else:
        inv_id = pinv_pk
        inv_obj = Inv.objects.get(pk=inv_id)

    #  get the interpreter from the related table
    act_id = pact_pk
    action_obj = Action.objects.get(pk=act_id)
    action_outputtarget = action_obj.outputtarget.pk
    # automation_scripttype = action_obj.automation.script_type.pk
    # interpreter = ScriptType.objects.filter(action__automation_script_type__pk=act_id)[0].interpreter
    interpreter = action_obj.automationid.script_type.interpreter
    # cmd = action_obj.code_file_path
    cmd = None
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

    #  Create a temporary folder with the script in it
    #  generate a random folder with some prefix:
    myprefix = "EV-" + str(ev_pk) + "-" + str(evattr_pk) + "-"
    mytempdir = tempfile.TemporaryDirectory(prefix=myprefix)
    #  make the tempdir the temp root
    tempfile.tempdir = mytempdir.name
    # with tempfile.TemporaryDirectory() as directory:
    # 2. copy script into temp folder
    # srcfile = path.join(MEDIA_ROOT, cmd)
    # destdir = mytempdir.name
    # destfile_clean = os.path.join(destdir, re.escape(oldev_file_name))
    # destfile = os.path.join(destdir, oldev_file_name)
    # I have used the renamed file because the Popen had issues with the special chars
    # and spaces in filenames...
    # destfile = os.path.join(destdir, os.path.basename(cmd))
    # copy(srcfile, destfile)
    # print("SRCFILE:%s" % (srcfile))
    # print("DSTFILE:%s" % (destfile))
    newname = str(act_id)+"_"
    newscript = tempfile.NamedTemporaryFile(mode='w+t', prefix=newname)
    # Put the code into the temp file from action code
    putintofile = action_obj.automationid.code  # .\
    #    replace('echo', '#echo')#.\
    #    replace('$FILE$', destfile)
    # replace('$EVIDENCE$', destfile)
    # replace('$OUTDIR$', destfile)

    connectionitemfields = ConnectionItemField.objects.filter(connectionitemid=action_obj.connectionitemid)
    if connectionitemfields:
        for connitemfield in connectionitemfields:
            if connitemfield:
                # replace the connection item names with the values
                # the scripts should contain the same names case sensitive
                # bordered by "$" signs
                fieldname = connitemfield.connectionitemfieldname
                replacethis = "$%s$" % fieldname
                if connitemfield.encryptvalue:
                    fieldvalue = decrypt_string(connitemfield.connectionitemfieldvalue)
                    putintofile = putintofile.replace(replacethis, fieldvalue)
                else:
                    fieldvalue = connitemfield.connectionitemfieldvalue
                    putintofile = putintofile.replace(replacethis, fieldvalue)
    if newscript:
        cmd = newscript.name

        newscript.writelines(putintofile)
        newscript.seek(0)
        # print(newscript.name)
        # print(newscript.read())
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
            if action_obj.automationid.type.pk == 4:
                #  b64 encrypted values
                argument_cleartext = argument.replace('$EVIDENCE$', desc)
                argument = argument.replace('$EVIDENCE$', b64encode(desc.encode()).decode())
            else:
                argument = argument.replace('$EVIDENCE$', desc)
                argument_cleartext = argument
            if action_obj.outputtarget.name == 'File':
                # this means the output is a file
                # generate a random folder with some prefix:
                myprefix = "EV-" + str(ev_pk) + "-"
                myouttempdir = tempfile.TemporaryDirectory(prefix=myprefix)
                #  make the tempdir the temp root
                tempfile.tempdir = myouttempdir.name
                # with tempfile.TemporaryDirectory() as directory:
                destdir = myouttempdir.name
                # argument replace the $OUTDIR$ with the standard dir where output files will be stored
                destoutdir = tempfile.mkdtemp()
                destoutdirname = str(destoutdir) + "/"
                argument = argument.replace('$OUTDIR$', destoutdirname)
        elif action_obj.scriptinput.pk == 2 and oldev_file:
            # this represents file type so reads the file from the evidence
            # need to have a file to work on, that's "2"
            # create a temporary file so the original remains intact
            # generate a random folder with some prefix:
            # myprefix = "EV-"+str(ev_pk)+"-"
            # mytempdir = tempfile.TemporaryDirectory(prefix=myprefix)
            # make the tempdir the temp root
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

    scripttype = action_obj.automationid.script_type
    actionq_startid = None
    results = ""
    if action_obj.automationid.type.pk == 1:  # Command
        # /bin/bash -c "`cat /tmp/cmd` -c3 8.8.8.8"
        # need to run as a command, later probably need to use interpreter...or something
        cmd = action_obj.automationid.code
        results = run_script_class("", cmd, argument, timeout).runcmd()
        pass
    elif action_obj.automationid.type.pk == 2:  # Executable
        pass
    elif action_obj.automationid.type.pk == 3:  # Script
        results = run_script_class(interpreter, cmd, argument, timeout).runscript()
    elif action_obj.automationid.type.pk == 4:  # Script with b64 encrypted values to pass over
        results = run_script_class(interpreter, cmd, argument, timeout).runscript()
    elif action_obj.automationid.type.pk == 5:  # Internal command
        afuncoutput = None
        if action_obj.automationid.code == "add_all_to_profile":
            from assets.models import new_create_profile_from_evattrs_all
            new_create_profile_from_evattrs_all(pev=ev_pk)
            afuncoutput = "adding evidence %s attributes to the profile " % ev_pk
        else:
            from tasks.scripts import String_Parser
            sp1 = String_Parser.StringParser
            afuncoutput = getattr(sp1, action_obj.automationid.code)('', argument)
            if action_obj.automationid.code == "check_malicious":
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
            # if action_obj.automationid.code == "StringParser.extract_ipv4":
            #     pass

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
    # resoutputl = None
    if action_obj.scriptoutput:
        try:
            if action_obj.scriptoutput.name == "List":
                from ast import literal_eval
                resoutput = literal_eval(resoutput)
            if action_obj.scriptoutput.delimiter:
                resoutput = OutputProcessor().split_delimiter(resoutput, action_obj.scriptoutput.delimiter)
        except:
            resoutput = "ERROR in parsing output"
            reserror = "Cannot parse output"
        finally:
            pass
    # save action to the actionQ

    actionq_stopid=None
    evid = None
    actq = None
    # if argumentoutput == "None"
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
        # print("Here2")
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
        # print("EVID: %s" % (evid))
        # Add an attribute with reputation
        if pcheckmalicious and ismalicious:
            # setobservable = False
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
            # print("XX noclone: %s"%pnoclone)
            # disabled cloning
            # if not pnoclone:
            #     # Creating a clone for the attribute item inspected
            #     if oldev_obj.parentattr:
            #         cloneevidattr = oldev_obj.parentattr
            #         # defuning PK as none will make sure a new item is created
            #         cloneevidattr.pk = None
            #         if cloneevidattr.evreputation.name == 'Suspicious' or cloneevidattr.evreputation.name == 'Malicious':
            #             cloneevidattr.observable = True
            #         cloneevidattr.attr_reputation = attr_rep
            #         newclone = cloneevidattr.save()

        if paddevattrintel:
            # print("XXXX TBD add intel to the EvidenceAttrIntel")
            # testtime = '2020-01-01T11:22:33'
            # if it is empty, it will not add the results...
            if resoutput:
                outstr_0 = resoutput.rstrip()[1:][:-1].replace("\'", "\"")
                outstr = json.loads(outstr_0)
                date_format = "%Y-%m-%dT%H:%M:%S"
                mytimestamp = datetime.strptime(outstr['date_last'], date_format)
                # naive_datetime = datetime.datetime.now()
                # naive_datetime.tzinfo  # None

                # settings.TIME_ZONE  # 'UTC'
                aware_datetime = make_aware(mytimestamp)
                date_last = aware_datetime
                # print(aware_datetime.tzinfo)  # <UTC>

                add_evattrintel(
                    aseverity=outstr['severity'],
                    aconfidence=outstr['confidence'],
                    astate=outstr['state'],
                    adate_last=date_last,
                    aitype=outstr['itype'],
                    asource=outstr['source'],
                    aintelvalue=outstr['value'],
                    aevidenceattr=evattr_obj,
                    aintelsource="%s-%s" % (action_obj.pk, action_obj.title),
                    aforce=True
                )
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
        if action_obj.automationid.code == 'check_malicious':
            currevattrformat = EvidenceAttrFormat.objects.get(name='Reputation')
        else:
            currevattrformat = EvidenceAttrFormat.objects.get(name='Unknown')
            if action_obj.scriptoutputtype:
                currevattrformat = EvidenceAttrFormat.objects.get(pk=action_obj.scriptoutputtype.pk)

        # if EvidenceAttrFormat.objects.get(name=argumentoutput):
        #     currevattrformat = EvidenceAttrFormat.objects.get(name=argumentoutput)
        # resoutput.split()
        # OUTPUT DELIMITER needs to be defined in the model - if empty, don't split...TBD
        print("XXX we are here but why")
        if isinstance(resoutput, list) or isinstance(resoutput, tuple):
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
        elif (isinstance(resoutput, str)):
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
                                             action_obj.title, scripttype, rescommand, argument_cleartext,
                                             argumentdynamic, reserror, resstatus, resoutput, respid,
                                             ActionQStatus.objects.get(name="Finished"), actuser)
                # update the actionQ with the parent value
                ActionQ.objects.filter(pk=actionq_startid.pk).update(parent=actionq_stopid)

                # copy files to the evidences folder
                evfolder = 'uploads/evidences'
                srcfilename1 = os.path.join(destoutdirname, fname)
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
                if check_file_type(os.path.join(MEDIA_ROOT, imgurl1)) == 'image':
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
    newscript.close()

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, blank=True, null=True,
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
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="actionq_parent")
    title = models.CharField(max_length=50, default=None, blank=True, null=True)
    scripttype = models.CharField(max_length=60, blank=False, null=False)
    command = models.CharField(max_length=2048, blank=False, null=False)
    argument = models.CharField(max_length=4096, default=None, blank=True, null=True)
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

class TasksInvDetailTabEvidences():

    def inv_tab_evidences_actions(self):
        retval = Action.objects.exclude(enabled=False) \
            .exclude(automationid__isnull=True) \
            .select_related('scriptinput') \
            .select_related('outputtarget') \
            .select_related('scriptinputattrtype') \
            .order_by('title')
        return retval

    def inv_tab_evidences_taskreadonly(self, ev_pk):
        retval = False
        if Evidence.objects.filter(pk=ev_pk).task:
            if Evidence.objects.filter(pk=ev_pk).task.pk:
                retval = True
        return retval


def get_actionq_list_by_evidence(ev):
    retval = ActionQ.objects.none()
    if ev:
        retval = ActionQ.objects.filter(evid=ev)
    return retval

def get_attribute_list_by_evidence(ev):
    retval = EvidenceAttr.objects.none()
    if ev:
        retval = EvidenceAttr.objects.filter(ev__pk=ev)\
            .select_related('attr_reputation')\
            .select_related('evattrformat')
    return retval


def get_attribute_list_by_evidence_values(ev):
    retval = EvidenceAttr.objects.none()
    if ev:
        retval = EvidenceAttr.objects.filter(ev__pk=ev)\
            .select_related('attr_reputation__pk')\
            .select_related('attr_reputation__name')\
            .select_related('evattrformat__pk')\
            .select_related('evattrformat__name')\
            .values('pk',
                    'attr_reputation__pk',
                    'attr_reputation__name',
                    'evattrformat__pk',
                    'evattrformat__name', 'observable', 'evattrvalue', 'ev__pk', 'modified_at')
    return retval


def get_attribute_intel_list_by_pk(attr_pk):
    retval = EvidenceAttr.objects.none()
    if attr_pk:
        retval = EvidenceAttrIntel.objects.filter(evidenceattr=attr_pk).order_by('date_last').reverse()
    return retval


class FileHashCalc():
    def __init__(self):
        # self.myfile=pfile
        pass

    def md5sum(self, filename):
        h = hashlib.md5()
        b = bytearray(128*1024)
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda: f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()

    def sha1sum(self, filename):
        h = hashlib.sha1()
        b = bytearray(128*1024)
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda: f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()

    def sha256sum(self, filename):
        h = hashlib.sha256()
        b = bytearray(128*1024)
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda: f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()

    def sha512sum(self, filename):
        h = hashlib.sha512()
        b = bytearray(128*1024)
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda: f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()

    # res_md5 = FileHashCals().md5sum('FilePath')

# def add_to_profile(pevattr):
#     print(pevattr)


# managing chunked uploads
def handle_uploaded_file_chunks(pfile, ppath):
    with open(ppath, 'wb+') as destination:
        for chunk in pfile.chunks():
            destination.write(chunk)

def taskreadonly(task_str):
    if task_str == 'Completed' or task_str == 'Skipped':
        return True
    else:
        return False

def taskcompleted(task_str):
    if task_str == 'Completed':
        return True
    else:
        return False

def evidencereadonly(ev_pk):
    # evtask = Evidence.objects.filter(pk=int(ev_pk)) #.select_related('task__status__name').values('task__status__name')
    # print(type(evtask['task__status__name']))
    evtask = Evidence.objects.filter(pk=ev_pk).select_related('task__status__name').values('task__status__name')
    if evtask:
        retval = taskreadonly(evtask.first()['task__status__name'])
    else:
        retval = False
    return retval

class TaskList():
    def get_tasklist(self, pinv, pexcltask, pallownull=False, porder_by='pk', preadonly=None):
        task_obj = None
        if pinv != '0':
            if pexcltask:
                task_objs = Task.objects.filter(inv__pk=pinv)\
                    .exclude(pk=pexcltask)\
                    .select_related('inv__pk') \
                    .select_related('status__name') \
                    .values_list('pk', 'inv__pk', 'title', 'status__name').order_by(porder_by)
            else:
                task_objs = Task.objects.filter(inv__pk=pinv)\
                    .select_related('inv__pk') \
                    .select_related('status__name') \
                    .values_list('pk', 'inv__pk', 'title','status__name').order_by(porder_by)
        else:
            if pexcltask:
                task_objs = Task.objects.exclude(pk=pexcltask)\
                    .select_related('inv__pk') \
                    .select_related('status__name') \
                    .values_list('pk', 'inv__pk', 'title', 'status__name').order_by(porder_by)
            else:
                task_objs = Task.objects.select_related('inv__pk') \
                    .select_related('status__name') \
                    .values_list('pk', 'inv__pk', 'title', 'status__name').order_by(porder_by)
        outlist = list()
        if pallownull:
            outlist.append(('', 'None'))
        NoneType = type(None)
        if task_objs.exists():
            for task in task_objs:
                if preadonly is True:
                    areadonly = taskreadonly(task[3])
                else:
                    areadonly = False
                if type(task[1]) != NoneType and areadonly:
                    outstr = "%s-%s (%s)" % (int(task[0]), str(task[2]), str(task[1]))
                else:
                    outstr = "%s-%s (%s)" % (int(task[0]), str(task[2]), "NA")
                if not taskreadonly(task[3]):
                    outlist.append((task[0], outstr))
        return outlist

    def get_taskstatuslist(self, anew=False):
        retval = None
        if anew:
            retval = TaskStatus.objects.exclude(name="Completed").values_list('pk', 'name').order_by('pk')
        else:
            retval = TaskStatus.objects.values_list('pk', 'name').order_by('pk')
        return retval

    def get_actionlist(self, pallownull=True, porderby='title'):
        act_objs = Action.objects.filter(enabled=True).select_related('scriptinput__shortname')\
            .select_related('outputtarget__shortname')\
            .values_list('pk', 'title', 'scriptinput__shortname', 'outputtarget__shortname', 'automationid')\
            .order_by(porderby)
        outlist = list()
        if pallownull:
            outlist.append(('', 'None'))
        if act_objs.exists():
            for act in act_objs:
                outstr = "%s (%s: %s->%s)" % (str(act[1]), str(act[0]), str(act[2]), str(act[3]))
                outlist.append((act[0], outstr))
        return outlist