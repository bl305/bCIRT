# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : invs/management/comands/dbimport.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : dbimport file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
from django.core.management.base import BaseCommand, CommandError
import tablib
import os
from django.contrib.auth import get_user_model
User = get_user_model()


class Command(BaseCommand):
    help = 'Imports the database from backup'
    p_dir = None
    p_format = None

    def add_arguments(self, parser):
        # parser.add_argument('-a', '--all', action='store_true', help='Run all')
        parser.add_argument('-d', '--dir', type=str, help='Import from this directory')
        parser.add_argument('-f', '--format', type=str, help='Import from this format: "json"')

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        pass

    def handle(self, *args, **options):
        # def handle(self, *args, **kwargs):
        self.p_dir = str(options['dir'])
        self.p_format = str(options['format'])
        # self.p_dir = str(p_dir)
        if self.p_dir is not None and self.p_format == 'json':
            self.import_evidenceformat(self.p_format)
            self.import_evidenceattrformat(self.p_format)
            self.import_evidence(self.p_format)
            self.import_evidenceattr(self.p_format)

            self.import_host(self.p_format)
            self.import_hostname(self.p_format)
            self.import_ipaddress(self.p_format)
            self.import_profile(self.p_format)

            self.import_invseverity(self.p_format)
            self.import_invstatus(self.p_format)
            self.import_invcategory(self.p_format)
            self.import_invphase(self.p_format)
            self.import_invpriority(self.p_format)
            self.import_invattackvector(self.p_format)
            self.import_inv(self.p_format)

            self.import_taskstatus(self.p_format)
            self.import_taskcategory(self.p_format)
            self.import_taskpriority(self.p_format)
            self.import_tasktype(self.p_format)
            self.import_task(self.p_format)
            self.import_tasktemplate(self.p_format)
            self.import_playbook(self.p_format)
            self.import_playbooktemplate(self.p_format)
            self.import_playbooktemplateitem(self.p_format)

            self.import_taskvarcategory(self.p_format)
            self.import_taskvartype(self.p_format)
            self.import_taskvar(self.p_format)

            self.import_actscriptos(self.p_format)
            self.import_actscriptcategory(self.p_format)
            self.import_actscripttype(self.p_format)
            self.import_actscriptoutput(self.p_format)
            self.import_actoutputtarget(self.p_format)
            self.import_acttype(self.p_format)
            self.import_actionqstatus(self.p_format)
            self.import_actionq(self.p_format)
            self.import_action(self.p_format)

            self.import_updatepackage(self.p_format)

            print("Database import from " + self.p_dir + " finished.")
        else:
            print(r"""
usage: manage.py dbimport [-h] [-d IMPORTDIR] [-f json] [--version]
        [-v {0,1,2,3}] [--settings SETTINGS]
        [--pythonpath PYTHONPATH] [--traceback] [--no-color]
            """)
        pass

    def import_evidenceformat(self, p_format):
        tablename = "EvidenceFormat"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import EvidenceFormatResource
                aresource = EvidenceFormatResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_evidenceattrformat(self, p_format):
        tablename = "EvidenceAttrFormat"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import EvidenceAttrFormatResource
                aresource = EvidenceAttrFormatResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_evidence(self, p_format):
        tablename = "Evidence"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import EvidenceResource
                aresource = EvidenceResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_evidenceattr(self, p_format):
        tablename = "EvidenceAttr"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import EvidenceAttrResource
                aresource = EvidenceAttrResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_host(self, p_format):
        tablename = "Host"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from assets.resources import HostResource
                aresource = HostResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_hostname(self, p_format):
        tablename = "HostName"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from assets.resources import HostNameResource
                aresource = HostNameResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_ipaddress(self, p_format):
        tablename = "IpAddress"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from assets.resources import IpAddressResource
                aresource = IpAddressResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_profile(self, p_format):
        tablename = "Profile"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from assets.resources import ProfileResource
                aresource = ProfileResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_invstatus(self, p_format):
        tablename = "InvStatus"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from invs.resources import InvStatusResource
                aresource = InvStatusResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_invseverity(self, p_format):
        tablename = "InvSeverity"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from invs.resources import InvSeverityResource
                aresource = InvSeverityResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_invpriority(self, p_format):
        tablename = "InvPriority"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from invs.resources import InvPriorityResource
                aresource = InvPriorityResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_invphase(self, p_format):
        tablename = "InvPhase"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from invs.resources import InvPhaseResource
                aresource = InvPhaseResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_invcategory(self, p_format):
        tablename = "InvCategory"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from invs.resources import InvCategoryResource
                aresource = InvCategoryResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_invattackvector(self, p_format):
        tablename = "InvAttackVector"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from invs.resources import InvAttackvectorResource
                aresource = InvAttackvectorResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_inv(self, p_format):
        tablename = "Inv"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from invs.resources import InvResource
                aresource = InvResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_actscriptos(self, p_format):
        tablename = "ActScriptOs"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import ScriptOsResource
                aresource = ScriptOsResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_actscriptcategory(self, p_format):
        tablename = "ActScriptCategory"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import ScriptCategoryResource
                aresource = ScriptCategoryResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_actscripttype(self, p_format):
        tablename = "ActScriptType"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import ScriptTypeResource
                aresource = ScriptTypeResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_actoutputtarget(self, p_format):
        tablename = "ActOutputTarget"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import OutputTargetResource
                aresource = OutputTargetResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_actscriptoutput(self, p_format):
        tablename = "ActScriptOutput"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import ScriptOutputResource
                aresource = ScriptOutputResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_acttype(self, p_format):
        tablename = "ActType"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import TypeResource
                aresource = TypeResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_taskcategory(self, p_format):
        tablename = "TaskCategory"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import TaskCategoryResource
                aresource = TaskCategoryResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename + " imported successfully")
            except:
                raise CommandError(tablename + " table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_taskpriority(self, p_format):
        tablename = "TaskPriority"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import TaskPriorityResource
                aresource = TaskPriorityResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename+" imported successfully")
            except:
                raise CommandError(tablename+" table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_taskstatus(self, p_format):
        tablename = "TaskStatus"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import TaskStatusResource
                aresource = TaskStatusResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename+" imported successfully")
            except:
                raise CommandError(tablename+" table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_tasktype(self, p_format):
        tablename = "TaskType"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import TaskTypeResource
                aresource = TaskTypeResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename+" imported successfully")
            except:
                raise CommandError(tablename+" table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_task(self, p_format):
        tablename = "Task"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import TaskResource
                aresource = TaskResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename+" imported successfully")
            except:
                raise CommandError(tablename+" table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_tasktemplate(self, p_format):
        tablename = "TaskTemplate"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import TaskTemplateResource
                aresource = TaskTemplateResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename+" imported successfully")
            except:
                raise CommandError(tablename+" table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_taskvar(self, p_format):
        tablename = "TaskVar"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import TaskVarResource
                aresource = TaskVarResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename+" imported successfully")
            except:
                raise CommandError(tablename+" table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_playbook(self, p_format):
        tablename = "Playbook"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import PlaybookResource
                aresource = PlaybookResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename+" imported successfully")
            except:
                raise CommandError(tablename+" table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_playbooktemplate(self, p_format):
        tablename = "PlaybookTemplate"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import PlaybookTemplateResource
                aresource = PlaybookTemplateResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename+" imported successfully")
            except:
                raise CommandError(tablename+" table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_playbooktemplateitem(self, p_format):
        tablename = "PlaybookTemplateItem"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import PlaybookTemplateItemResource
                aresource = PlaybookTemplateItemResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename+" imported successfully")
            except:
                raise CommandError(tablename+" table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_taskvarcategory(self, p_format):
        tablename = "TaskVarCategory"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import TaskVarCategoryResource
                aresource = TaskVarCategoryResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename+" imported successfully")
            except:
                raise CommandError(tablename+" table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_taskvartype(self, p_format):
        tablename = "TaskVarType"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import TaskVarTypeResource
                aresource = TaskVarTypeResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename+" imported successfully")
            except:
                raise CommandError(tablename+" table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_action(self, p_format):
        tablename = "Action"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import ActionResource
                aresource = ActionResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename+" imported successfully")
            except:
                raise CommandError(tablename+" table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_actionqstatus(self, p_format):
        tablename = "ActionQStatus"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import ActionQStatusResource
                aresource = ActionQStatusResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename+" imported successfully")
            except:
                raise CommandError(tablename+" table could not be imported!")
        else:
            print(fname+" is not readable!")

    def import_actionq(self, p_format):
        tablename = "ActionQ"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import ActionQResource
                aresource = ActionQResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename+" imported successfully")
            except:
                raise CommandError(tablename+" table could not be imported!")
        else:
            print(fname+" is not readable!")


    def import_updatepackage(self, p_format):
        tablename = "UpdatePackage"
        print("Importing "+tablename)
        fname = os.path.join(self.p_dir, tablename+'.'+p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            try:
                from tasks.resources import UpdatePackageResource
                aresource = UpdatePackageResource()
                dataset = tablib.Dataset().load(open(fname).read())
                result = aresource.import_data(dataset, dry_run=True)
                if not result.has_errors():
                    aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                    print(tablename+" imported successfully")
            except:
                raise CommandError(tablename+" table could not be imported!")
        else:
            print(fname+" is not readable!")
