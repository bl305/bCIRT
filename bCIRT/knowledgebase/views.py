from django.shortcuts import render
from .models import KnowledgeBase, KnowledgeBaseFormat
from django.shortcuts import redirect, reverse # , get_object_or_404  # ,render,
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.views import generic
import logging
from bCIRT.settings import ALLOWED_HOSTS
from django.utils.http import is_safe_url
from bCIRT.custom_variables import LOGLEVEL, LOGSEPARATOR
from django.contrib.auth import get_user_model
from .forms import KnowledgeBaseForm
User = get_user_model()
logger = logging.getLogger('log_file_verbose')


# Create your views here.
class KnowledgeBaseListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = KnowledgeBase
    form_class = KnowledgeBaseForm
    permission_required = ('knowledgebase.view_knowledgebase',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(KnowledgeBaseListView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(KnowledgeBaseListView, self).get_context_data(**kwargs)


# @method_decorator(csrf_exempt, name='dispatch')
class KnowledgeBaseCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    #  fields = ("inv", "user", "description", "fileRef")
    model = KnowledgeBase
    form_class = KnowledgeBaseForm
    permission_required = ('knowledgebase.add_knowledgebase',)
    success_url = 'knowledgebase:kb_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(KnowledgeBaseCreateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(KnowledgeBaseCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        self.object.created_by = self.request.user.get_username()
        if self.request.FILES:
            self.object.fileName = self.request.FILES['fileRef'].name
        self.object.save()
        return super(KnowledgeBaseCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('knowledgebase.add_knowledgebase'):
            messages.error(self.request, "No permission to add a record !!!")
            return redirect('knowledgebase:kb_list')
        # Checks pass, let http method handlers process the request
        return super(KnowledgeBaseCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(KnowledgeBaseCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user.username
        return kwargs


class KnowledgeBaseDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = KnowledgeBase
    permission_required = ('knowledgebase.view_knowledgebase',)

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(KnowledgeBaseDetailView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(KnowledgeBaseDetailView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('knowledgebase.view_knowledgebase'):
            messages.error(self.request, "No permission to view a record !!!")
            return redirect('knowledgebase:kb_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(KnowledgeBaseDetailView, self).dispatch(request, *args, **kwargs)


# @method_decorator(csrf_exempt, name='dispatch')
class KnowledgeBaseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    login_url = '/'
    # redirect_field_name = 'knowledgebase/evidence_detail.html'
    form_class = KnowledgeBaseForm
    model = KnowledgeBase
    permission_required = ('knowledgebase.change_knowledgebase',)
    success_url = 'knowledgebase:kb_list'

    def __init__(self, *args, **kwargs):
        self.object = None
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(KnowledgeBaseUpdateView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(KnowledgeBaseUpdateView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('knowledgebase.change_knowledgebase'):
            messages.error(self.request, "No permission to change a record !!!")
            return redirect('knowledgebase:kb_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(KnowledgeBaseUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.modified_by = self.request.user.get_username()
        if self.request.FILES:
            self.object.fileName = self.request.FILES['fileRef'].name
        self.object.save()
        return super(KnowledgeBaseUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(KnowledgeBaseUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        # kwargs['kb_pk'] = self.kwargs.get('pk')
        return kwargs


class KnowledgeBaseRemoveView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = KnowledgeBase
#    success_url = reverse_lazy('knowledgebase:ev_list')
    permission_required = ('knowledgebase.delete_knowledgebase', 'knowledgebase.view_knowledgebase',)
    success_url = 'knowledgebase:kb_list'

    def __init__(self, *args, **kwargs):
        if LOGLEVEL == 1:
            pass
        elif LOGLEVEL == 2:
            pass
        elif LOGLEVEL == 3:
            logmsg = "na" + LOGSEPARATOR + "call" + LOGSEPARATOR + self.__class__.__name__
            logger.info(logmsg)
        super(KnowledgeBaseRemoveView, self).__init__(*args, **kwargs)

    def get_success_url(self):
        if 'next1' in self.request.GET:
            redirect_to = self.request.GET['next1']
            if not is_safe_url(url=redirect_to, allowed_hosts=ALLOWED_HOSTS):
                return reverse(self.success_url)
        else:
            return reverse(self.success_url)
        return redirect_to

    def get_context_data(self, **kwargs):
        return super(KnowledgeBaseRemoveView, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        elif not self.request.user.has_perm('knowledgebase.delete_knowledgebase'):
            messages.error(self.request, "No permission to delete a record !!!")
            return redirect('knowledgebase:kb_detail', pk=self.kwargs.get('pk'))
        # Checks pass, let http method handlers process the request
        return super(KnowledgeBaseRemoveView, self).dispatch(request, *args, **kwargs)