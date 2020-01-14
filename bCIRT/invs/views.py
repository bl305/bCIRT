# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : invs/view.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : View file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# 2019.09.06  Lendvay     2      Added session security
# 2019.11.29  Lendvay     3      Added reviewers
# **********************************************************************;
from tasks.models import TaskTemplate, PlaybookTemplate, Action, ActionGroupMember
from tasks.models import new_playbook, new_evidence, task_close
from django.core.exceptions import ValidationError
from django.utils.timezone import now as timezone_now
# from django.utils.translation import gettext_lazy as _
# from tasks.models import Task, Playbook
import os
import shutil
from io import BytesIO
from django.core.files import File
import tempfile
# from zipfile import ZipFile
import zipfile
from bCIRT.settings import MEDIA_ROOT
from shutil import copyfile
from django.shortcuts import redirect, reverse, get_object_or_404  # ,render,
from django.http import JsonResponse
from django.template.loader import render_to_string
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# to manage manual uploads
# from os import path
# from bCIRT.custom_variables import MYMEDIA_ROOT
# from django.http import HttpResponseRedirect
# from django.shortcuts import render
##############

from .forms import InvForm, InvSuspiciousEmailForm, InvReviewer1Form, InvReviewer2Form
from .models import Inv, InvStatus, new_inv, InvCategory, InvAttackVector, InvPhase, InvSeverity, CurrencyType,\
    InvPriority  # , InvReviewRules
# from django.shortcuts import redirect, reverse    # ,render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.views import generic
import logging
from bCIRT.custom_variables import LOGLEVEL, LOGSEPARATOR
from django.utils.http import is_safe_url
from bCIRT.settings import ALLOWED_HOSTS
# check remaining session time
# from django.contrib.sessions.models import Session
# from datetime import datetime, timezone
# check remaining session time
from django.template.loader import get_template
# from wkhtmltopdf.views import PDFTemplateResponse
from django.contrib.auth import get_user_model
User = get_user_model()
logger = logging.getLogger('log_file_verbose')


# Create your views here.
# class MyPDFView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
#     # context = {"title": "Task evidences"}  # data that has to be rendered to pdf template
#     model = Inv
#     permission_required = ('invs.view_inv', 'tasks.view_evidence', 'tasks.view_task', 'tasks.view_playbook')
#     context = {"title": "Investigation evidences"}
#
#     def __init__(self, *args, **kwargs):
#         if LOGLEVEL == 1:
#             pass
#         elif LOGLEVEL == 2:
#             pass
#         elif LOGLEVEL == 3:
#             logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
#             logger.info(logmsg)
#         super(MyPDFView, self).__init__(*args, **kwargs)
#
#     def get(self, request, *args, **kwargs):
#         self.context['inv'] = self.get_object()
#         self.context['user'] = self.request.user.get_username()
#
#         html_template = get_template('invs/inv_detail_REPORT_v1.html')
#
#         # rendered_html = html_template.render(self.context)
#         #
#         # css_path = custom_params.PROJECT_ROOT + '/static/bCIRT/bootstrap-3.3.7/css/bootstrap.min.css'
#         # pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(css_path)])
#         # # pdf_file = HTML(string=rendered_html).write_pdf()
#
#         # http_response = HttpResponse(pdf_file, content_type='application/pdf')
#         # http_response['Content-Disposition'] = 'filename="report_investigation.pdf"'
#         response = PDFTemplateResponse(request=request,
#                                        template=html_template,
#                                        filename="investigation_report_" + str(self.get_object().pk) + ".pdf",
#                                        context=self.context,
#                                        show_content_in_browser=False,
#                                        cmd_options={'margin-top': 10,
#                                                     "zoom": 1,
#                                                     "viewport-size": "1366 x 513",
#                                                     'javascript-delay': 1000,
#                                                     'footer-center': '[page]/[topage]',
#                                                     "no-stop-slow-scripts": True},
#                                        )
#         return response


class InvDetailPrintView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Inv
    template_name = 'invs/inv_detail_REPORT_v1.html'
    permission_required = ('invs.view_inv',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvDetailPrintView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['templatecategories'] = TaskTemplate.objects.filter(enabled=True)
        kwargs['playbooks'] = PlaybookTemplate.objects.filter(enabled=True)
        kwargs['actions'] = Action.objects.filter(enabled=True)
        return super(InvDetailPrintView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.view_inv'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('invs:inv_list')
        # Checks pass, let http method handlers process the request
        return super(InvDetailPrintView, self).dispatch(request, *args, **kwargs)


# TESTING EXPORT
# https://simpleisbetterthancomplex.com/packages/2016/08/11/django-import-export.html
from django.http import HttpResponse
from .resources import InvResource


#
# def exportreviewrules(request):
#     invreviewrules_resource = InvReviewRulesResource()
#     dataset = invreviewrules_resource.export()
#     response = HttpResponse(dataset.json, content_type='application/json')
#     response['Content-Disposition'] = 'attachment; filename="invreviewrules.json"'
#     return response
class ExportInvView(LoginRequiredMixin, PermissionRequiredMixin, generic.View):
    # Exports the Inv table details into JSON

    # context = {"title": "Task evidences"}  # data that has to be rendered to pdf template
    # model = InvReviewRules
    permission_required = ('invs.view_inv', 'tasks.view_evidence', 'tasks.view_task', 'tasks.view_playbook')
    context = {"title": "Investigation Export"}

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ExportInvView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        # self.context['invrule'] = self.get_object()
        # self.context['user'] = self.request.user.get_username()
        inv_resource = InvResource()
        # to filter enable the following lines below
        inv_pk = self.kwargs.get('pk')
        queryset = Inv.objects.filter(pk=inv_pk)
        dataset = inv_resource.export(queryset)
        # filter end
        # nofilter
        # dataset = invreviewrules_resource.export()
        response = HttpResponse(dataset.json, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="inv_'+str(inv_pk)+'.json"'
        return response


class ExportInvFilesView(LoginRequiredMixin, PermissionRequiredMixin, generic.View):
    # Exports the Inv table details into JSON

    # context = {"title": "Task evidences"}  # data that has to be rendered to pdf template
    # model = InvReviewRules
    permission_required = ('invs.view_inv', 'tasks.view_evidence', 'tasks.view_task', 'tasks.view_playbook')
    context = {"title": "Investigation Export"}

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(ExportInvFilesView, self).__init__(*args, **kwargs)

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

    def get(self, request, *args, **kwargs):

        inv_pk = self.kwargs.get('pk')
        # queryset = Inv.objects.filter(pk=inv_pk)
        inv_obj = Inv.objects.get(pk=inv_pk)
        # inv_tasklist = inv_obj.tasklist()
        inv_evidencelist = inv_obj.evidence_inv.exclude(fileRef="")
        # fullfilepath = None

        # 1. create a temp folder
        # generate a random folder with some prefix:
        tempfile.tempdir = os.path.join(MEDIA_ROOT, "tmp")
        myprefix = "BCIRT-" + str(inv_pk)
        myprefix1 = myprefix + "-"
        myouttempdir1 = tempfile.TemporaryDirectory(prefix=myprefix1)
        #  make the tempdir the temp root
        tempfile.tempdir = myouttempdir1.name
        destoutdirpath = tempfile.gettempdir()

        for evitem in inv_evidencelist:
            # 2. copy the files into the temp folder
            # fullfilepath = os.path.join(MEDIA_ROOT, str(evitem.fileRef))
            destoutdirfilename = os.path.join(destoutdirpath, str(evitem.pk)+"_"+str(evitem.fileName))
            oldfile = os.path.join(MEDIA_ROOT, str(evitem.fileRef))
            # adding exception handling
            try:
                copyfile(oldfile, destoutdirfilename)
            except IOError as e:
                print("Unable to copy file. %s" % e)
            except Exception:
                print("Unexpected error:", Exception)

        destdir = myouttempdir1.name

        # report filename
        indexfilename = 'index.html'
        indexfilepath = os.path.join(destdir, indexfilename)
        context = {'pk': inv_pk, 'user': 'admin', 'inv': inv_obj}
        open(indexfilepath, "w").write(render_to_string('invs/inv_detail_REPORT_v1.html', context))

        # files zipping
        zipfile_memory = self.download_dir_zipped(destdir)
        zip_filename = "Export-Investigation-" + str(inv_pk) + ".zip"
        # Grab ZIP file from in-memory, make response with correct MIME-type
        resp = HttpResponse(content_type="application/x-zip-compressed")
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
        zipfile_memory.seek(0)
        resp.write(zipfile_memory.read())
        return resp


# #############################################################################3
# Investigation related views
class InvListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Inv
    form_class = InvForm
    permission_required = ('invs.view_inv',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(InvListView, self).get_context_data(**kwargs)


class InvCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Inv
    form_class = InvForm
    permission_required = ('invs.add_inv',)
    success_url = 'invs:inv_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(InvCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # self.object.user = self.request.user
        self.object.user = self.request.user
        self.object.modified_by = self.request.user.get_username()
        self.object.created_by = self.request.user.get_username()
        self.object.save()
        return super(InvCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.add_inv'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('invs:inv_list')
        else:
            pass
        # Checks pass, let http method handlers process the request
        return super(InvCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(InvCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        # kwargs['inv_pk'] = self.kwargs.get('inv_pk')
        kwargs['user'] = self.request.user
        return kwargs


class InvDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Inv
    permission_required = ('invs.view_inv',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['templatecategories'] = TaskTemplate.objects.filter(enabled=True)
        kwargs['playbooks'] = PlaybookTemplate.objects.filter(enabled=True)
        kwargs['actions'] = Action.objects.filter(enabled=True)
        # inv_obj = Inv.objects.get(pk=self.kwargs.get('pk'))
        # ev_obj = inv_obj.evidence_inv.all()
        # evattr_set = set()
        # for ev_obj_item in ev_obj:
        #     if ev_obj_item.evattr_evidence.all():
        #         for evattr_obj in ev_obj_item.evattr_evidence.all():
        #             evattr_set.add(evattr_obj)
        # kwargs['invevidence_evattr_evidence_all'] = evattr_set
        # actiongrmember_file = set()
        # actiongrmember_desc = set()
        # actiongrmember_attr = set()
        actiongroups_file = set()
        actiongroups_desc = set()
        actiongroups_attr = set()
        if ActionGroupMember.objects.all():
            for actgrpmember in ActionGroupMember.objects.all():
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
        # print(actiongr_desc)
        # print(actiongr_file)
        # print(actiongr_attr)
        # kwargs['actiongroupmembers_desc'] = actiongrmember_desc
        # kwargs['actiongroupmembers_file'] = actiongrmember_file
        # kwargs['actiongroupmembers_attr'] = actiongrmember_attr
        kwargs['actiongroups_desc'] = actiongroups_desc
        kwargs['actiongroups_file'] = actiongroups_file
        kwargs['actiongroups_attr'] = actiongroups_attr
        return super(InvDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.view_inv'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('invs:inv_list')
        # Checks pass, let http method handlers process the request
        return super(InvDetailView, self).dispatch(request, *args, **kwargs)


class InvUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    redirect_field_name = 'invs/inv_detail.html'
    form_class = InvForm
    model = Inv
    permission_required = ('invs.change_inv',)
    success_url = 'invs:inv_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(InvUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.change_inv'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('invs:inv_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(InvUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        self.object.save()
        return super(InvUpdateView, self).form_valid(form)


class InvRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Inv
    permission_required = ('invs.delete_inv',)
    success_url = 'invs:inv_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        return reverse(self.success_url)

    def get_context_data(self, **kwargs):
        return super(InvRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.delete_inv'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('invs:inv_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(InvRemoveView, self).dispatch(request, *args, **kwargs)


class InvAssignView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):
    permission_required = ('invs.view_inv', 'invs.change_inv')
    success_url = 'invs:inv_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvAssignView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.change_inv'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('invs:inv_list')
        inv_pk = self.kwargs.get('pk')
        # Checks pass, let http method handlers process the request
        Inv.objects.filter(pk=inv_pk).update(user=self.request.user)
        assigned_obj = InvStatus.objects.get(name='Assigned')
        Inv.objects.filter(pk=inv_pk).update(status=assigned_obj)
        # return redirect(self.success_url)
        return super(InvAssignView, self).dispatch(request, *args, **kwargs)

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


class InvReview1UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    redirect_field_name = 'invs/inv_detail.html'
    form_class = InvReviewer1Form
    model = Inv
    permission_required = ('invs.change_inv',)
    success_url = 'invs:inv_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvReview1UpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        # kwargs['instance'] = Inv.objects.all()
        return super(InvReview1UpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.change_inv'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('invs:inv_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(InvReview1UpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # self.object.modified_by = self.request.user.get_username()
        self.object.reviewer1 = self.request.user  # .get_username()
        self.object.status = InvStatus.objects.get(pk=3)
        self.object.save()
        return super(InvReview1UpdateView, self).form_valid(form)


class InvReview2UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    redirect_field_name = 'invs/inv_detail.html'
    form_class = InvReviewer2Form
    model = Inv
    permission_required = ('invs.change_inv',)
    success_url = 'invs:inv_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvReview2UpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        # kwargs['instance'] = Inv.objects.all()
        return super(InvReview2UpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.change_inv'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('invs:inv_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(InvReview2UpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # self.object.modified_by = self.request.user.get_username()
        self.object.reviewer2 = self.request.user  # .get_username()
        self.object.status = InvStatus.objects.get(pk=3)
        self.object.save()
        return super(InvReview2UpdateView, self).form_valid(form)


class InvReview1CompleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):
    permission_required = ('invs.view_inv', 'invs.change_inv')
    success_url = 'invs:inv_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvReview1CompleteView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.change_inv'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('invs:inv_list')
        inv_pk = self.kwargs.get('pk')
        inv_obj = Inv.objects.get(pk=inv_pk)
        # Checks pass, let http method handlers process the request
        assigned_obj = InvStatus.objects.get(name='Review2')

        # Inv.objects.filter(pk=inv_pk).update(user=self.request.user)
        # Inv.objects.filter(pk=inv_pk).update(reviewer1=self.request.user)
        # Inv.objects.filter(pk=inv_pk).update(reviewed1_by=self.request.user.get_username())
        # Inv.objects.filter(pk=inv_pk).update(reviewed1_at=timezone_now())
        # Inv.objects.filter(pk=inv_pk).update(status=assigned_obj)
        try:
            inv_obj.full_clean()
            reviewers2 = User.objects.filter(profile__reviewer2=True)
            reviewers2list = set()
            for reviewer2 in reviewers2:
                reviewers2list.add(reviewer2)
            randomreviewer2 = reviewers2.order_by("?").first()
            # Inv.objects.filter(pk=inv_pk).update(reviewer2=randomreviewer2)


            # inv_obj.user=self.request.user
            inv_obj.reviewer1=self.request.user
            inv_obj.reviewed1_by=self.request.user.get_username()
            inv_obj.reviewed1_at=timezone_now()
            inv_obj.status=assigned_obj
            inv_obj.reviewer2=randomreviewer2
            inv_obj.save()

        except ValidationError as e:
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('invs:inv_detail', pk=inv_pk)
        # return redirect(self.success_url)
        return super(InvReview1CompleteView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to


class InvReview2CompleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.RedirectView):
    permission_required = ('invs.view_inv', 'invs.change_inv')
    success_url = 'invs:inv_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvReview2CompleteView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('invs.change_inv'):
            inv_pk = self.kwargs.get('pk')
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('invs:inv_detail', pk=inv_pk)
        inv_pk = self.kwargs.get('pk')
        # Checks pass, let http method handlers process the request
        # Inv.objects.filter(pk=inv_pk).update(user=self.request.user)
        assigned_obj = InvStatus.objects.get(name='Closed')
        # Inv.objects.filter(pk=inv_pk).update(status=assigned_obj)
        inv_obj = Inv.objects.get(pk=inv_pk)
        # Inv.objects.filter(pk=inv_pk).update(reviewer2=self.request.user)
        # Inv.objects.filter(pk=inv_pk).update(reviewed2_by=self.request.user.get_username())
        # Inv.objects.filter(pk=inv_pk).update(reviewed2_at=timezone_now())
        # Inv.objects.filter(pk=inv_pk).update(status=assigned_obj)
        try:
            inv_obj.full_clean()
            inv_obj.reviewer2 = self.request.user
            inv_obj.reviewed2_by = self.request.user.get_username()
            inv_obj.reviewed2_at = timezone_now()
            inv_obj.status = assigned_obj
            inv_obj.save()
        except ValidationError as e:
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('invs:inv_detail', pk=inv_pk)
            # raise ValidationError(_('First review must happen first!'))
        # https://goodcode.io/articles/django-assert-raises-validationerror/

        # return redirect(self.success_url)
        return super(InvReview2CompleteView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

# ########### TESTING
# from django.shortcuts import render
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
#
# def simple_upload(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         print(request.POST.get('description'))
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
#         return render(request, 'invs/inv_invphishing.html', {
#             'uploaded_file_url': uploaded_file_url
#         })
#     return render(request, 'invs/inv_invphishing.html')

# def upload_file(request):
#     if request.method == 'POST':
#         form = InvSuspiciousEmailForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file_chunks(request.FILES['file'], '/tmp/aaa.txt')
#             return HttpResponseRedirect('home')
#     else:
#         form = InvSuspiciousEmailForm()
#     return render(request, 'upload.html', {'form': form})


class InvSuspiciousEmailCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.FormView):
    # template_name = "invs/inv_invphishing.html"
    template_name = 'invs/inv_form.html'
    form_class = InvSuspiciousEmailForm
    permission_required = ('invs.view_inv', 'tasks.view_task')
    success_url = '../'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvSuspiciousEmailCreateView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # kwargs['user'] = self.request.user
        # kwargs['invs'] = Inv.objects.filter(user=self.request.user, status=3)
        return super(InvSuspiciousEmailCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):

        cleandata = form.cleaned_data
        auser = self.request.user.get_username()
        auser_obj = self.request.user
        cinvid = cleandata['invid']
        if cinvid is None or cinvid == "":
            cinvid = 'Phishing'
        cdescription = cleandata['description']
        if cdescription is None or cdescription == "":
            cdescription = 'Phishing'
        cticket = cleandata['ticket']
        creference = cleandata['reference']
        cfileref = cleandata['fileRef']
        inv_obj = new_inv(puser=auser_obj,
                          pparent=None,
                          # pinvid="Suspicious Email",
                          pinvid=cinvid,
                          pticketid=cticket,
                          prefid=creference,
                          pstatus=InvStatus.objects.get(name="Assigned"),
                          pphase=InvPhase.objects.get(pk=2),
                          pseverity=InvSeverity.objects.get(pk=2),
                          pcategory=InvCategory.objects.get(pk=6),
                          ppriority=InvPriority.objects.get(pk=1),
                          pattackvector=InvAttackVector.objects.get(name="Phishing"),
                          pdescription=cdescription,
                          psummary="Suspicious email",
                          pcomment=None,
                          pstarttime=None,
                          pendtime=None,
                          pinvduration=None,
                          pcreated_at=None,
                          pcreated_by=auser,
                          pmodified_at=None,
                          pmodified_by=auser,
                          pmonetaryloss=0,
                          plosscurrency=CurrencyType.objects.get(pk=1),
                          pnumofvictims=None
                          )
        # add the uploaded file to evidences without assigning to any task
        # if the file is email, the evidence need to be attached to the first task
        evidence_obj = new_evidence(
            puser=auser_obj,
            ptask=None,
            pinv=inv_obj,
            pcreated_by=auser,
            pmodified_by=auser,
            pdescription=cdescription,
            pevformat=None,
            pparent=None,
            pparentattr=None,
            pfilename=cfileref.name,
            # pfilename=None,
            pfileref=cfileref,
            # pfileref=None,
            pforce=True,
        )

        cfileext = os.path.basename(str(cfileref)).split(".")[-1]
        if ((cfileext.lower() == 'eml') or (cfileext.lower() == 'msg')) \
                and PlaybookTemplate.objects.filter(name="Suspicious Email"):
            # use the file as an evidence, assign it to the first task
            # Need to create a playbook and tasks within it using the suspicious email template
            playbooktemplate_obj = PlaybookTemplate.objects.get(name="Suspicious Email")
            playbook_obj = new_playbook(pplaybooktemplate=playbooktemplate_obj,
                                        pname=playbooktemplate_obj.name,
                                        pversion=playbooktemplate_obj.version,
                                        puser=auser_obj,
                                        pinv=inv_obj,
                                        pdescription=playbooktemplate_obj.description,
                                        pmodified_by=auser,
                                        pcreated_by=auser
                                        )
            # find first task
            first_task = None
            if playbook_obj.task_playbook.last():
                first_task = playbook_obj.task_playbook.last()
            # add evidence to the first task
            evidence_obj.task = first_task
            evidence_obj.save()
            # this will attach the file to the first evidence
            # need to close the first task
            task_close(first_task.pk, 'action')

        elif cfileext == 'zip':
            # this means the intput is a ZIP file
            # generate a random folder with some prefix:

            ev_pk = evidence_obj.pk
            tempfile.tempdir = os.path.join(MEDIA_ROOT, "tmp")
            myprefix1 = "EVtmp-" + str(ev_pk) + "-"
            myouttempdir1 = tempfile.TemporaryDirectory(prefix=myprefix1)
            #  make the tempdir the temp root
            tempfile.tempdir = myouttempdir1.name
            # with tempfile.TemporaryDirectory() as directory:
            # destdir = myouttempdir.name
            # standard dir where output files will be stored
            #            destoutdir = tempfile.mkdtemp()
            #           destoutdirpath = MEDIA_ROOT +  destoutdir
            # destoutdirname = MEDIA_ROOT + str(destoutdir) + str(cfileref)
            destoutdirpath = tempfile.gettempdir()
            # destoutdirfilename = os.path.join(destoutdirpath, cfileref.name)
            destoutdirfilename = os.path.join(destoutdirpath, evidence_obj.fileName)
            # destoutdirname = destoutdirpath + "/" + cfileref.name
            # Create a ZipFile Object and load sample.zip in it
            # oldfile = MEDIA_ROOT + str(evidence_obj.fileRef)
            oldfile = os.path.join(MEDIA_ROOT, str(evidence_obj.fileRef))
            #            print("tempdir: %s"%(destoutdir.gettempdir()))
            # TBD copy the original evidence
            # copyfile(oldfile, destoutdirname)
            # adding exception handling
            try:
                copyfile(oldfile, destoutdirfilename)
            except IOError as e:
                print("Unable to copy file. %s" % e)
                # exit(1)
            except Exception:
                print("Unexpected error:", Exception)
                # exit(1)

            # print("LIST1:%s"%(str(os.listdir(str(destoutdirpath)))))

            # TBD create a copy in a subfolder
            # copy files into it
            # ...
            # https://thispointer.com/python-how-to-unzip-a-file-extract-single-multiple-or-all-files-from-a-zip-archive/
            #            with ZipFile(destoutdirname, 'r') as zipObj:
            #                # Extract all the contents of zip file in different directory
            #                # zipObj.extractall(path=destoutdirpath, pwd=None)
            #                # Get a list of all archived file names from the zip
            #                listOfFileNames = zipObj.namelist()
            #                # Iterate over the file names
            #                for fileName in listOfFileNames:
            #                    # Check filename
            #                    if fileName.endswith('.txt') or fileName.endswith('txt'):
            #                        # Extract a single file from zip
            #                        zipObj.extract(member=fileName, path=destoutdirpath, pwd=None)

            my_dir = destoutdirpath
            my_zip = destoutdirfilename
            with zipfile.ZipFile(my_zip) as zip_file:
                for member in zip_file.namelist():
                    filename = os.path.basename(member)
                    # skip directories
                    if not filename:
                        continue
                    if filename.lower().endswith(".eml") or filename.lower().endswith(".msg"):
                        source = zip_file.open(member)
                        target = open(os.path.join(my_dir, filename), "wb")
                        with source, target:
                            try:
                                shutil.copyfileobj(source, target)
                            except Exception:
                                print("Error:%s" % Exception)

                        # print(os.path.join(destoutdirpath,filename))

                        # 2 create playbook for each file

                        # use the file as an evidence, assign it to the first task
                        # Need to create a playbook and tasks within it using the suspicious email template
                        playbooktemplate_obj = PlaybookTemplate.objects.get(name="Suspicious Email")
                        playbook_obj = new_playbook(pplaybooktemplate=playbooktemplate_obj,
                                                    pname=playbooktemplate_obj.name,
                                                    pversion=playbooktemplate_obj.version,
                                                    puser=auser_obj,
                                                    pinv=inv_obj,
                                                    pdescription=playbooktemplate_obj.description,
                                                    pmodified_by=auser,
                                                    pcreated_by=auser
                                                    )
                        # find first task
                        first_task = None
                        if playbook_obj.task_playbook.last():
                            first_task = playbook_obj.task_playbook.last()
                        # add evidence to the first task
                        filetouploadpath = os.path.join(destoutdirpath, target.name)
                        # print("filetouploadpath:%s" % (filetouploadpath))
                        filetoupload = open(filetouploadpath)

                        new_evidence(
                            puser=auser_obj,
                            ptask=first_task,
                            pinv=inv_obj,
                            pcreated_by=auser,
                            pmodified_by=auser,
                            pdescription=cdescription,
                            pevformat=None,
                            pparent=None,
                            pparentattr=None,
                            # pfilename=cfileref.name,
                            pfilename=target.name,
                            # pfilename=None,
                            # pfileref=cfileref,
                            pfileref=File(filetoupload),
                            # pfileref=None,
                            pforce=True,
                        )
                        filetoupload.close()
                        # this will attach the file to the evidence
                        # evidence_obj.fileRef.save(cfileref.name, cfileref)

                        # need to close the first task
                        task_close(first_task.pk, 'action')
        return super(InvSuspiciousEmailCreateView, self).form_valid(form)

        # def get_success_url(self):
        #     if 'next1' in self.request.GET:
        #         redirect_to = self.request.GET['next1']
        #         if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
        #             return reverse(self.success_url)
        #     else:
        #         return reverse(self.success_url)
        #     return redirect_to


class InvTabDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = 'invs/inv_detail_tab_detail_home.html'
    permission_required = ('invs.view_inv', 'tasks.view_task')

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvTabDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InvTabDetailView, self).get_context_data(**kwargs)
        kwargs['inv'] = Inv.objects.get(pk=self.kwargs.get('pk'))
        return kwargs


class InvTabProfileView(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = 'invs/inv_detail_tab_profile_home.html'
    permission_required = ('invs.view_inv', 'tasks.view_task')

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvTabProfileView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InvTabProfileView, self).get_context_data(**kwargs)
        kwargs['inv'] = Inv.objects.get(pk=self.kwargs.get('pk'))
        return kwargs


class InvTabPlaybookView(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = 'invs/inv_detail_tab_playbooks_home.html'
    permission_required = ('invs.view_inv', 'tasks.view_task')

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvTabPlaybookView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InvTabPlaybookView, self).get_context_data(**kwargs)
        kwargs['inv'] = Inv.objects.get(pk=self.kwargs.get('pk'))
        kwargs['playbooks'] = PlaybookTemplate.objects.filter(enabled=True)
        return kwargs


class InvTabTasksView(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = 'invs/inv_detail_tab_tasks_home.html'
    permission_required = ('invs.view_inv', 'tasks.view_task')

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvTabTasksView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InvTabTasksView, self).get_context_data(**kwargs)
        kwargs['inv'] = Inv.objects.get(pk=self.kwargs.get('pk'))
        kwargs['templatecategories'] = TaskTemplate.objects.filter(enabled=True)
        # kwargs['actions'] = Action.objects.filter(enabled=True)
        return kwargs


class InvTabEvidencesView(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = 'invs/inv_detail_tab_evidences_home.html'
    permission_required = ('invs.view_inv', 'tasks.view_task')

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(InvTabEvidencesView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InvTabEvidencesView, self).get_context_data(**kwargs)
        kwargs['inv'] = Inv.objects.get(pk=self.kwargs.get('pk'))
        # kwargs['templatecategories'] = TaskTemplate.objects.filter(enabled=True)
        kwargs['actions'] = Action.objects.filter(enabled=True)
        return kwargs

# ################################3
# import os
# from bCIRT.settings import MEDIA_ROOT
# from django.core.files.storage import default_storage
#
# def file_upload(request):
#     save_path = os.path.join(MEDIA_ROOT, 'uploads', request.FILES['file'])
#     path = default_storage.save(save_path, request.FILES['file'])
#     return default_storage.path(path)


# def save_inv_form(request, form, template_name):
#     data = dict()
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             data['form_is_valid'] = True
#             invs = Inv.objects.all()
#             data['html_data_list'] = render_to_string('invs/inv_detail_tab_evidence_tablebody.html', {
#                 'object_list': invs
#             })
#         else:
#             data['form_is_valid'] = False
#     context = {'form': form}
#     data['html_form'] = render_to_string(template_name, context, request=request)
#     return JsonResponse(data)
#
# def invaj_create_view(request):
#     if request.method == 'POST':
#         form = InvForm(request.POST)
#     else:
#         form = InvForm()
#     return save_inv_form(request, form, 'invs/inv_form_create_ajax.html')


class InvCreateAjaxView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Inv
    form_class = InvForm
    permission_required = ('invs.add_inv',)
    # success_url = 'invs:inv_list'
    # template_name = 'invs/inv_form_create_ajax.html'
    # success_url = reverse_lazy('invs:inv_list')
    ajax_partial = 'invs/inv_form_create_ajax.html'
    # ajax_list = 'invs/inv_list.html'
    ajax_list = 'invs/inv_list_tablebody.html'
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
        super(InvCreateAjaxView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data()
        if request.is_ajax():
            html_form = render_to_string(self.ajax_partial, context, request)
            return JsonResponse({'html_form': html_form})
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # return super(InvCreateAjaxView, self).get_context_data(**kwargs)
        context = super(InvCreateAjaxView, self).get_context_data(**kwargs)
        invs = Inv.objects.all()
        context['object_list'] = invs
        return context

    def form_valid(self, form):
        data = dict()
        context = self.get_context_data()

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.modified_by = self.request.user.get_username()
            self.object.created_by = self.request.user.get_username()
            self.object.save()
            # form.save()
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
        elif not self.request.user.has_perm('invs.add_inv'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('invs:inv_list')
        else:
            pass
        # Checks pass, let http method handlers process the request
        return super(InvCreateAjaxView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(InvCreateAjaxView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        # kwargs['inv_pk'] = self.kwargs.get('inv_pk')
        kwargs['user'] = self.request.user
        return kwargs


# https://www.abidibo.net/blog/2014/05/26/how-implement-modal-popup-django-forms-bootstrap/
# https://dkoug.com/django/django-ajax-class-based-views/
# https://chriskief.com/2013/10/29/advanced-django-class-based-views-modelforms-and-ajax-example-tutorial/
