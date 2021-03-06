# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : tasks/view.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : View file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# 2019.09.06  Lendvay     2      Added session security
# 2020.05.16  Lendvay     3      taskstatuslist excluded Completed in newtask, so a task cannot be created as completed
# 2020.06.12  Lendvay     2      Attribute filters
# **********************************************************************;
from .models import Task, TaskTemplate, TaskType, TaskPriority, TaskCategory, TaskStatus
from .models import TaskVar, TaskList  # , TaskVarType, TaskVarCategory
from .models import Playbook, PlaybookTemplate, PlaybookTemplateItem, new_playbook, actiongroupmember_items
from invs.models import InvDetailTabEvidences, Inv, InvList
from .models import TasksInvDetailTabEvidences
# from .models import Inv
from .models import Evidence, EvidenceAttr  # , EvidenceAttrFormat, EvidenceFormat
from .models import add_task_from_template, run_action, evidenceattrobservabletoggle, clone_action, \
    new_evidence, evidenceattrmalicioustoggle
from .models import Action, ActionQ, ActionGroup, ActionGroupMember, Automation
from tasks.models import playbooktemplateitem_check_delete_condition
from .forms import TaskForm, TaskTemplateForm, TaskVarForm, AddTicketAndCloseForm
from .forms import ActionForm, ActionGroupForm, ActionGroupMemberForm, AutomationForm
from .forms import EvidenceAttrForm, EvidenceForm
from .forms import PlaybookForm, PlaybookTemplateForm, PlaybookTemplateItemForm
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse # , get_object_or_404  # ,render,
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import FileResponse
# from django.shortcuts import get_object_or_404
from django.views import generic
# from django.forms.widgets import SplitDateTimeWidget  # , ClearableFileInput
import logging
from bCIRT.custom_variables import BCIRT_MEDIA_ROOT
from bCIRT.settings import ALLOWED_HOSTS
# check remaining session time
# from django.contrib.sessions.models import Session
# from datetime import timezone
# check remaining session time
from django.utils.http import is_safe_url
import os
from io import BytesIO
from datetime import datetime
import zipfile
from django.http import HttpResponse
from .resources import PlaybookTemplateResource, PlaybookTemplateItemResource, TaskTemplateResource, TaskVarResource,\
    ActionResource, AutomationResource
from bCIRT.settings import MEDIA_ROOT
from shutil import copy
import tempfile
from bCIRT.custom_variables import LOGLEVEL, LOGSEPARATOR
from django.contrib.auth import get_user_model
User = get_user_model()
logger = logging.getLogger('log_file_verbose')


#  ##### Export functions start ######
class PlaybookTemplateExportView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    # context = {"title": "Task evidences"}  # data that has to be rendered to pdf templete
    model = PlaybookTemplate
    permission_required = ('tasks.view_playbooktemplate', 'tasks.view_playbooktemplateitem', 'tasks.view_evidence', 'tasks:view_task')
    context = {"title": "PlaybookTemplates"}
    outdiract = None  #'/tmp/export/actions'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookTemplateExportView, self).__init__(*args, **kwargs)

    def download_dir_zipped(self, p_dir):
        in_memory = BytesIO()
        os.chdir(os.path.dirname(p_dir))
        with zipfile.ZipFile(in_memory,
                             "w",
                             zipfile.ZIP_DEFLATED,
                             allowZip64=True) as zf:
            for root, _, filenames in os.walk(os.path.basename(p_dir)):
                for name in filenames:
                    name = os.path.join(root, name)
                    name = os.path.normpath(name)
                    zf.write(name, name)
        return in_memory

    def save_to_file(self, a_dir, a_filename, a_content):
        destpath = os.path.join(a_dir, a_filename)
        try:
            with open(destpath, "w") as outfile:
                outfile.write(a_content)
            outfile.close()
        except IOError:
            print('Error occured while trying to write file: ' + destpath)

    def get(self, request, *args, **kwargs):
        self.context['playbooktemplate'] = self.get_object()
        self.context['user'] = self.request.user.get_username()
        # response = None
        # Collecting playbooktemplate values
        pbtmp_pk = str(self.get_object().pk)

        # 1. create temp folder
        tempfile.tempdir = os.path.join(MEDIA_ROOT, "tmp")
        # generate a random folder with some prefix:
        myprefix = "Export-PlayBookTemplate-" + str(pbtmp_pk) + "-"
        mytempdir = tempfile.TemporaryDirectory(prefix=myprefix)
        #  make the tempdir the temp root
        tempfile.tempdir = mytempdir.name
        # with tempfile.TemporaryDirectory() as directory:
        destdir = mytempdir.name
        destactdir = os.path.join(destdir, 'actions')
        os.makedirs(destactdir, exist_ok=True)

        playbooktemplate_resource = PlaybookTemplateResource()
        pbtmp_obj = PlaybookTemplate.objects.filter(pk=pbtmp_pk)
        pbtmp_dataset = playbooktemplate_resource.export(pbtmp_obj)
        self.save_to_file(a_dir=destdir, a_filename='PlaybookTemplate.json',
                          a_content=pbtmp_dataset.json)
        # Exporting values PlaybookTemplate
        # response = HttpResponse(pbtmp_dataset.json, content_type='application/json')
        # response['Content-Disposition'] = 'attachment; filename="PlaybookTemplate.json"'

        playbooktemplateitem_resource = PlaybookTemplateItemResource()
        # pbtmpitem_obj = PlaybookTemplateItem.objects.filter(playbooktemplateid=pbtmp_pk)
        pbtmpitem_obj = pbtmp_obj[0].playbooktemplateitem_playbooktemplate.all()
        pbtmpitem_dataset = playbooktemplateitem_resource.export(pbtmpitem_obj)
        self.save_to_file(a_dir=destdir, a_filename='PlaybookTemplateItem.json',
                          a_content=pbtmpitem_dataset.json)
        # Exporting values PlaybookTemplateItem
        # response = HttpResponse(pbtmpitem_dataset.json, content_type='application/json')
        # response['Content-Disposition'] = 'attachment; filename="PlaybookTemplateItem.json"'

        # Iterate through the playbooktemplateitems and find the tasktemplates needed
        # can be acttask, prevtask, nexttask
        # define an empty queryset
        tsktmp_objset = TaskTemplate.objects.none()
        tasktemplate_resource = TaskTemplateResource()
        if pbtmpitem_obj:
            for pbtmpitemsingle_obj in pbtmpitem_obj:
                if pbtmpitemsingle_obj.acttask:
                    pbtmpitem_acttask = pbtmpitemsingle_obj.acttask.pk
                    tsktmp_obj = TaskTemplate.objects.filter(pk=pbtmpitem_acttask)
                    # collect all the tasktemplates into the same queryset
                    tsktmp_objset = tsktmp_objset | tsktmp_obj

                if pbtmpitemsingle_obj.prevtask:
                    pbtmpitem_prevtask = pbtmpitemsingle_obj.prevtask.pk
                    tsktmp_obj = TaskTemplate.objects.filter(pk=pbtmpitem_prevtask)
                    # collect all the tasktemplates into the same queryset
                    tsktmp_objset = tsktmp_objset | tsktmp_obj

                if pbtmpitemsingle_obj.nexttask:
                    pbtmpitem_nexttask = pbtmpitemsingle_obj.nexttask.pk
                    tsktmp_obj = TaskTemplate.objects.filter(pk=pbtmpitem_nexttask)
                    # collect all the tasktemplates into the same queryset
                    tsktmp_objset = tsktmp_objset | tsktmp_obj

            # generate the dataset for export
            tsktmp_dataset = tasktemplate_resource.export(tsktmp_objset)
            self.save_to_file(a_dir=destdir, a_filename='TaskTemplate.json',
                              a_content=tsktmp_dataset.json)
            # Exporting values PlaybookTemplateItem
            # response = HttpResponse(tsktmp_dataset.json, content_type='application/json')
            # response['Content-Disposition'] = 'attachment; filename="TaskTemplate.json"'
        tskvar_objset = TaskVar.objects.none()
        taskvar_resource = TaskVarResource()
        if tsktmp_objset:
            for tsktmp_single_obj in tsktmp_objset:
                if tsktmp_single_obj:
                    tsktmp_pk = tsktmp_single_obj.pk
                    tskvar_obj = TaskVar.objects.filter(pk=tsktmp_pk)
                    tskvar_objset = tskvar_objset | tskvar_obj
        # generate the dataset for export
        tskvar_dataset = taskvar_resource.export(tskvar_objset)
        self.save_to_file(a_dir=destdir, a_filename='TaskVar.json', a_content=tskvar_dataset.json)
        # Exporting values PlaybookTemplateItem
        # response = HttpResponse(tskvar_dataset.json, content_type='application/json')
        # response['Content-Disposition'] = 'attachment; filename="TaskVar.json"'

        # export ACTION
        act_objset = Action.objects.none()
        action_resource = ActionResource()
        if tsktmp_objset:
            for tsktmp_single_obj in tsktmp_objset:
                if tsktmp_single_obj:
                    if tsktmp_single_obj.action:
                        act_pk = tsktmp_single_obj.action.pk
                        act_obj = Action.objects.filter(pk=act_pk)
                        act_objset = act_objset | act_obj
                        if act_obj[0].fileRef:
                            srcfile = os.path.join(str(MEDIA_ROOT), str(act_obj[0].fileRef))
                            destfile = os.path.join(destactdir, os.path.basename(str(act_obj[0].fileRef)))
                            copy(srcfile, destfile)
        # generate the dataset for export
        act_dataset = action_resource.export(act_objset)
        self.save_to_file(a_dir=destdir, a_filename='Action.json', a_content=act_dataset.json)

        # getting the automations
        auto_objset = Automation.objects.none()
        auto_resource = AutomationResource()
        if act_objset:
            for act_objitem in act_objset:
                if act_objitem.automationid:
                    auto_obj = Automation.objects.filter(pk=act_objitem.automationid.pk)
                    auto_objset = auto_objset | auto_obj
                    if auto_obj[0].fileRef:
                        srcfile = os.path.join(str(MEDIA_ROOT), str(auto_obj[0].fileRef))
                        destfile = os.path.join(destactdir, os.path.basename(str(auto_obj[0].fileRef)))
                        copy(srcfile, destfile)
        auto_dataset = auto_resource.export(auto_objset)
        self.save_to_file(a_dir=destdir, a_filename='Automation.json', a_content=auto_dataset.json)

        # Exporting values Action
        # response = HttpResponse(act_dataset.json, content_type='application/json')
        # response['Content-Disposition'] = 'attachment; filename="Action.json"'
        # response = redirect('tasks:playtmp_list')
        # return response

        zipfile_memory = self.download_dir_zipped(destdir)
        zip_filename = "Export-PlayBookTemplate-" + str(pbtmp_pk) + ".zip"
        # Grab ZIP file from in-memory, make response with correct MIME-type
        resp = HttpResponse(content_type="application/x-zip-compressed")
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

        zipfile_memory.seek(0)

        resp.write(zipfile_memory.read())

        return resp

# ##### Export functions end ######
# class GetPlaybookTemplateZippedView(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
#     permission_required = ('tasks.view_playbooktemplate','tasks.view_playbooktemplateitem','tasks.view_tasktemplate',
#     'tasks.view_taskvar')
#     context = {"title": "Directory Zipped Download"}
#     pass


class GetFileRawView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Evidence
    permission_required = ('tasks.view_evidence')
    context = {"title": "Evidence Download"}

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(GetFileRawView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        ev_pk = self.kwargs.get('ev_pk')
        # fileName = None
        # filepath = None
        # fullpath = None
        http_response = HttpResponse('Record not found!!!')
        try:
            if Evidence.objects.filter(pk=ev_pk).exists():
                origfilename = str(Evidence.objects.get(pk=ev_pk).fileName)
                filepath = str(Evidence.objects.get(pk=ev_pk).fileRef)
                fileroot = str(BCIRT_MEDIA_ROOT)
                fullpath = os.path.join(fileroot, filepath)

                now = datetime.now()
                # date_time = now.strftime("%Y%m%d-%H%M%S")
                if filepath is not None:
                    http_response = FileResponse(open(fullpath, "rb"))
                    http_response['Content-Disposition'] = 'attachment; filename="%s"' % origfilename
                    # self.download_file_zipped("Evidence_"+ev_pk+"_"+date_time, fullpath, origfilename)
        except:
            pass
        # http_response = HttpResponse("Result:"+fullpath, content_type="text/plain")
        # print(fileName)
        return http_response


class GetFileZippedView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Evidence
    permission_required = 'tasks.view_evidence'
    context = {"title": "Evidence Download"}

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(GetFileZippedView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        ev_pk = self.kwargs.get('ev_pk')
        # fileName = None
        # filepath = None
        # fullpath = None
        http_response = HttpResponse('Record not found!!!')

        try:
            if Evidence.objects.filter(pk=ev_pk).exists():
                origfilename = str(Evidence.objects.get(pk=ev_pk).fileName)
            # self.context['ev_pk'] = self.get_object()
            # self.context['user'] = self.request.user.get_username()
                filepath = str(Evidence.objects.get(pk=ev_pk).fileRef)
                fileroot = str(BCIRT_MEDIA_ROOT)
                fullpath = os.path.join(fileroot, filepath)

                now = datetime.now()
                date_time = now.strftime("%Y%m%d-%H%M%S")
                if filepath is not None:
                    http_response = self.download_file_zipped("Evidence_"+ev_pk+"_"+date_time, fullpath, origfilename)
        except:
            pass
        # http_response = HttpResponse("Result:"+fullpath, content_type="text/plain")
        # print(fileName)
        return http_response

    def download_file_zipped(self, pprefix, pfilepath, pzip_filename):
        fpath = pfilepath
        # Folder name in ZIP archive
        # E.g [myfile.zip]/somefiles/file1.txt
        zip_subdir = pprefix
        # zip filename
        # zip_filename = None
        if pzip_filename is not None:
            zip_filename = pzip_filename+".zip"
        else:
            zip_filename = "%s.zip" % zip_subdir
        # Open BytesIO to grab in-memory ZIP contents
        in_memory = BytesIO()

        # The zip compressor
        zf = zipfile.ZipFile(in_memory, "w")

        zip_path = os.path.join(zip_subdir, pzip_filename)

        try:
            # Add file, at correct path
            zf.write(fpath, zip_path)
            # fix for Linux zip files read in Windows
            for file in zf.filelist:
                file.create_system = 0
        finally:
            # Must close zip for all contents to be written
            zf.close()
        # Grab ZIP file from in-memory, make response with correct MIME-type
        resp = HttpResponse(content_type="application/x-zip-compressed")
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename="%s"' % zip_filename
        in_memory.seek(0)
        resp.write(in_memory.read())

        return resp


# Create your views here.
# #############################################################################3
class AutomationListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Automation
    form_class = AutomationForm
    permission_required = ('tasks.view_automation',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(AutomationListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(AutomationListView, self).get_context_data(**kwargs)


# @method_decorator(csrf_exempt, name='dispatch')
class AutomationCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    #  fields = ("inv", "user", "description", "fileRef")
    model = Automation
    form_class = AutomationForm
    permission_required = ('tasks.add_automation',)
    success_url = 'tasks:auto_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(AutomationCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(AutomationCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.modified_by = self.request.user.get_username()
        self.object.created_by = self.request.user.get_username()
        if self.request.FILES:
            self.object.fileName = self.request.FILES['fileRef'].name
        self.object.save()
        return super(AutomationCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_automation'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('tasks:auto_list')
        # Checks pass, let http method handlers process the request
        return super(AutomationCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(AutomationCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class AutomationDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Automation
    permission_required = ('tasks.view_automation',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(AutomationDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(AutomationDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.view_automation'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('tasks:auto_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(AutomationDetailView, self).dispatch(request, *args, **kwargs)


# @method_decorator(csrf_exempt, name='dispatch')
class AutomationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    # redirect_field_name = 'tasks/evidence_detail.html'
    form_class = AutomationForm
    model = Automation
    permission_required = ('tasks.change_automation',)
    success_url = 'tasks:auto_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(AutomationUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(AutomationUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_automation'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:auto_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(AutomationUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        if self.request.FILES:
            self.object.fileName = self.request.FILES['fileRef'].name
        self.object.save()
        return super(AutomationUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(AutomationUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class AutomationRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Automation
#    success_url = reverse_lazy('tasks:ev_list')
    permission_required = ('tasks.delete_automation', 'tasks.view_automation',)
    success_url = 'tasks:auto_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(AutomationRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(AutomationRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.delete_automation'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('tasks:auto_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(AutomationRemoveView, self).dispatch(request, *args, **kwargs)


# ##############################################################################
class ActionListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Action
    form_class = ActionForm
    permission_required = ('tasks.view_action',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(ActionListView, self).get_context_data(**kwargs)


# @method_decorator(csrf_exempt, name='dispatch')
class ActionCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    #  fields = ("inv", "user", "description", "fileRef")
    model = Action
    form_class = ActionForm
    permission_required = ('tasks.add_action',)
    success_url = 'tasks:act_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(ActionCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.modified_by = self.request.user.get_username()
        self.object.created_by = self.request.user.get_username()
        if self.request.FILES:
            self.object.fileName = self.request.FILES['fileRef'].name
        self.object.save()
        return super(ActionCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_action'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('tasks:act_list')
        # Checks pass, let http method handlers process the request
        return super(ActionCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(ActionCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class ActionDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Action
    permission_required = ('tasks.view_action',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(ActionDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.view_action'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('tasks:act_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ActionDetailView, self).dispatch(request, *args, **kwargs)


# @method_decorator(csrf_exempt, name='dispatch')
class ActionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    # redirect_field_name = 'tasks/evidence_detail.html'
    form_class = ActionForm
    model = Action
    permission_required = ('tasks.change_action',)
    success_url = 'tasks:act_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(ActionUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_action'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:act_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ActionUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        if self.request.FILES:
            self.object.fileName = self.request.FILES['fileRef'].name
        self.object.save()
        return super(ActionUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(ActionUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class ActionRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Action
#    success_url = reverse_lazy('tasks:ev_list')
    permission_required = ('tasks.delete_action', 'tasks.view_action',)
    success_url = 'tasks:act_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(ActionRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.delete_action'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('tasks:act_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ActionRemoveView, self).dispatch(request, *args, **kwargs)


class ActionQDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = ActionQ
    permission_required = ('tasks.view_actionq',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionQDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(ActionQDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.view_actionq'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('tasks:act_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ActionQDetailView, self).dispatch(request, *args, **kwargs)


# ActionGroups
class ActionGroupListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = ActionGroup
    form_class = ActionGroupForm
    permission_required = ('tasks.view_actiongroup',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionGroupListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(ActionGroupListView, self).get_context_data(**kwargs)


class ActionGroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    #  fields = ("inv", "user", "description", "fileRef")
    model = ActionGroup
    form_class = ActionGroupForm
    permission_required = ('tasks.add_actiongroup',)
    success_url = 'tasks:actgrp_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionGroupCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(ActionGroupCreateView, self).get_context_data(**kwargs)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     return super(ActionGroupCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_actiongroup'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('tasks:actgrp_list')
        # Checks pass, let http method handlers process the request
        return super(ActionGroupCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        # grab the current set of form #kwargs
        kwargs = super(ActionGroupCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class ActionGroupDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = ActionGroup
    permission_required = ('tasks.view_actiongroup',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionGroupDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(ActionGroupDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.view_actiongroup'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('tasks:actgrp_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ActionGroupDetailView, self).dispatch(request, *args, **kwargs)


class ActionGroupUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    # redirect_field_name = 'tasks/evidence_detail.html'
    form_class = ActionGroupForm
    model = ActionGroup
    permission_required = ('tasks.change_actiongroup',)
    success_url = 'tasks:actgrp_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionGroupUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(ActionGroupUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_actiongroup'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:actgrp_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ActionGroupUpdateView, self).dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     return super(ActionGroupUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        # grab the current set of form #kwargs
        kwargs = super(ActionGroupUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class ActionGroupRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = ActionGroup
#    success_url = reverse_lazy('tasks:ev_list')
    permission_required = ('tasks.delete_actiongroup', 'tasks.view_actiongroup',)
    success_url = 'tasks:actgrp_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionGroupRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(ActionGroupRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.delete_actiongroup'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('tasks:actgrp_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ActionGroupRemoveView, self).dispatch(request, *args, **kwargs)


# ActionGroupMembers
class ActionGroupMemberListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = ActionGroupMember
    form_class = ActionGroupMemberForm
    permission_required = ('tasks.view_actiongroupmember',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionGroupMemberListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(ActionGroupMemberListView, self).get_context_data(**kwargs)


class ActionGroupMemberCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    #  fields = ("inv", "user", "description", "fileRef")
    model = ActionGroupMember
    form_class = ActionGroupMemberForm
    permission_required = ('tasks.add_actiongroupmember',)
    success_url = 'tasks:actgrpmem_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionGroupMemberCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(ActionGroupMemberCreateView, self).get_context_data(**kwargs)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     return super(ActionGroupCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_actiongroupmember'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('tasks:actgrpmem_list')
        # Checks pass, let http method handlers process the request
        return super(ActionGroupMemberCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        # grab the current set of form #kwargs
        kwargs = super(ActionGroupMemberCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class ActionGroupMemberDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = ActionGroupMember
    permission_required = ('tasks.view_actiongroupmember',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionGroupMemberDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(ActionGroupMemberDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.view_actiongroup'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('tasks:actgrp_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ActionGroupMemberDetailView, self).dispatch(request, *args, **kwargs)


class ActionGroupMemberUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    # redirect_field_name = 'tasks/evidence_detail.html'
    form_class = ActionGroupMemberForm
    model = ActionGroupMember
    permission_required = ('tasks.change_actiongroupmember',)
    success_url = 'tasks:actgrpmem_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionGroupMemberUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(ActionGroupMemberUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_actiongroupmember'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:actgrpmem_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ActionGroupMemberUpdateView, self).dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     return super(ActionGroupUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        # grab the current set of form #kwargs
        kwargs = super(ActionGroupMemberUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class ActionGroupMemberRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = ActionGroupMember
#    success_url = reverse_lazy('tasks:ev_list')
    permission_required = ('tasks.delete_actiongroup', 'tasks.view_actiongroupmember',)
    success_url = 'tasks:actgrpmem_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionGroupMemberRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(ActionGroupMemberRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.delete_actiongroupmember'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('tasks:actgrpmem_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(ActionGroupMemberRemoveView, self).dispatch(request, *args, **kwargs)


class OutputProcessor(LoginRequiredMixin):

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(OutputProcessor, self).__init__(*args, **kwargs)

    def split_delimiter(self, pstrin, pdelimiter):
        retval = str(pstrin).split(pdelimiter)
        return retval


class ActionExecScriptRedirectView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):
    """
    This class performs the "action" execution and records the output in the ActionQ table.
    """
    permission_required = ('tasks.view_actionq', 'tasks.change_actionq')
    success_url = 'tasks:act_list'
    actq = ""

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionExecScriptRedirectView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_actionq'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:act_list')
        self.actq = run_action(
            pactuser=self.request.user,
            pactusername=self.request.user.get_username(),
            pev_pk=self.kwargs.get('ev_pk'),
            pevattr_pk=self.kwargs.get('evattr_pk'),
            ptask_pk=self.kwargs.get('task_pk'),
            pact_pk=self.kwargs.get('pk'),
            pinv_pk=self.kwargs.get('inv_pk'),
            pargdyn=self.request.GET.get('argdyn'),
            pattr=self.request.GET.get('attr')
        )

        return super(ActionExecScriptRedirectView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to
        # return reverse('tasks:actq_detail', kwargs={'pk': self.actq})

        # return reverse('tasks:act_list')
        # return super().get_redirect_url(*args, **kwargs)


class ActionExecScriptGroupRedirectView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):
    """
    This class performs the "action" execution and records the output in the ActionQ table.
    """
    permission_required = ('tasks.view_actionq', 'tasks.change_actionq')
    success_url = 'tasks:act_list'
    actq = ""

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionExecScriptGroupRedirectView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_actionq'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:act_list')
        actionslistpk = str(self.kwargs.get('pk'))
        actionslist_obj = ActionGroupMember.objects.all().filter(actiongroupid=actionslistpk)
        if actionslist_obj:
            for actions in actionslist_obj:
                self.actq = run_action(
                    pactuser=self.request.user,
                    pactusername=self.request.user.get_username(),
                    pev_pk=self.kwargs.get('ev_pk'),
                    pevattr_pk=self.kwargs.get('evattr_pk'),
                    ptask_pk=self.kwargs.get('task_pk'),
                    pact_pk=actions.actionid.pk,
                    pinv_pk=self.kwargs.get('inv_pk'),
                    pargdyn=self.request.GET.get('argdyn'),
                    pattr=self.request.GET.get('attr')
                )
        return super(ActionExecScriptGroupRedirectView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to
        # return reverse('tasks:actq_detail', kwargs={'pk': self.actq})

        # return reverse('tasks:act_list')
        # return super().get_redirect_url(*args, **kwargs)


class ActionCloneRedirectView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):
    """
    This class performs the "action" execution and records the output in the ActionQ table.
    """
    permission_required = ('tasks.view_action', 'tasks.view_actionq', 'tasks.change_actionq')
    success_url = 'tasks:act_list'
    actq = ""

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ActionCloneRedirectView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_actionq'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:act_list')
        clone_action(paction_pk=self.kwargs.get('pk'))

        return super(ActionCloneRedirectView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to


class TaskListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    # model = Task
    # form_class = TaskTemplateForm
    # permission_required = ('tasks.view_task',)
    #
    # def __init__(self, *args, **kwargs):
    #     if LOGLEVEL == 1:
    #         pass
    #     elif LOGLEVEL == 2:
    #         pass
    #     elif LOGLEVEL == 3:
    #         logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
    #         logger.info(logmsg)
    #     super(TaskListView, self).__init__(*args, **kwargs)
    #
    # def get_queryset(self):
    #     retval = Task.objects.all()\
    #         .select_related('status__name')\
    #         .select_related('priority__name')\
    #         .select_related('user__username')\
    #         .select_related('playbook__pk') \
    #         .select_related('playbook__name') \
    #         .select_related('inv__pk') \
    #         .select_related('parent__pk') \
    #         .select_related('action__automationid') \
    #         .values('id', 'pk', 'title', 'description_html', 'inv__pk', 'status__name', 'priority__name',
    #                 'user__username', 'playbook__pk', 'playbook__name', 'created_at', 'modified_at', 'modified_by',
    #                 'parent', 'action__automationid', 'starttime')
    #     return retval
    #
    # def get_context_data(self, **kwargs):
    #     # create_task()
    #     kwargs['templatecategories'] = TaskTemplate.objects.filter(enabled=True).select_related('category__catid')\
    #         .select_related('category__name')\
    #         .values('pk', 'category__catid', 'category__name', 'title')
    #     return super(TaskListView, self).get_context_data(**kwargs)
    model = Task
    form_class = TaskForm
    permission_required = ('tasks.view_task',)
    paginate_by = 25

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskListView, self).__init__(*args, **kwargs)

    def get_queryset(self):
        result = super(TaskListView, self).get_queryset()
        # search related stuff
        pager_raw = self.request.GET.get("pager")
        if pager_raw == "25":
            self.paginate_by = 25
        elif pager_raw == "50":
            self.paginate_by = 50
        elif pager_raw == "100":
            self.paginate_by = 100
        order_by = self.request.GET.get("order")
        if order_by == "id":
            order_by = "id"
        elif order_by == "created":
            order_by = "created_at"
        elif order_by == "modified":
            order_by = "modified_at"
        elif order_by == "assigned":
            order_by = "user__username"
        elif order_by == "description":
            order_by = "description"
        elif order_by == "priority":
            order_by = "priority__name"
        elif order_by == "playbook":
            order_by = "playbook__name"
        elif order_by == "investigation":
            order_by = "inv__pk"
        elif order_by == "title":
            order_by = "title"
        elif order_by == "status":
            order_by = "status__name"
        elif order_by == "start":
            order_by = "starttime"
        else:
            order_by = "id"
        # queryset_list = Task.objects.all().order_by(order_by)
        queryset_list = Task.objects.all()\
            .select_related('status__name')\
            .select_related('priority__name')\
            .select_related('user__username')\
            .select_related('playbook__pk') \
            .select_related('playbook__name') \
            .select_related('inv__pk') \
            .select_related('parent__pk') \
            .select_related('action__automationid') \
            .values('id', 'pk', 'title', 'description_html', 'inv__pk', 'status__name', 'priority__name',
                    'user__username', 'playbook__pk', 'playbook__name', 'created_at', 'modified_at', 'modified_by',
                    'parent', 'action__automationid', 'starttime').order_by(order_by)

        result = queryset_list
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(pk__icontains=query) |
                Q(user__username__icontains=query) |
                Q(modified_by__icontains=query) |
                Q(description__icontains=query) |
                Q(created_by__icontains=query) |
                Q(priority__name__icontains=query) |
                Q(playbook__name__icontains=query) |
                Q(title__icontains=query) |
                Q(inv__pk__icontains=query) |
                Q(status__name__icontains=query) |
                Q(starttime__icontains=query)
            ).distinct().order_by(order_by)
            result = queryset_list
        return result

    def get_context_data(self, **kwargs):
        #     # create_task()
        kwargs['templatecategories'] = TaskTemplate.objects.filter(enabled=True).select_related('category__catid')\
            .select_related('category__name')\
            .values('pk', 'category__catid', 'category__name', 'title')
        # kwargs['actions'] = Action.objects.filter(enabled=True).order_by('title')
        # search related stuff
        kwargs['pager'] = self.paginate_by
        itemnum = Task.objects.all().count()
        divresult = divmod(itemnum, self.paginate_by)
        if divresult[1]:
            finres = divresult[0] + 1
        else:
            finres = 0
        kwargs['allcount'] = finres
        if self.request.GET.get('q'):
            kwargs['q'] = str(self.request.GET.get('q'))
        if self.request.GET.get('page'):
            kwargs['page'] = int(self.request.GET.get('page'))
        if self.request.GET.get('order'):
            kwargs['order'] = str(self.request.GET.get('order'))

        context = super(TaskListView, self).get_context_data(**kwargs)
        return context

# @method_decorator(csrf_exempt, name='dispatch')
class TaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    permission_required = ('tasks.add_task',)
    success_url = 'tasks:tsk_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(TaskCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.modified_by = self.request.user.get_username()
        self.object.created_by = self.request.user.get_username()
        self.object.save()
        return super(TaskCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_task'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('tasks:tsk_list')
        # Checks pass, let http method handlers process the request
        return super(TaskCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        inv_pk = self.kwargs.get('inv_pk')
        if inv_pk:
        #     kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=inv_pk, allownull=True)
            pass
        else:
        #     kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=None, allownull=True)
            inv_pk = 0
        kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=None, allownull=True)
        kwargs['taskstatuslist'] = TaskList.get_taskstatuslist(TaskStatus.objects.none(), anew=True)
        kwargs['inv_pk'] = inv_pk
        thetasklist = TaskList.get_tasklist(Task.objects.none(), pinv=inv_pk, pexcltask=None, pallownull=True,
                                            porder_by='pk')
        kwargs['actiontargetlist'] = thetasklist
        kwargs['parentlist'] = thetasklist
        kwargs['inputfromlist'] = thetasklist
        kwargs['actionlist'] = TaskList.get_actionlist(Action.objects.none())
        kwargs['user'] = self.request.user
        return kwargs


class TaskDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Task
    permission_required = ('tasks.view_task',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['actions'] = Action.objects.filter(enabled=True).order_by('title')
        return super(TaskDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.view_task'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('tasks:tsk_list')
        # Checks pass, let http method handlers process the request
        return super(TaskDetailView, self).dispatch(request, *args, **kwargs)


# @method_decorator(csrf_exempt, name='dispatch')
class TaskUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    redirect_field_name = 'tasks/task_detail.html'
    form_class = TaskForm
    model = Task
    permission_required = ('tasks.change_task',)
    success_url = 'tasks:tsk_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(TaskUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_task'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:tsk_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(TaskUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        self.object.save()
        return super(TaskUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(TaskUpdateView, self).get_form_kwargs()
        task_pk = self.object.pk
        inv_pk = self.object.inv.pk
        if inv_pk:
        #     kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=inv_pk, allownull=True)
            pass
        else:
        #     kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=None, allownull=True)
            inv_pk = 0
        kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=None, allownull=True)
        kwargs['inv_pk'] = inv_pk
        kwargs['actionlist'] = TaskList.get_actionlist(Action.objects.none())
        kwargs['taskstatuslist'] = TaskList.get_taskstatuslist(TaskStatus.objects.none())
        thetasklist = TaskList.get_tasklist(Task.objects.none(), pinv=inv_pk, pexcltask=task_pk, pallownull=True,
                                            porder_by='pk')
        kwargs['actiontargetlist'] = thetasklist
        kwargs['parentlist'] = thetasklist
        kwargs['inputfromlist'] = thetasklist
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class TaskRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Task
    # success_url = reverse_lazy('tasks:tsk_list')
    permission_required = ('tasks.delete_task',)
    success_url = 'tasks:tsk_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(TaskRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.delete_task'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('tasks:tsk_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(TaskRemoveView, self).dispatch(request, *args, **kwargs)


#  #################### TASK TEMPLATE VIEWS###############################
class TaskTemplateListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = TaskTemplate
    form_class = TaskTemplateForm
    permission_required = ('tasks.view_tasktemplate',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskTemplateListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # create_task()
        return super(TaskTemplateListView, self).get_context_data(**kwargs)


class TaskTemplateCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = TaskTemplate
    form_class = TaskTemplateForm
    permission_required = ('tasks.add_tasktemplate',)
    success_url = 'tasks:tmp_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskTemplateCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(TaskTemplateCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.modified_by = self.request.user.get_username()
        self.object.created_by = self.request.user.get_username()
        self.object.save()
        return super(TaskTemplateCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_tasktemplate'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('tasks:tmp_list')
        # Checks pass, let http method handlers process the request
        return super(TaskTemplateCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(TaskTemplateCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class TaskTemplateDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = TaskTemplate
    permission_required = ('tasks.view_tasktemplate',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskTemplateDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(TaskTemplateDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.view_tasktemplate'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('tasks:tmp_list')
        # Checks pass, let http method handlers process the request
        return super(TaskTemplateDetailView, self).dispatch(request, *args, **kwargs)


class TaskTemplateUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    redirect_field_name = 'tasks/tasktemplate_detail.html'
    form_class = TaskTemplateForm
    model = TaskTemplate
    permission_required = ('tasks.change_tasktemplate',)
    success_url = 'tasks:tmp_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskTemplateUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(TaskTemplateUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_tasktemplate'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:tmp_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(TaskTemplateUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        self.object.save()
        return super(TaskTemplateUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(TaskTemplateUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class TaskTemplateRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = TaskTemplate
    # success_url = reverse_lazy('tasks:tsk_list')
    permission_required = ('tasks.delete_tasktemplate',)
    success_url = 'tasks:tmp_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskTemplateRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(TaskTemplateRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.delete_tasktemplate'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('tasks:tmp_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(TaskTemplateRemoveView, self).dispatch(request, *args, **kwargs)


# def add_task_from_template(atitle, astatus, aplaybook, auser, ainv,
#                            acategory, apriority, atype, asummary, adescription,
#                            amodified_by, acreated_by):
#     obj = Task.objects.create(
#         title=atitle,
#         status=astatus,
#         playbook=aplaybook,
#         user=auser,
#         inv=ainv,
#         category=acategory,
#         priority=apriority,
#         type=atype,
#         summary=asummary,
#         description=adescription,
#         modified_by=amodified_by,
#         created_by=acreated_by,
#     )
#     return obj

class TaskTemplateAddView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):
    """
    This function generates a task based on a specified template task.
    It also pulls in associated defined variables and creates under the new task
    """

    # model = TaskTemplate
    permission_required = ('tasks.view_task', 'tasks.add_task', 'tasks.view_tasktemplate')
    # url = reverse_lazy('tasks:ev_list')
    success_url = 'tasks:tsk_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskTemplateAddView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_task'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('tasks:tsk_list')
        # playbook_pk = self.kwargs.get('play_pk')
        play_pk = self.kwargs.get('play_pk')
        tmp_pk = self.kwargs.get('pk')
        # Checks pass, let http method handlers process the request
        tmp_obj = TaskTemplate.objects.get(pk=tmp_pk)
        if tmp_obj.user:
            tmp_user = User.objects.get(pk=tmp_obj.user.pk)
        else:
            tmp_user = None
        inv_obj = self.kwargs.get('inv_pk')
        # if inv_obj != None and inv_obj!='0':
        if inv_obj is not None and inv_obj != '0':
            tmp_inv = Inv.objects.get(pk=self.kwargs.get('inv_pk'))
        else:
            tmp_inv = None
        if tmp_obj.action:
            # tmp_action = TaskTemplate.objects.get(pk=tmp_obj.action.pk) # BL
            tmp_action = Action.objects.get(pk=tmp_obj.action.pk)
        else:
            tmp_action = None
        if tmp_obj.status:
            new_status = TaskStatus.objects.get(pk=tmp_obj.status.pk)
        else:
            new_status = None
        if play_pk != "0" and play_pk is not None:
            new_play = Playbook.objects.get(pk=play_pk)
        else:
            new_play = None
        if tmp_obj.category:
            new_category = TaskCategory.objects.get(pk=tmp_obj.category.pk)
        else:
            new_category = None
        if tmp_obj.priority:
            new_priority = TaskPriority.objects.get(pk=tmp_obj.priority.pk)
        else:
            new_priority = None
        if tmp_obj.type:
            new_type = TaskType.objects.get(pk=tmp_obj.type.pk)
        else:
            new_type = None
        if tmp_obj.requiresevidence:
            new_requiresevidence = True
        else:
            new_requiresevidence = False
        task_instance = add_task_from_template(
            atitle=str(tmp_obj.title),
            astatus=new_status,
            aplaybook=new_play,
            auser=tmp_user,
            ainv=tmp_inv,
            # aaction=tmp_action,
            aaction=tmp_action,
            aactiontarget=None,
            acategory=new_category,
            apriority=new_priority,
            atype=new_type,
            asummary=str(tmp_obj.summary),
            adescription=str(tmp_obj.description),
            arequiresevidence=new_requiresevidence,
            amodified_by=str(self.request.user),
            acreated_by=str(self.request.user),
            )

        # This section below generates the variables for the new task
        myvars = TaskVar.objects.filter(tasktemplate=tmp_pk)
        for myvar in myvars:
            TaskVar.objects.create(
                category=myvar.category,
                type=myvar.type,
                task=task_instance,
                tasktemplate=None,
                name=myvar.name,
                value=myvar.value,
                required=myvar.required,
                enabled=myvar.enabled
            )

        # task_instance = Task.objects.create(title="autotest", description="x", priority=TaskPriority.objects.
        # get(pk=1))
        # return redirect(self.success_url)
        return super(TaskTemplateAddView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to
        # return reverse('tasks:tsk_list')
        # return super().get_redirect_url(*args, **kwargs)


#   Task Var views
class TaskVarListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = TaskVar
    form_class = TaskVarForm
    permission_required = ('tasks.view_taskvar',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskVarListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # create_task()
        return super(TaskVarListView, self).get_context_data(**kwargs)


class TaskVarCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = TaskVar
    form_class = TaskVarForm
    permission_required = ('tasks.add_taskvar',)
    success_url = 'tasks:tvar_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskVarCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(TaskVarCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # self.object.user = self.request.user
        self.object.modified_by = self.request.user.get_username()
        self.object.created_by = self.request.user.get_username()
        self.object.save()
        return super(TaskVarCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_taskvar'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('tasks:tvar_list')
        # Checks pass, let http method handlers process the request
        return super(TaskVarCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(TaskVarCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        task_pk = self.kwargs.get('task_pk')
        tasktmp_pk = self.kwargs.get('tasktmp_pk')

        if task_pk:
            pass
        else:
            task_pk = 0
        if tasktmp_pk:
            pass
        else:
            tasktmp_pk = 0

        kwargs['task_pk'] = task_pk
        kwargs['tasktmp_pk'] = tasktmp_pk
        kwargs['user'] = self.request.user
        return kwargs


class TaskVarDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = TaskVar
    permission_required = ('tasks.view_taskvar',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskVarDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(TaskVarDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.view_taskvar'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('tasks:tvar_list')
        # Checks pass, let http method handlers process the request
        return super(TaskVarDetailView, self).dispatch(request, *args, **kwargs)


class TaskVarUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    redirect_field_name = 'tasks/taskvar_detail.html'
    form_class = TaskVarForm
    model = TaskVar
    permission_required = ('tasks.change_taskvar',)
    success_url = 'tasks:tvar_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskVarUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(TaskVarUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_taskvar'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:tvar_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(TaskVarUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # self.object.modified_by = self.request.user.get_username()
        self.object.save()
        return super(TaskVarUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(TaskVarUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class TaskVarRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = TaskVar
    permission_required = ('tasks.delete_taskvar',)
    success_url = 'tasks:tvar_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskVarRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(TaskVarRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.delete_taskvar'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('tasks:tvar_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(TaskVarRemoveView, self).dispatch(request, *args, **kwargs)


class PlaybookListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Playbook
    form_class = PlaybookForm
    permission_required = ('tasks.view_playbook',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['playbooktmp'] = PlaybookTemplate.objects.filter(enabled=True)
        return super(PlaybookListView, self).get_context_data(**kwargs)


class PlaybookCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):
    permission_required = ('tasks.add_playbook',)
    success_url = 'tasks:play_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookCreateView, self).__init__(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_playbook'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('tasks:play_list')

        inv_pk = self.kwargs.get('inv_pk')
        tmp_pk = self.kwargs.get('tmp_pk')
        tmp_obj = PlaybookTemplate.objects.get(pk=tmp_pk)
        if tmp_obj.user:
            tmp_user = User.objects.get(pk=tmp_obj.user.pk)
        else:
            tmp_user = None
        inv_obj = self.kwargs.get('inv_pk')
        # if inv_obj != None and inv_obj != '0':
        if inv_obj is not None and inv_obj != '0':
            tmp_inv = Inv.objects.get(pk=inv_pk)
        else:
            tmp_inv = None
        new_playbook(
            pplaybooktemplate=tmp_obj,
            pname=tmp_obj.name,
            pversion=tmp_obj.version,
            puser=tmp_user,
            pinv=tmp_inv,
            pdescription=tmp_obj.description,
            pmodified_by=str(self.request.user),
            pcreated_by=str(self.request.user)
        )
        # Checks pass, let http method handlers process the request
        return super(PlaybookCreateView, self).dispatch(request, *args, **kwargs)

    # def get_form_kwargs(self):
    #     kwargs = super(PlaybookCreateView, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs


class PlaybookDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Playbook
    permission_required = ('tasks.view_playbook',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(PlaybookDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.view_playbook'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('tasks:play_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(PlaybookDetailView, self).dispatch(request, *args, **kwargs)


class PlaybookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    form_class = PlaybookForm
    model = Playbook
    permission_required = ('tasks.change_playbook',)
    success_url = 'tasks:play_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(PlaybookUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_playbook'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:play_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(PlaybookUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        self.object.save()
        return super(PlaybookUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(PlaybookUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class PlaybookRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Playbook
    permission_required = ('tasks.delete_playbook', 'tasks.view_playbook',)
    success_url = 'tasks:play_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(PlaybookRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.delete_playbook'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('tasks:playtmp_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(PlaybookRemoveView, self).dispatch(request, *args, **kwargs)


class PlaybookTemplateListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = PlaybookTemplate
    form_class = PlaybookTemplateForm
    permission_required = ('tasks.view_playbooktemplate',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookTemplateListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(PlaybookTemplateListView, self).get_context_data(**kwargs)


class PlaybookTemplateCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = PlaybookTemplate
    form_class = PlaybookTemplateForm
    permission_required = ('tasks.add_playbooktemplate',)
    # inv_pk = None
    # task_pk = None
    success_url = 'tasks:playtmp_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookTemplateCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(PlaybookTemplateCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.modified_by = self.request.user.get_username()
        self.object.created_by = self.request.user.get_username()
        self.object.save()
        return super(PlaybookTemplateCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_playbooktemplate'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('tasks:playtmp_list')
        # Checks pass, let http method handlers process the request
        return super(PlaybookTemplateCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(PlaybookTemplateCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        # kwargs['inv_pk'] = self.kwargs.get('inv_pk')
        kwargs['user'] = self.request.user
        return kwargs


class PlaybookTemplateDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = PlaybookTemplate
    permission_required = ('tasks.view_playbooktemplate',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookTemplateDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(PlaybookTemplateDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.view_playbooktemplate'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('tasks:playtmp_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(PlaybookTemplateDetailView, self).dispatch(request, *args, **kwargs)


class PlaybookTemplateUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    # redirect_field_name = 'playbooks/playbooktemplate_detail.html'
    form_class = PlaybookTemplateForm
    model = PlaybookTemplate
    permission_required = ('tasks.change_playbooktemplate',)
    success_url = 'tasks:playtmp_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookTemplateUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(PlaybookTemplateUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_playbooktemplate'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:playtmp_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(PlaybookTemplateUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        self.object.save()
        return super(PlaybookTemplateUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(PlaybookTemplateUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class PlaybookTemplateRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = PlaybookTemplate
#    success_url = reverse_lazy('tasks:play_list')
    permission_required = ('tasks.delete_playbooktemplate', 'tasks.view_playbooktemplate',)
    success_url = 'tasks:playtmp_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookTemplateRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(PlaybookTemplateRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.delete_playbooktemplate'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('tasks:playtmp_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(PlaybookTemplateRemoveView, self).dispatch(request, *args, **kwargs)


# ################# Playbook Items
class PlaybookTemplateItemListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = PlaybookTemplateItem
    form_class = PlaybookTemplateItemForm
    permission_required = ('tasks.view_playbooktemplateitem',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookTemplateItemListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # create_task()
        # kwargs['templatecategories'] = TaskVar.objects.all()
        return super(PlaybookTemplateItemListView, self).get_context_data(**kwargs)


class PlaybookTemplateItemCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = PlaybookTemplateItem
    form_class = PlaybookTemplateItemForm
    permission_required = ('tasks.add_playbooktemplateitem',)
    success_url = 'tasks:playittmp_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookTemplateItemCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(PlaybookTemplateItemCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # self.object.user = self.request.user
        self.object.modified_by = self.request.user.get_username()
        self.object.created_by = self.request.user.get_username()
        self.object.save()
        return super(PlaybookTemplateItemCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_playbooktemplateitem'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('tasks:playittmp_list')
        # Checks pass, let http method handlers process the request
        return super(PlaybookTemplateItemCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(PlaybookTemplateItemCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        play_pk = self.kwargs.get('play_pk')

        if play_pk:
            pass
        else:
            play_pk = 0
        kwargs['play_pk'] = play_pk
        kwargs['user'] = self.request.user
        return kwargs


class PlaybookTemplateItemDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = PlaybookTemplateItem
    permission_required = ('tasks.view_playbooktemplateitem',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookTemplateItemDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(PlaybookTemplateItemDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.view_playbooktemplateitem'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('tasks:playittmp_list')
        # Checks pass, let http method handlers process the request
        return super(PlaybookTemplateItemDetailView, self).dispatch(request, *args, **kwargs)


class PlaybookTemplateItemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    redirect_field_name = 'playbooks/playbooktemplateitem_detail.html'
    form_class = PlaybookTemplateItemForm
    model = PlaybookTemplateItem
    permission_required = ('tasks.change_playbooktemplateitem',)
    success_url = 'tasks:playittmp_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookTemplateItemUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(PlaybookTemplateItemUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_playbooktemplateitem'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:playittmp_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(PlaybookTemplateItemUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # self.object.modified_by = self.request.user.get_username()
        self.object.save()
        return super(PlaybookTemplateItemUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(PlaybookTemplateItemUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        play_pk = self.kwargs.get('pk')

        if play_pk:
            pass
        else:
            play_pk = 0
        kwargs['play_pk'] = play_pk
        kwargs['user'] = self.request.user
        return kwargs


class PlaybookTemplateItemRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = PlaybookTemplateItem
    # success_url = reverse_lazy('tasks:tsk_list')
    permission_required = ('tasks.delete_playbooktemplateitem',)
    success_url = 'tasks:playittmp_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(PlaybookTemplateItemRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(PlaybookTemplateItemRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        curr_pk = self.kwargs.get('pk')
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.delete_playbooktemplateitem'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('tasks:playittmp_detail', pk=curr_pk)
        elif curr_pk:
            outmsgitems = playbooktemplateitem_check_delete_condition(curr_pk)
            if len(outmsgitems) != 0:
                outmsg = "The Task is referenced from other tasks as inputs, Task(s): %s" % outmsgitems
                messages.error(self.request, outmsg)
                return redirect('tasks:playittmp_detail', pk=curr_pk)

        # Checks pass, let http method handlers process the request
        return super(PlaybookTemplateItemRemoveView, self).dispatch(request, *args, **kwargs)


# #### Assign task to the user
class TaskAssignView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):

    # model = TaskTemplate
    permission_required = ('tasks.view_task', 'tasks.change_task')
    # url = reverse_lazy('tasks:ev_list')
    success_url = 'tasks:tsk_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskAssignView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_task'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:tsk_list')
        task_pk = self.kwargs.get('pk')
        # Checks pass, let http method handlers process the request
        # Task.objects.filter(pk=task_pk).update(user=self.request.user)
        # Task.objects.filter(pk=task_pk).update(status=3)
        task_obj = Task.objects.get(pk=task_pk)
        task_obj.user = self.request.user
        task_obj.status = TaskStatus.objects.get(pk=3)
        task_obj.save()

        # return redirect(self.success_url)
        return super(TaskAssignView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to
        # return reverse('tasks:tsk_list')
        # return super().get_redirect_url(*args, **kwargs)


# ### CLOSE TASK
class TaskCloseView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):

    # model = TaskTemplate
    permission_required = ('tasks.view_task', 'tasks.change_task')
    # url = reverse_lazy('tasks:ev_list')
    success_url = 'tasks:tsk_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskCloseView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_task'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:tsk_list')
        task_pk = self.kwargs.get('pk')
        # Checks pass, let http method handlers process the request
        # Task.objects.filter(pk=task_pk).update(status=2)
        task_obj = Task.objects.get(pk=task_pk)
        task_obj.status = TaskStatus.objects.get(pk=2)
        task_obj.save()
        # return redirect(self.success_url)
        return super(TaskCloseView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to
        # return reverse('tasks:tsk_list')
        # return super().get_redirect_url(*args, **kwargs)


class TaskOpenView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):

    # model = TaskTemplate
    permission_required = ('tasks.view_task', 'tasks.change_task')
    # url = reverse_lazy('tasks:ev_list')
    success_url = 'tasks:tsk_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskOpenView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_task'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:tsk_list')
        task_pk = self.kwargs.get('pk')
        # Checks pass, let http method handlers process the request
        # Task.objects.filter(pk=task_pk).update(status=1)
        task_obj = Task.objects.get(pk=task_pk)
        task_obj.status = TaskStatus.objects.get(pk=1)
        task_obj.save()

        # return redirect(self.success_url)
        return super(TaskOpenView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to
        # return reverse('tasks:tsk_list')
        # return super().get_redirect_url(*args, **kwargs)


class TaskWaitingView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):

    # model = TaskTemplate
    permission_required = ('tasks.view_task', 'tasks.change_task')
    # url = reverse_lazy('tasks:ev_list')
    success_url = 'tasks:tsk_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskWaitingView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_task'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:tsk_list')
        task_pk = self.kwargs.get('pk')
        # Checks pass, let http method handlers process the request
        # Task.objects.filter(pk=task_pk).update(status=1)
        task_obj = Task.objects.get(pk=task_pk)
        task_obj.status = TaskStatus.objects.get(pk=5)
        task_obj.save()

        # return redirect(self.success_url)
        return super(TaskWaitingView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to
        # return reverse('tasks:tsk_list')
        # return super().get_redirect_url(*args, **kwargs)


class TaskSkipView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):

    # model = TaskTemplate
    permission_required = ('tasks.view_task', 'tasks.change_task')
    # url = reverse_lazy('tasks:ev_list')
    success_url = 'tasks:tsk_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(TaskSkipView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_task'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:tsk_list')
        task_pk = self.kwargs.get('pk')
        # Checks pass, let http method handlers process the request
        # Task.objects.filter(pk=task_pk).update(status=1)
        task_obj = Task.objects.get(pk=task_pk)
        task_obj.status = TaskStatus.objects.get(pk=4)
        task_obj.save()

        # return redirect(self.success_url)
        return super(TaskSkipView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to


# Create your views here.
# #############################################################################3
# Investigation related views
class EvidenceListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Evidence
    form_class = EvidenceForm
    permission_required = ('tasks.view_evidence',)
    paginate_by = 25

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(EvidenceListView, self).__init__(*args, **kwargs)

    def get_queryset(self):
        result = super(EvidenceListView, self).get_queryset()
        # search related stuff
        pager_raw = self.request.GET.get("pager")
        if pager_raw == "25":
            self.paginate_by = 25
        elif pager_raw == "50":
            self.paginate_by = 50
        elif pager_raw == "100":
            self.paginate_by = 100
        order_by = self.request.GET.get("order")
        if order_by == "id":
            order_by = "id"
        elif order_by == "created":
            order_by = "created_at"
        elif order_by == "modified":
            order_by = "modified_at"
        elif order_by == "filename":
            order_by = "fileName"
        elif order_by == "assigned":
            order_by = "user__username"
        elif order_by == "investigation":
            order_by = "investigation"
        elif order_by == "task":
            order_by = "task"
        else:
            order_by = "id"
        queryset_list = Evidence.objects.all().order_by(order_by)
        result = queryset_list
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(pk__icontains=query) |
                    Q(fileName__icontains=query) |
                    Q(modified_by__icontains=query) |
                    Q(description__icontains=query) |
                    Q(created_by__icontains=query) |
                    Q(user__username__icontains=query)
                    ).distinct().order_by(order_by)
            result = queryset_list
        return result

    def get_context_data(self, **kwargs):
        kwargs['actions'] = Action.objects.filter(enabled=True).order_by('title')
        # search related stuff
        kwargs['pager'] = self.paginate_by
        itemnum = Evidence.objects.all().count()
        divresult = divmod(itemnum, self.paginate_by)
        if divresult[1]:
            finres = divresult[0] + 1
        else:
            finres = 0
        kwargs['allcount'] = finres
        if self.request.GET.get('q'):
            kwargs['q'] = str(self.request.GET.get('q'))
        if self.request.GET.get('page'):
            kwargs['page'] = int(self.request.GET.get('page'))
        if self.request.GET.get('order'):
            kwargs['order'] = str(self.request.GET.get('order'))

        context = super(EvidenceListView, self).get_context_data(**kwargs)
        return context


# @method_decorator(csrf_exempt, name='dispatch')
class EvidenceCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    # fields = ("inv", "user", "description", "fileRef")
    model = Evidence
    form_class = EvidenceForm
    permission_required = ('tasks.add_evidence',)
    # inv_pk = None
    # task_pk = None
    success_url = 'tasks:ev_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(EvidenceCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            if '/invs/detail/' in self.request.GET['next1']:
                redirect_to = self.request.GET['next1'] + "#thebottom"
            else:
                redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(EvidenceCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.modified_by = self.request.user.get_username()
        self.object.created_by = self.request.user.get_username()
        if self.request.FILES:
            self.object.fileName = self.request.FILES['fileRef'].name
        self.object.save()
        # if self.inv_pk and self.inv_pk!=0:
        #     return redirect('invs:inv_detail',pk=self.inv_pk)
        # elif self.task_pk and self.task_pk!=0:
        #     return redirect('tasks:tsk_detail', pk=self.task_pk)
        # return redirect(self.next1redir)
        return super(EvidenceCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_evidence'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('tasks:ev_list')
        # Checks pass, let http method handlers process the request
        return super(EvidenceCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(EvidenceCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        inv_pk = self.kwargs.get('inv_pk')
        task_pk = self.kwargs.get('task_pk')
        if inv_pk:
        #     kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=inv_pk, allownull=True)
            pass
        else:
        #     kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=None, allownull=True)
            inv_pk = 0
        kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=None, allownull=True)
        if task_pk:
            pass
        else:
            task_pk = 0
        kwargs['tasklist'] = TaskList.get_tasklist(Task.objects.none(), pinv=inv_pk, pexcltask=None, pallownull=True,
                                                   porder_by='pk', preadonly=True)
        kwargs['inv_pk'] = inv_pk
        kwargs['task_pk'] = task_pk
        kwargs['user'] = self.request.user
        return kwargs


class EvidenceDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Evidence
    permission_required = ('tasks.view_evidence',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(EvidenceDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['actions'] = Action.objects.filter(enabled=True).order_by('title')
        return super(EvidenceDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.view_evidence'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('tasks:ev_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(EvidenceDetailView, self).dispatch(request, *args, **kwargs)


# @method_decorator(csrf_exempt, name='dispatch')
class EvidenceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    # redirect_field_name = 'tasks/evidence_detail.html'
    form_class = EvidenceForm
    model = Evidence
    permission_required = ('tasks.change_evidence',)
    success_url = 'tasks:ev_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(EvidenceUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(EvidenceUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        ev_pk = Evidence.objects.get(pk=self.kwargs.get('pk'))
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_evidence'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:ev_detail', pk=self.kwargs.get('pk'))
        elif ev_pk.task and ev_pk.task.status.name == "Completed":
            messages.error(self.request, "Task is Completed!!!")
            return redirect('tasks:ev_detail', pk=self.kwargs.get('pk'))
        elif ev_pk.task and ev_pk.task.status.name == "Skipped":
            messages.error(self.request, "Task is Skipped!!!")
            return redirect('tasks:ev_detail', pk=self.kwargs.get('pk'))
        elif ev_pk.inv and ev_pk.inv.status.name == "Closed":
            messages.error(self.request, "Investigation is Closed!!!")
            return redirect('tasks:ev_detail', pk=self.kwargs.get('pk'))
        elif ev_pk.inv and ev_pk.inv.status.name == "Archived":
            messages.error(self.request, "Investigation is Archived!!!")
            return redirect('tasks:ev_detail', pk=self.kwargs.get('pk'))

        # Checks pass, let http method handlers process the request
        return super(EvidenceUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()

        if self.request.FILES:
            self.object.fileName = self.request.FILES['fileRef'].name

        self.object.save()
        return super(EvidenceUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(EvidenceUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        inv_pk = self.kwargs.get('inv_pk')
        task_pk = self.kwargs.get('task_pk')
        # if inv_pk:
        #     pass
        # else:
        #     inv_pk = 0
        # if task_pk:
        #     pass
        # else:
        #     task_pk = 0
        #
        # kwargs['inv_pk'] = inv_pk
        # kwargs['task_pk'] = task_pk
        if inv_pk:
            kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=inv_pk, allownull=True)
            pass
        else:
            kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=None, allownull=True)
            inv_pk = 0
        if task_pk:
            pass
        else:
            task_pk = 0
        kwargs['tasklist'] = TaskList.get_tasklist(Task.objects.none(), pinv=inv_pk, pexcltask=None, pallownull=True,
                                                   porder_by='pk')
        kwargs['inv_pk'] = inv_pk
        kwargs['task_pk'] = task_pk
        # print("XXX: %s %s"%(inv_pk, task_pk))
        return kwargs


class EvidenceRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Evidence
#    success_url = reverse_lazy('tasks:ev_list')
    permission_required = ('tasks.delete_evidence', 'tasks.view_evidence',)
    success_url = 'tasks:ev_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(EvidenceRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(EvidenceRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        ev_pk = Evidence.objects.get(pk=self.kwargs.get('pk'))
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.delete_evidence'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('tasks:ev_detail', pk=self.kwargs.get('pk'))
        elif ev_pk.task and ev_pk.task.status.name == "Completed":
            messages.error(self.request, "Task is Completed!!!")
            return redirect('tasks:ev_detail', pk=self.kwargs.get('pk'))
        elif ev_pk.task and ev_pk.task.status.name == "Skipped":
            messages.error(self.request, "Task is Skipped!!!")
            return redirect('tasks:ev_detail', pk=self.kwargs.get('pk'))
        elif ev_pk.inv and ev_pk.inv.status.name == "Closed":
            messages.error(self.request, "Investigation is Closed!!!")
            return redirect('tasks:ev_detail', pk=self.kwargs.get('pk'))
        elif ev_pk.inv and ev_pk.inv.status.name == "Archived":
            messages.error(self.request, "Investigation is Archived!!!")
            return redirect('tasks:ev_detail', pk=self.kwargs.get('pk'))

        # Checks pass, let http method handlers process the request
        return super(EvidenceRemoveView, self).dispatch(request, *args, **kwargs)


class EvidenceAssignTaskView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):

    # model = TaskTemplate
    permission_required = ('tasks.view_task', 'tasks.change_task', 'tasks.view_evidence', 'tasks.change_evidence')
    # url = reverse_lazy('tasks:ev_list')
    success_url = 'tasks:tsk_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(EvidenceAssignTaskView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_task') or \
                not self.request.user.has_perm('tasks.change_evidence'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:tsk_list')
        ev_pk = self.kwargs.get('pk')
        task_pk = self.kwargs.get('task_pk')
        if task_pk == 0 or task_pk == "0":
            task_pk = None
        # Checks pass, let http method handlers process the request
        # Task.objects.filter(pk=task_pk).update(user=self.request.user)
        # Task.objects.filter(pk=task_pk).update(status=3)
        ev_obj = Evidence.objects.get(pk=ev_pk)
        if task_pk:
            task_obj = Task.objects.get(pk=task_pk)
        else:
            task_obj = None
        ev_obj.task = task_obj
        ev_obj.save()

        # return redirect(self.success_url)
        return super(EvidenceAssignTaskView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to
        # return reverse('tasks:tsk_list')
        # return super().get_redirect_url(*args, **kwargs)



# ############ Attributes
class EvidenceAttrListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    # model = EvidenceAttr
    # form_class = EvidenceAttrForm
    # permission_required = ('tasks.view_evidenceattr',)
    #
    # def __init__(self, *args, **kwargs):
    #     if LOGLEVEL == 1:
    #         pass
    #     elif LOGLEVEL == 2:
    #         pass
    #     elif LOGLEVEL == 3:
    #         logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
    #         logger.info(logmsg)
    #     super(EvidenceAttrListView, self).__init__(*args, **kwargs)
    #
    # def get_context_data(self, **kwargs):
    #     kwargs['actions'] = Action.objects.filter(enabled=True).order_by('title')
    #     return super(EvidenceAttrListView, self).get_context_data(**kwargs)
    model = EvidenceAttr
    form_class = EvidenceAttrForm
    permission_required = ('tasks.view_evidenceattr',)
    paginate_by = 25

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(EvidenceAttrListView, self).__init__(*args, **kwargs)

    def get_queryset(self):
        result = super(EvidenceAttrListView, self).get_queryset()
        # search related stuff
        pager_raw = self.request.GET.get("pager")
        if pager_raw == "25":
            self.paginate_by = 25
        elif pager_raw == "50":
            self.paginate_by = 50
        elif pager_raw == "100":
            self.paginate_by = 100
        order_by = self.request.GET.get("order")
        if order_by == "id":
            order_by = "id"
        elif order_by == "created":
            order_by = "created_at"
        elif order_by == "modified":
            order_by = "modified_at"
        elif order_by == "value":
            order_by = "evattrvalue"
        elif order_by == "format":
            order_by = "evattrformat__name"
        elif order_by == "observable":
            order_by = "observable"
        elif order_by == "reputation":
            order_by = "attr_reputation__name"
        elif order_by == "user":
            order_by = "user__username"
        elif order_by == "evidence":
            order_by = "ev__pk"
        else:
            order_by = "id"
        queryset_list = EvidenceAttr.objects.all().order_by(order_by)
        result = queryset_list
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(pk__icontains=query) |
                Q(ev__pk__icontains=query) |
                Q(evattrvalue__icontains=query) |
                Q(modified_by__icontains=query) |
                Q(evattrformat__name__icontains=query) |
                Q(attr_reputation__name__icontains=query) |
                Q(created_by__icontains=query)
                ).distinct().order_by(order_by)
            result = queryset_list
        return result

    def get_context_data(self, **kwargs):
        #     kwargs['actions'] = Action.objects.filter(enabled=True).order_by('title')
        # search related stuff
        kwargs['pager'] = self.paginate_by
        itemnum = EvidenceAttr.objects.all().count()
        divresult = divmod(itemnum, self.paginate_by)
        if divresult[1]:
            finres = divresult[0] + 1
        else:
            finres = 0
        kwargs['allcount'] = finres
        if self.request.GET.get('q'):
            kwargs['q'] = str(self.request.GET.get('q'))
        if self.request.GET.get('page'):
            kwargs['page'] = int(self.request.GET.get('page'))
        if self.request.GET.get('order'):
            kwargs['order'] = str(self.request.GET.get('order'))

        context = super(EvidenceAttrListView, self).get_context_data(**kwargs)
        return context

class EvidenceAttrCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    # fields = ("inv", "user", "description", "fileRef")
    model = EvidenceAttr
    form_class = EvidenceAttrForm
    permission_required = ('tasks.add_evidenceattr',)
    # inv_pk = None
    # task_pk = None
    success_url = 'tasks:evattr_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(EvidenceAttrCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(EvidenceAttrCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.modified_by = self.request.user.get_username()
        self.object.created_by = self.request.user.get_username()
        self.object.save()
        # if self.inv_pk and self.inv_pk!=0:
        #     return redirect('invs:inv_detail',pk=self.inv_pk)
        # elif self.task_pk and self.task_pk!=0:
        #     return redirect('tasks:tsk_detail', pk=self.task_pk)
        # return redirect(self.next1redir)
        return super(EvidenceAttrCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_evidenceattr'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('tasks:evattr_list')
        # Checks pass, let http method handlers process the request
        return super(EvidenceAttrCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(EvidenceAttrCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs.get('pk')
        return kwargs


class EvidenceAttrDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = EvidenceAttr
    permission_required = ('tasks.view_evidenceattr',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(EvidenceAttrDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['actions'] = Action.objects.filter(enabled=True).order_by('title')
        return super(EvidenceAttrDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.view_evidenceattr'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('tasks:evattr_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(EvidenceAttrDetailView, self).dispatch(request, *args, **kwargs)


class EvidenceAttrUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    # redirect_field_name = 'tasks/evidence_detail.html'
    form_class = EvidenceAttrForm
    model = EvidenceAttr
    permission_required = ('tasks.change_evidenceattr',)
    success_url = 'tasks:evattr_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(EvidenceAttrUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(EvidenceAttrUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_evidenceattr'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:evattr_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(EvidenceAttrUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        self.object.save()
        return super(EvidenceAttrUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(EvidenceAttrUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        # inv_pk = self.kwargs.get('inv_pk')
        # task_pk = self.kwargs.get('task_pk')
        # if inv_pk:
        #     pass
        # else:
        #     inv_pk = 0
        # if task_pk:
        #     pass
        # else:
        #     task_pk = 0
        #
        # kwargs['inv_pk'] = inv_pk
        # kwargs['task_pk'] = task_pk
        return kwargs


class EvidenceAttrRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = EvidenceAttr
#    success_url = reverse_lazy('tasks:ev_list')
    permission_required = ('tasks.delete_evidenceattr', 'tasks.view_evidenceattr',)
    success_url = 'tasks:evattr_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(EvidenceAttrRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
                # return reverse("tasks:ev_detail", kwargs={'pk': self.object.ev.pk})
        else:
            return reverse(self.success_url)
            # return reverse("tasks:ev_detail", kwargs={'pk': self.object.ev.pk})
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(EvidenceAttrRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.delete_evidenceattr'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('tasks:evattr_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(EvidenceAttrRemoveView, self).dispatch(request, *args, **kwargs)


class EvidenceAttrObservableToggleView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):
    permission_required = ('tasks.view_evidenceattr', 'tasks.change_evidenceattr')
    success_url = 'tasks:evattr_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(EvidenceAttrObservableToggleView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_evidenceattr'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:evattr_list')
        evattr_pk = self.kwargs.get('pk')
        evidenceattrobservabletoggle(evattr_pk)
        # evattr_obj = EvidenceAttr.objects.get(pk=evattr_pk)
        # evattr_obj.observable = True
        # evattr_obj.save()

        # return redirect(self.success_url)
        return super(EvidenceAttrObservableToggleView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to
        # return reverse('tasks:tsk_list')
        # return super().get_redirect_url(*args, **kwargs)


class EvidenceAttrMaliciousToggleView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):
    permission_required = ('tasks.view_evidenceattr', 'tasks.change_evidenceattr')
    success_url = 'tasks:evattr_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(EvidenceAttrMaliciousToggleView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_evidenceattr'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:evattr_list')
        evattr_pk = self.kwargs.get('pk')
        evidenceattrmalicioustoggle(evattr_pk)
        return super(EvidenceAttrMaliciousToggleView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to
        # return reverse('tasks:tsk_list')
        # return super().get_redirect_url(*args, **kwargs)

# #######################################################
class AddToProfileRedirectView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):
    """
    This class performs the "add tp profile" action on an attribute depending on it's type.
    """
    permission_required = ('tasks.view_evidence', 'tasks.change_evidence', 'tasks.view_evidenceattr',
                           'tasks.change_evidenceattr')
    success_url = 'tasks:ev_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(AddToProfileRedirectView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_profile'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:ev_list')

        # self.actq = run_action(
        #     pactuser=self.request.user,
        #     pactusername=self.request.user.get_username(),
        #     pev_pk=self.kwargs.get('ev_pk'),
        #     pevattr_pk=self.kwargs.get('evattr_pk'),
        #     ptask_pk=self.kwargs.get('task_pk'),
        #     pact_pk=self.kwargs.get('pk'),
        #     pinv_pk=self.kwargs.get('inv_pk'),
        #     pargdyn=self.request.GET.get('argdyn'),
        #     pattr=self.request.GET.get('attr')
        # )

        return super(AddToProfileRedirectView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to
        # return reverse('tasks:actq_detail', kwargs={'pk': self.actq})

        # return reverse('tasks:act_list')
        # return super().get_redirect_url(*args, **kwargs)


class AddTicketAndCloseView(LoginRequiredMixin, PermissionRequiredMixin, generic.FormView):
    template_name = 'tasks/task_form_addticketandclose.html'
    permission_required = ('invs.view_inv', 'tasks.view_task')
    form_class = AddTicketAndCloseForm
    success_url = reverse_lazy('tasks:task_list')
    # success_url = '../'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(AddTicketAndCloseView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # kwargs['user'] = self.request.user
        kwargs['taskname'] = Task.objects.get(pk=self.kwargs.get('task_pk')).title
        return super(AddTicketAndCloseView, self).get_context_data(**kwargs)

    # def get_initial(self):
    #     initial = super(AddTicketAndCloseView, self).get_initial()
    #     if self.request.user.is_authenticated:
    #         initial.update({'name': self.request.user.get_full_name()})
    #     return initial

    def form_valid(self, form):
        cleandata = form.cleaned_data
        auser = self.request.user.get_username()
        auser_obj = self.request.user
        cdescription = cleandata.get('ticket')
        cstatus = cleandata.get('status')
        task_pk = self.kwargs.get('task_pk')
        task_obj_list = Task.objects.filter(pk=task_pk)
        task_obj = task_obj_list[0]
        inv_obj = task_obj.inv
        # add an evidence
        evidence_obj = new_evidence(
            puser=auser_obj,
            ptask=task_obj,
            pinv=inv_obj,
            pcreated_by=auser,
            pmodified_by=auser,
            pdescription=cdescription,
            pevformat=None,
            pparent=None,
            pparentattr=None,
            pfilename=None,
            # pfilename=None,
            pfileref=None,
            # pfileref=None,
            pforce=True,
        )
        task_obj_list.update(status=cstatus)

        return super(AddTicketAndCloseView, self).form_valid(form)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_task'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:tsk_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(AddTicketAndCloseView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(AddTicketAndCloseView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        # kwargs['user'] = self.request.user
        return kwargs


#  ##################  AJAX
# @method_decorator(csrf_exempt, name='dispatch')
class XEvidenceCreateAjaxView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Evidence
    form_class = EvidenceForm
    permission_required = ('tasks.add_evidence',)
    # success_url = 'invs:inv_list'
    # template_name = 'invs/inv_form_create_ajax.html'
    # success_url = reverse_lazy('invs:inv_list')
    ajax_partial = 'tasks/evidence_form_create_ajax.html'
    # ajax_list = 'tasks/evidence_list.html'
    # ajax_list = 'invs/inv_detail_tab_evidences.html'
    ajax_list = 'tasks/evidence_list_tablebody.html'
    context_object_name = 'object_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(XEvidenceCreateAjaxView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data()
        if request.is_ajax():
            html_form = render_to_string(self.ajax_partial, context, request)
            return JsonResponse({'html_form': html_form})
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(XEvidenceCreateAjaxView, self).get_context_data(**kwargs)
        # context = super(XEvidenceCreateAjaxView, self).get_context_data(**kwargs)
        # evs = Evidence.objects.all()
        # context['object_list'] = evs
        # return context

    def form_valid(self, form):
        data = dict()
        context = self.get_context_data()

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.modified_by = self.request.user.get_username()
            self.object.created_by = self.request.user.get_username()
            if self.request.FILES:
                self.object.fileName = self.request.FILES['fileRef'].name
            self.object.save()
            data['form_is_valid'] = True
            data['html_data_list'] = render_to_string(
                self.ajax_list, context, self.request)
        else:
            data['form_is_valid'] = False
        data['html_form'] = render_to_string(
            self.ajax_partial, context, request=self.request)

        if self.request.is_ajax():
            return JsonResponse(data)
        else:
            return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_evidence'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('tasks:ev_list')
        else:
            pass
        # Checks pass, let http method handlers process the request
        return super(XEvidenceCreateAjaxView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(XEvidenceCreateAjaxView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        inv_pk = self.kwargs.get('inv_pk')
        task_pk = self.kwargs.get('task_pk')
        if inv_pk:
            # self.inv_pk = inv_pk
            pass
        else:
            inv_pk = 0
        if task_pk:
            # self.task_pk = task_pk
            pass
        else:
            task_pk = 0

        kwargs['inv_pk'] = inv_pk
        kwargs['task_pk'] = task_pk
        kwargs['user'] = self.request.user
        return kwargs


# @method_decorator(csrf_exempt, name='dispatch')
class InvEvidenceCreateAjaxView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Evidence
    form_class = EvidenceForm
    permission_required = ('tasks.add_evidence',)
    # success_url = 'invs:inv_list'
    # template_name = 'invs/inv_form_create_ajax.html'
    # success_url = reverse_lazy('invs:inv_list')
    # ajax_partial = 'tasks/evidence_form_create_ajax.html'
    ajax_partial = 'tasks/invevidence_form_create_ajax.html'
    # ajax_list = 'tasks/evidence_list.html'
    # ajax_list = 'invs/inv_detail_tab_evidences.html'
    ajax_list = 'invs/inv_detail_tab_evidences_tablebody.html'
    context_object_name = 'inv'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvEvidenceCreateAjaxView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # return super(InvEvidenceCreateAjaxView, self).get_context_data(**kwargs)
        context = super(InvEvidenceCreateAjaxView, self).get_context_data(**kwargs)
        inv_pk = self.kwargs.get('inv_pk')
        # inv = Inv.objects.get(pk=inv_pk)
        # context['inv'] = inv
        #
        # invevidences = inv.evidence_inv.all()\
        #     .select_related('task') \
        #     .select_related('evidenceformat')\
        #     .select_related('mitretactic') \
        #     .select_related('parent') \
        #     .select_related('parentattr')
        # invevidences2 = invevidences
        # context['invevidences'] = invevidences.iterator()
        # # kwargs['invevidences2_exist'] = invevidences.exists()
        # context['invevidences2'] = invevidences2.iterator()

        # inv = Inv.objects.filter(pk=inv_pk) \
        #     .select_related('status')[0].order_by('pk')
        # invevidences = invs.evidence_inv.all()\
        #     .select_related('task') \
        #     .select_related('evidenceformat')\
        #     .select_related('mitretactic') \
        #     .select_related('parent') \
        #     .select_related('parentattr')
        # invevidences = invs.evidences_table()
        # invevidences2 = invevidences
        # kwargs['inv'] = invs
        # invevidences = Inv.objects.filter(pk=inv_pk) \
        #     .select_related('evidence_inv__pk') \
        #     .select_related('evidence_inv__fileRef') \
        #     .select_related('evidence_inv__fileName') \
        #     .select_related('evidence_inv__task__pk') \
        #     .select_related('evidence_inv__task__title') \
        #     .select_related('evidence_inv__created_at') \
        #     .select_related('evidence_inv__created_by') \
        #     .select_related('evidence_inv__modified_at') \
        #     .select_related('evidence_inv__modified_by') \
        #     .select_related('evidence_inv__mitretactic__name') \
        #     .select_related('evidence_inv__parent__pk') \
        #     .select_related('evidence_inv__parentattr__pk') \
        #     .select_related('evidence_inv__evidenceformat__pk') \
        #     .select_related('evidence_inv__description') \
        #     .values('pk', 'evidence_inv__pk', 'evidence_inv__fileRef', 'evidence_inv__fileName',
        #             'evidence_inv__task__pk', 'evidence_inv__task__title', 'evidence_inv__created_at',
        #             'evidence_inv__created_by', 'evidence_inv__modified_at', 'evidence_inv__modified_by',
        #             'evidence_inv__mitretactic__name', 'evidence_inv__parent__pk', 'evidence_inv__parentattr__pk',
        #             'evidence_inv__evidenceformat__pk', 'evidence_inv__description')
        invevidences = InvDetailTabEvidences().inv_tab_evidences_invevidences(inv_pk)
        invevidences2 = invevidences
        context['inv'] = InvDetailTabEvidences().inv_tab_evidences_inv(inv_pk)
        context['invevidences'] = invevidences
        context['invevidences2'] = invevidences2
        # context['actions'] = Action.objects.filter(enabled=True) \
        #     .select_related('scriptinput')\
        #     .select_related('outputtarget')\
        #     .select_related('scriptinputattrtype')
        context['actions'] = TasksInvDetailTabEvidences().inv_tab_evidences_actions()

        actgrpitems = actiongroupmember_items()
        context['actiongroups_desc'] = actgrpitems['actiongroups_desc']
        context['actiongroups_file'] = actgrpitems['actiongroups_file']
        context['actiongroups_attr'] = actgrpitems['actiongroups_attr']
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data()
        if request.is_ajax():
            html_form = render_to_string(self.ajax_partial, context, request)
            return JsonResponse({'html_form': html_form})
        else:
            return super(InvEvidenceCreateAjaxView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        data = dict()
        context = self.get_context_data()
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.modified_by = self.request.user.get_username()
            self.object.created_by = self.request.user.get_username()
            # file upload is not possible via ajax other than async upload
            if self.request.FILES:
                self.object.fileName = self.request.FILES['fileRef'].name
            self.object.save()
            data['form_is_valid'] = True
            # logger.info(self.ajax_list)
            data['html_data_list'] = render_to_string(
                self.ajax_list, context, self.request)
        else:
            data['form_is_valid'] = False

        data['html_form'] = render_to_string(
            self.ajax_partial, context, request=self.request)

        if self.request.is_ajax():
            return JsonResponse(data)
        else:
            return super(InvEvidenceCreateAjaxView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.add_evidence'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('invs:inv_list')
        else:
            pass
        # Checks pass, let http method handlers process the request
        return super(InvEvidenceCreateAjaxView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(InvEvidenceCreateAjaxView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        # inv_pk = self.kwargs.get('inv_pk')
        # task_pk = self.kwargs.get('task_pk')
        # if inv_pk:
        #     # self.inv_pk = inv_pk
        #     pass
        # else:
        #     inv_pk = 0
        # if task_pk:
        #     # self.task_pk = task_pk
        #     pass
        # else:
        #     task_pk = 0
        #
        # kwargs['inv_pk'] = inv_pk
        # kwargs['task_pk'] = task_pk
        inv_pk = self.kwargs.get('inv_pk')
        task_pk = self.kwargs.get('task_pk')
        # if inv_pk:
        #     pass
        # else:
        #     inv_pk = 0
        # if task_pk:
        #     pass
        # else:
        #     task_pk = 0
        #
        # kwargs['inv_pk'] = inv_pk
        # kwargs['task_pk'] = task_pk
        # if inv_pk:
        #     kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=inv_pk, allownull=True)
        #     pass
        # else:
        #     kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=None, allownull=True)
        #     inv_pk = 0
        if task_pk:
            pass
        else:
            task_pk = 0
        kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=None, allownull=True)
        kwargs['tasklist'] = TaskList.get_tasklist(Task.objects.none(), pinv=inv_pk, pexcltask=None, pallownull=True,
                                                   porder_by='pk')
        kwargs['inv_pk'] = inv_pk
        kwargs['task_pk'] = task_pk

        kwargs['user'] = self.request.user
        return kwargs


class InvEvidenceUpdateAjaxView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Evidence
    form_class = EvidenceForm
    permission_required = ('tasks.change_evidence',)
    ajax_partial = 'tasks/invevidence_form_update_ajax.html'
    ajax_list = 'invs/inv_detail_tab_evidences_tablebody.html'
    context_object_name = 'inv'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvEvidenceUpdateAjaxView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # return super(InvEvidenceUpdateAjaxView, self).get_context_data(**kwargs)
        context = super(InvEvidenceUpdateAjaxView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        ev_obj = Evidence.objects.get(pk=pk)
        inv_obj = ev_obj.inv
        context['inv'] = inv_obj
        context['evformat'] = ev_obj.evidenceformat.pk



        inv_pk = inv_obj.pk
        invevidences = InvDetailTabEvidences().inv_tab_evidences_invevidences(inv_pk)
        invevidences2 = invevidences
        context['inv'] = InvDetailTabEvidences().inv_tab_evidences_inv(inv_pk)
        context['invevidences'] = invevidences
        context['invevidences2'] = invevidences2
        context['actions'] = TasksInvDetailTabEvidences().inv_tab_evidences_actions()
        actgrpitems = actiongroupmember_items()
        context['actiongroups_desc'] = actgrpitems['actiongroups_desc']
        context['actiongroups_file'] = actgrpitems['actiongroups_file']
        context['actiongroups_attr'] = actgrpitems['actiongroups_attr']




        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        if request.is_ajax():
            html_form = render_to_string(self.ajax_partial, context, request)
            return JsonResponse({'html_form': html_form})
        else:
            return super(InvEvidenceUpdateAjaxView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        data = dict()
        context = self.get_context_data()
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.modified_by = self.request.user.get_username()
            if self.request.FILES:
                self.object.fileName = self.request.FILES['fileRef'].name
            self.object.save()
            data['form_is_valid'] = True
            # logger.info(self.ajax_list)
            data['html_data_list'] = render_to_string(
                self.ajax_list, context, self.request)
        else:
            data['form_is_valid'] = False

        data['html_form'] = render_to_string(
            self.ajax_partial, context, request=self.request)

        if self.request.is_ajax():
            return JsonResponse(data)
        else:
            return super(InvEvidenceUpdateAjaxView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        ev_obj = self.kwargs.get('pk')
        ev_pk = Evidence.objects.get(pk=ev_obj)
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('tasks.change_evidence'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('tasks:ev_detail', pk=ev_obj)
        elif ev_pk.task and ev_pk.task.status.name == "Completed":
            messages.error(self.request, "Task is Completed!!!")
            return redirect('tasks:ev_detail', pk=ev_obj)
        elif ev_pk.task and ev_pk.task.status.name == "Skipped":
            messages.error(self.request, "Task is Skipped!!!")
            return redirect('tasks:ev_detail', pk=ev_obj)
        elif ev_pk.inv and ev_pk.inv.status.name == "Closed":
            messages.error(self.request, "Investigation is Closed!!!")
            return redirect('tasks:ev_detail', pk=ev_obj)
        elif ev_pk.inv and ev_pk.inv.status.name == "Archived":
            messages.error(self.request, "Investigation is Archived!!!")
            return redirect('tasks:ev_detail', pk=ev_obj)
        # Checks pass, let http method handlers process the request
        return super(InvEvidenceUpdateAjaxView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(InvEvidenceUpdateAjaxView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        # inv_pk = self.kwargs.get('inv_pk')
        # task_pk = self.kwargs.get('task_pk')
        pk = self.kwargs.get('pk')
        ev = Evidence.objects.get(pk=pk)
        # inv_pk = ev.inv.pk
        # task_pk = ev.task.pk
        if ev.inv:
            inv_pk = ev.inv.pk
            pass
        else:
            inv_pk = 0
        if ev.task:
            task_pk = ev.task.pk
            pass
        else:
            task_pk = 0
        #
        # kwargs['inv_pk'] = inv_pk
        # kwargs['task_pk'] = task_pk
        # inv_pk = self.kwargs.get('inv_pk')
        # task_pk = self.kwargs.get('task_pk')
        # if inv_pk:
        #     pass
        # else:
        #     inv_pk = 0
        # if task_pk:
        #     pass
        # else:
        #     task_pk = 0
        #
        # kwargs['inv_pk'] = inv_pk
        # kwargs['task_pk'] = task_pk
        # if inv_pk:
        #     kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=inv_pk, allownull=True)
        #     pass
        # else:
        #     kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=None, allownull=True)
        #     inv_pk = 0
        if task_pk:
            pass
        else:
            task_pk = 0
        kwargs['invlist'] = InvList.get_invlist(Inv.objects.none(), pexcl=None, allownull=True)
        kwargs['tasklist'] = TaskList.get_tasklist(Task.objects.none(), pinv=inv_pk, pexcltask=None, pallownull=True,
                                                   porder_by='pk')
        # print("UPDATE: %s %s"%(inv_pk, task_pk))
        # if kwargs['invlist']:
        #     print("INVLIST OK")
        # else:
        #     print("INVLIST FAIL")
        # if kwargs['tasklist']:
        #     print("TASKLIST OK")
        # else:
        #     print("TASKLIST FAIL")
        kwargs['inv_pk'] = inv_pk
        kwargs['task_pk'] = task_pk
        kwargs['user'] = self.request.user
        return kwargs
