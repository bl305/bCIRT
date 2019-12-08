# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : configuration/signals.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Signals file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from django.dispatch import receiver
from django.db.models.signals import post_delete
from .models import UpdatePackage


# By adding 'UpdatePackage' as 'sender' argument we only receive signals from that model
@receiver(post_delete, sender=UpdatePackage)
def on_delete(sender, **kwargs):
    instance = kwargs['instance']
    # ref is the name of the field file of the UpdatePackage model
    # replace with name of your file field
    instance.fileRef.delete(save=False)
