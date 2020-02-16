# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : assets/models.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Models file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
# from django.shortcuts import render
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from invs.models import Inv
from tasks.models import EvidenceAttr, Evidence
# HTML renderer
import misaka
# Get the user so we can use this
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.
class Host(models.Model):
    objects = models.Manager()
    name = models.CharField(blank=False, null=False, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=True, default='', blank=True)
    # ip = models.GenericIPAddressField(blank=True, null=True, default='')

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(Host, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "assets:host_detail",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        # if self.ip == '' and self.name == '':
        #     raise ValidationError(_('You must enter an IP address or a Hostname.'))
        pass

    class Meta:
        ordering = ["id"]


# To store related hostnames
class Hostname(models.Model):
    objects = models.Manager()
    name = models.CharField(blank=True, default='', max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=True, default='', blank=True)
    hosts = models.ForeignKey(Host, blank=True, related_name="hostname_hosts", default=None, on_delete=models.SET_NULL,
                              null=True)

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.name)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(Hostname, self).save(*args, **kwargs)


# To store related ips
class Ipaddress(models.Model):
    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    ip = models.GenericIPAddressField(blank=True, null=True, default='')
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=True, default='', blank=True)
    hosts = models.ForeignKey(Host, blank=True, related_name="ipaddress_hosts", default=None,
                              on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.ip)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(Ipaddress, self).save(*args, **kwargs)


# Create your models here.
class Profile(models.Model):
    objects = models.Manager()
    username = models.CharField(blank=True, null=True, default='', max_length=50)
    userid = models.CharField(blank=True, null=True, default='', max_length=30)
    email = models.EmailField(blank=True, null=True, max_length=50)
    host = models.CharField(blank=True, null=True, default='', max_length=30)
    ip = models.GenericIPAddressField(blank=True, null=True, default='')
    location = models.CharField(blank=True, null=True, default='', max_length=30)
    department = models.CharField(blank=True, null=True, default='', max_length=30)
    location_contact = models.CharField(blank=True, null=True, default='', max_length=30)
    inv = models.ForeignKey(Inv, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="profile_inv")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20, default="unknown")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=20, default="unknown")
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "assets:prof_detail",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            })

    def clean(self):
        # Don't allow empty record.
        if self.username is None and \
                self.userid is None and \
                self.email is None and \
                self.host is None and \
                self.ip == "":
            raise ValidationError(_('You must fill in one of the fields: Username, UserID, Email, Host, IP'))

    class Meta:
        ordering = ["id"]


def new_profile(pinv, pusername=None, puserid=None, pemail=None, phost=None, pip=None, plocation=None,
                pdepartment=None, plocation_contact=None, pcreated_by=None, pmodified_by=None, pdescription=None):
    newprofile = Profile.objects.update_or_create(
        inv=pinv,
        username=pusername,
        userid=puserid,
        email=pemail,
        host=phost,
        ip=pip,
        location=plocation,
        department=pdepartment,
        location_contact=plocation_contact,
        created_by=pcreated_by,
        modified_by=pmodified_by,
        description=pdescription,
    )
    return newprofile


@transaction.atomic
def new_create_profile_from_evattrs(pinv_pk, pevattr_pk, pev_pk, pusername):
    # Creating a new profile based on the attribute calling this function
    # if the pev_pk = 0, it will add one attribute specified
    # if the pev_pk has a value, it adds all attributes under the evidence
    invpk = pinv_pk
    invobj = Inv.objects.get(pk=invpk)
    evattrpk = pevattr_pk
    evattr_obj = None
    if evattrpk:
        evattr_obj = EvidenceAttr.objects.get(pk=evattrpk)
    evpk = pev_pk
    attrpklist = list()
    if evpk == 0:
        attrpklist.append(evattr_obj)
    else:
        from django.db.models import Q
        attributes = EvidenceAttr.objects.filter(ev__pk=evpk)\
            .filter(Q(evattrformat__name='Email')
                    | Q(evattrformat__name="UserName")
                    | Q(evattrformat__name="UserID")
                    | Q(evattrformat__name="HostName")
                    | Q(evattrformat__name="IPv4"))
        if attributes:
            for attritem in attributes:
                attrpklist.append(attritem)
    for evattrobj in attrpklist:
        # find attributes and run the commands on them
        # if ev_pk is not 0, then we need to run it on all evidence attributes
        # evattrobj = EvidenceAttr.objects.get(pk=evattrpk)
        evattrtype = evattrobj.evattrformat.name
        ausername = None
        auserid = None
        aemail = None
        ahostname = None
        aip = None
        if evattrtype == "UserName":
            ausername = evattrobj.evattrvalue
        elif evattrtype == "UserID":
            auserid = evattrobj.evattrvalue
        elif evattrtype == "Email":
            aemail = evattrobj.evattrvalue
        elif evattrtype == "HostName":
            ahostname = evattrobj.evattrvalue
        elif evattrtype == "IPv4" or evattrtype == "IPv6":
            aip = evattrobj.evattrvalue
        else:
            pass

        # evattrvalue = evattrobj.evattrvalue
        new_profile(
            pinv=invobj,
            pusername=ausername,
            puserid=auserid,
            pemail=aemail,
            phost=ahostname,
            pip=aip,
            plocation=None,
            pdepartment=None,
            plocation_contact=None,
            pcreated_by=pusername,
            pmodified_by=pusername,
            pdescription="",
        )
    return True


@transaction.atomic
def new_create_profile_from_evattrs_all(pev):
    if pev is not None and pev != "0" and pev != 0:
        ev_obj = Evidence.objects.filter(pk=pev)\
            .select_related('inv__pk') \
            .select_related('user__username') \
            .values('inv__pk', 'user__username')[0]
        pinv_pk = ev_obj['inv__pk']
        pusername = ev_obj['user__username']
        new_create_profile_from_evattrs(pinv_pk=pinv_pk, pevattr_pk=None, pev_pk=pev, pusername=pusername)
    return True
