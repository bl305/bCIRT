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
# **********************************************************************;
from tasks.models import TaskTemplate, PlaybookTemplate, Action, ActionGroupMember
from tasks.models import new_playbook, new_evidence, task_close
# from tasks.models import Task, Playbook
import os
import shutil
from django.core.files import File
import tempfile
from zipfile import ZipFile
from bCIRT.settings import MEDIA_ROOT
from shutil import copyfile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# to manage manual uploads
# from os import path
# from bCIRT.custom_variables import MYMEDIA_ROOT
# from django.http import HttpResponseRedirect
# from django.shortcuts import render
##############

from .forms import InvForm, InvSuspiciousEmailForm
from .models import Inv, InvStatus, new_inv, InvCategory, InvAttackvector, InvPhase, InvSeverity, CurrencyType,\
    InvPriority
from django.shortcuts import redirect, reverse    # ,render, get_object_or_404
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
from wkhtmltopdf.views import PDFTemplateResponse
from django.contrib.auth import get_user_model
User = get_user_model()
logger = logging.getLogger('log_file_verbose')


# Create your views here.
class MyPDFView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    # context = {"title": "Task evidences"}  # data that has to be rendered to pdf templete
    model = Inv
    permission_required = ('invs.view_inv', 'tasks.view_evidence', 'tasks:view_task', 'tasks:view_playbook')
    context = {"title": "Investigation evidences"}

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(MyPDFView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.context['inv'] = self.get_object()
        self.context['user'] = self.request.user.get_username()

        html_template = get_template('invs/inv_detail_REPORT_v1.html')

        # rendered_html = html_template.render(self.context)
        #
        # css_path = custom_params.PROJECT_ROOT + '/static/bCIRT/bootstrap-3.3.7/css/bootstrap.min.css'
        # pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(css_path)])
        # # pdf_file = HTML(string=rendered_html).write_pdf()

        # http_response = HttpResponse(pdf_file, content_type='application/pdf')
        # http_response['Content-Disposition'] = 'filename="report_investigation.pdf"'
        response = PDFTemplateResponse(request=request,
                                       template=html_template,
                                       filename="investigation_report_" + str(self.get_object().pk) + ".pdf",
                                       context=self.context,
                                       show_content_in_browser=False,
                                       cmd_options={'margin-top': 10,
                                                    "zoom": 1,
                                                    "viewport-size": "1366 x 513",
                                                    'javascript-delay': 1000,
                                                    'footer-center': '[page]/[topage]',
                                                    "no-stop-slow-scripts": True},
                                       )
        return response


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


        inv_obj = Inv.objects.get(pk=self.kwargs.get('pk'))
        ev_obj = inv_obj.evidence_inv.all()
        evattr_set = set()
        for ev_obj_item in ev_obj:
            if ev_obj_item.evattr_evidence.all():
                for evattr_obj in ev_obj_item.evattr_evidence.all():
                    evattr_set.add(evattr_obj)
        kwargs['invevidence_evattr_evidence_all'] = evattr_set
        # actiongrmember_file = set()
        # actiongrmember_desc = set()
        # actiongrmember_attr = set()
        actiongroups_file = set()
        actiongroups_desc = set()
        actiongroups_attr = set()
        if ActionGroupMember.objects.all():
            for actgrpmember in ActionGroupMember.objects.all():
                # input is description scriptinput=1:
                if actgrpmember.actionid.enabled == True and actgrpmember.actionid.scriptinput.pk == 1:
                    # actiongrmember_desc.add(actgrpmember.actionid)
                    actiongroups_desc.add(actgrpmember.actiongroupid)
                # input is file scriptinput=2:
                elif actgrpmember.actionid.enabled == True and actgrpmember.actionid.scriptinput.pk == 2:
                    # actiongrmember_file.add(actgrpmember.actionid)
                    actiongroups_file.add(actgrpmember.actiongroupid)
                # input is attribute scriptinput=1:
                elif actgrpmember.actionid.enabled == True and actgrpmember.actionid.scriptinput.pk == 3:
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
        assigned_pk = InvStatus.objects.get(name='Assigned')
        Inv.objects.filter(pk=inv_pk).update(status=assigned_pk)
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
#             handle_uploaded_file_chunks(request.FILES['file'], '/tmp/xxx.txt')
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
                          pattackvector=InvAttackvector.objects.get(name="Phishing"),
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
        if (cfileext.lower() == 'eml') or (cfileext.lower() == 'msg'):
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
            evidence_obj.task=first_task
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
            with ZipFile(my_zip) as zip_file:
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
                                print("Error:%s" % (Exception))

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

                        evidence_obj = new_evidence(
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
#################################3
# import os
# from bCIRT.settings import MEDIA_ROOT
# from django.core.files.storage import default_storage
#
# def file_upload(request):
#     save_path = os.path.join(MEDIA_ROOT, 'uploads', request.FILES['file'])
#     path = default_storage.save(save_path, request.FILES['file'])
#     return default_storage.path(path)
