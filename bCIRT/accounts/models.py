# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : accounts/models.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Models file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
import logging
# from django.utils.timezone import now as timezone_now


# from django.db import models

# Create your models here.
class UserAudit(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    username = models.CharField(max_length=256, default=None, null=True, blank=True)
    eventtype = models.CharField(max_length=20, default="na", null=False, blank=False)
    session_id = models.CharField(max_length=100, default=None, null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    host = models.CharField(default=None, max_length=64, null=True, blank=True)
    action = models.CharField(max_length=64)
    event_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{0} - {1} - {2} - {3} - {4} - {5}'.format(self.event_time, self.eventtype, self.action, self.username,
                                                          self.ip, self.host)

    def __str__(self):
        return '{0} - {1} - {2} - {3} - {4} - {5}'.format(self.event_time, self.eventtype, self.action, self.username,
                                                          self.ip, self.host)

# for logging - define "error" named logging handler and logger in settings.py
error_log = logging.getLogger('error')


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    try:
        ip = request.META.get('REMOTE_ADDR')
        UserAudit.objects.create(eventtype='account_login',
                                 action='success',
                                 ip=ip,
                                 host=request.META['HTTP_HOST'],
                                 user=user,
                                 username=user.username,
                                 session_id=request.session.session_key
                                 )
    except Exception:
        # log the error
        error_log.error("log_user_logged_in request: %s, error: %s" % (request, Exception))


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    try:
        ip = request.META.get('REMOTE_ADDR')
        UserAudit.objects.create(eventtype='account_logout',
                                 action='success',
                                 ip=ip,
                                 host=request.META['HTTP_HOST'],
                                 user=user,
                                 username=user.username,
                                 session_id=request.session.session_key
                                 )
    except Exception:
        # log the error
        error_log.error("log_user_logged_out request: %s, error: %s" % (request, Exception))

    # try:
    #     login_logout_logs = UserAudit.objects.filter(session_key=request.COOKIES["sessionid"] , user=user.id)
    #     if not login_logout_logs:
    #         login_logout_log = UserAudit(session_key=request.COOKIES["sessionid"],
    #                                      user=user)
    #         login_logout_log.save()
    # except Exception:
        # log the error
        # error_log.error("log_user_logged_out request: %s, error: %s" % (request, Exception))

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    UserAudit.objects.create(eventtype='account_login',
                             action='fail',
                             username=credentials.get('username', None)
                             )