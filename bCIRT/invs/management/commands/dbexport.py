# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : invs/management/commands/dbexport.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : dbexport file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
# TBD:
# add settingsuser, settingssystem, settingscategory

from django.core.management.base import BaseCommand, CommandError
# from invs.models import InvStatus, InvPriority, InvAttackVector, InvCategory, InvPhase, InvSeverity
# from tasks.models import TaskVarType, TaskVarCategory, TaskType, TaskCategory, TaskStatus, TaskPriority
# from tasks.models import ScriptOs, ScriptType, ScriptCategory, Action, Type, ActionQStatus, OutputTarget, ScriptOutput
# from tasks.models import EvidenceFormat, EvidenceAttr, EvidenceAttrFormat
from os import path
from django.contrib.auth import get_user_model
User = get_user_model()


class Command(BaseCommand):
    help = 'Exports the database to backup'
    p_dir = None

    def add_arguments(self, parser):
        # parser.add_argument('-a', '--all', action='store_true', help='Run all')
        parser.add_argument('-a', '--all', action='store_true', help='Export the whole database')
        parser.add_argument('-i', '--table_name', type=str, help='Export the specified module tables')
        parser.add_argument('-f', '--format', type=str, help='Export in this format: "json/csv"')
        parser.add_argument('-d', '--dir', type=str, help='Export to this directory')

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        pass

    def handle(self, *args, **options):
        # def handle(self, *args, **kwargs):
        p_all = options['all']
        p_table = options['table_name']
        p_format = options['format']
        p_dir = options['dir']
        self.p_dir = str(p_dir)
        if p_all and p_dir is not None and p_format: # == "json":
            self.export_user(p_format)
            self.export_group(p_format)

            self.export_evidenceformat(p_format)
            self.export_evidenceattrformat(p_format)
            self.export_evreputation(p_format)
            self.export_evidence(p_format)
            self.export_evidenceattr(p_format)
            self.export_mitreattck_techniques(p_format)
            self.export_mitreattck_tactics(p_format)

            self.export_updatepackage(p_format)

            self.export_host(p_format)
            self.export_hostname(p_format)
            self.export_ipaddress(p_format)
            self.export_profile(p_format)

            self.export_invseverity(p_format)
            self.export_invstatus(p_format)
            self.export_invcategory(p_format)
            self.export_invphase(p_format)
            self.export_invpriority(p_format)
            self.export_invattackvector(p_format)
            self.export_currencytype(p_format)
            self.export_invreviewrules(p_format)
            self.export_inv(p_format)

            self.export_taskstatus(p_format)
            self.export_taskcategory(p_format)
            self.export_taskpriority(p_format)
            self.export_tasktype(p_format)
            self.export_task(p_format)
            self.export_tasktemplate(p_format)
            self.export_playbook(p_format)
            self.export_playbooktemplate(p_format)
            self.export_playbooktemplateitem(p_format)

            self.export_taskvarcategory(p_format)
            self.export_taskvartype(p_format)
            self.export_taskvar(p_format)

            self.export_actscriptos(p_format)
            self.export_actscriptcategory(p_format)
            self.export_actscripttype(p_format)
            self.export_actscriptoutput(p_format)
            self.export_actscriptinput(p_format)
            self.export_actoutputtarget(p_format)
            self.export_acttype(p_format)
            self.export_actionqstatus(p_format)
            self.export_actionq(p_format)
            self.export_actiongroup(p_format)
            self.export_actiongroupmember(p_format)
            self.export_action(p_format)

            self.export_connectionitem(p_format)
            self.export_connectionitemfield(p_format)

            self.export_useraudit(p_format)

            self.export_automation(p_format)

            print("Database export to " + p_dir + " finished.")
        elif p_table and p_dir is not None and p_format: # == "json":
            if p_table == "investigations":
                self.export_invseverity(p_format)
                self.export_invstatus(p_format)
                self.export_invcategory(p_format)
                self.export_invphase(p_format)
                self.export_invpriority(p_format)
                self.export_invattackvector(p_format)
                self.export_mitreattck_techniques(p_format)
                self.export_mitreattck_tactics(p_format)
                self.export_invreviewrules(p_format)
                self.export_currencytype(p_format)
                self.export_inv(p_format)
                print("Database export to " + p_dir + " finished.")
            elif p_table == "evidences":
                self.export_evidenceformat(p_format)
                self.export_evidenceattrformat(p_format)
                self.export_evreputation(p_format)
                self.export_evidence(p_format)
                self.export_evidenceattr(p_format)
                print("Database export to " + p_dir + " finished.")
            elif p_table == "hosts":
                self.export_host(p_format)
                self.export_hostname(p_format)
                self.export_ipaddress(p_format)
                self.export_profile(p_format)
                print("Database export to " + p_dir + " finished.")
            elif p_table == "tasks":
                self.export_taskstatus(p_format)
                self.export_taskcategory(p_format)
                self.export_taskpriority(p_format)
                self.export_tasktype(p_format)
                self.export_task(p_format)
                self.export_tasktemplate(p_format)
                self.export_playbook(p_format)
                self.export_playbooktemplate(p_format)
                self.export_playbooktemplateitem(p_format)
                print("Database export to " + p_dir + " finished.")
            elif p_table == "taskvars":
                self.export_taskvarcategory(p_format)
                self.export_taskvartype(p_format)
                self.export_taskvar(p_format)
                print("Database export to " + p_dir + " finished.")
            elif p_table == "actions":
                self.export_actscriptos(p_format)
                self.export_actscriptcategory(p_format)
                self.export_actscripttype(p_format)
                self.export_actscriptoutput(p_format)
                self.export_actscriptinput(p_format)
                self.export_actoutputtarget(p_format)
                self.export_acttype(p_format)
                self.export_actionqstatus(p_format)
                self.export_actionq(p_format)
                self.export_actiongroup(p_format)
                self.export_actiongroupmember(p_format)
                self.export_action(p_format)
                print("Database export to " + p_dir + " finished.")
            elif p_table == "configuration":
                self.export_updatepackage(p_format)
                print("Database export to " + p_dir + " finished.")
            elif p_table == "connection":
                self.export_connectionitem(p_format)
                self.export_connectionitemfield(p_format)
                print("Database export to " + p_dir + " finished.")
            elif p_table == "audit":
                self.export_useraudit(p_format)
                print("Database export to " + p_dir + " finished.")
            elif p_table == "automation":
                self.export_automation(p_format)
                print("Database export to " + p_dir + " finished.")
            elif p_table == "user":
                self.export_user(p_format)
                self.export_group(p_format)
                print("Database export to " + p_dir + " finished.")
            else:
                print("Wrong parameter! Options:\ninvestigations / tasks / taskvars / actions / evidences / "
                      "configuration / connection / audit / automation / user\n")
        else:
            print(r"""
usage: manage.py dbexport [-h] [-a]\[-i TABLE_NAME] [-f json/csv] [-d OUTDIR] [--version]
        [-v {0,1,2,3}] [--settings SETTINGS]
        [--pythonpath PYTHONPATH] [--traceback] [--no-color]
            """)
        pass

    def save_to_file(self, a_filename, a_content):
        destpath = path.join(self.p_dir, a_filename)
        try:
            with open(destpath, "w") as outfile:
                outfile.write(a_content)
            outfile.close()
        except IOError:
            print('Error occured while trying to write file: ' + destpath)

    def export_user(self, p_format):
        try:
            print("Exporting User")
            from users.resources import UserResource
            aresource = UserResource()
            dataset = aresource.export()
            tablename = 'User'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("User table could not be exported!")

    def export_group(self, p_format):
        try:
            print("Exporting Group")
            from users.resources import GroupResource
            aresource = GroupResource()
            dataset = aresource.export()
            tablename = 'Group'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("Group table could not be exported!")

    def export_evidenceformat(self, p_format):
        try:
            # self.stdout.write("Exporting EvidenceFormat")
            print("Exporting EvidenceFormat")
            from tasks.resources import EvidenceFormatResource
            aresource = EvidenceFormatResource()
            # queryset = EvidenceFormat.objects.filter(pk=1)
            # dataset = aresource.export(queryset)
            dataset = aresource.export()
            tablename = 'EvidenceFormat'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("EvidenceFormat table could not be exported!")

    def export_evidenceattrformat(self, p_format):
        try:
            print("Exporting EvidenceAttrFormat")
            from tasks.resources import EvidenceAttrFormatResource
            aresource = EvidenceAttrFormatResource()
            dataset = aresource.export()
            tablename = 'EvidenceAttrFormat'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("EvidenceAttrFormat table could not be exported!")

    def export_evreputation(self, p_format):
        try:
            print("Exporting EvReputation")
            from tasks.resources import EvReputationResource
            aresource = EvReputationResource()
            dataset = aresource.export()
            tablename = 'EvReputation'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("EvReputation table could not be exported!")

    def export_mitreattck_techniques(self, p_format):
        try:
            print("Exporting MitreAttck_Techniques")
            from tasks.resources import MitreAttck_TechniquesResource
            aresource = MitreAttck_TechniquesResource()
            dataset = aresource.export()
            tablename = 'MitreAttck_Techniques'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("MitreAttck_Techinques table could not be exported!")

    def export_mitreattck_tactics(self, p_format):
        try:
            print("Exporting MitreAttck_Tactics")
            from tasks.resources import MitreAttck_TacticsResource
            aresource = MitreAttck_TacticsResource()
            dataset = aresource.export()
            tablename = 'MitreAttck_Tactics'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("MitreAttck_Tactics table could not be exported!")

    def export_evidence(self, p_format):
        try:
            # self.stdout.write("Exporting EvidenceFormat")
            print("Exporting Evidence")
            from tasks.resources import EvidenceResource
            aresource = EvidenceResource()
            # queryset = EvidenceFormat.objects.filter(pk=1)
            # dataset = aresource.export(queryset)
            from tasks.models import Evidence
            queryset = Evidence.objects.all().order_by('parent').reverse()
            dataset = aresource.export(queryset)
            # dataset = aresource.export()
            tablename = 'Evidence'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("Evidence table could not be exported!")

    def export_evidenceattr(self, p_format):
        try:
            # self.stdout.write("Exporting EvidenceFormat")
            print("Exporting EvidenceAttr")
            from tasks.resources import EvidenceAttrResource
            aresource = EvidenceAttrResource()
            # queryset = EvidenceFormat.objects.filter(pk=1)
            # dataset = aresource.export(queryset)
            dataset = aresource.export()
            tablename = 'EvidenceAttr'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("EvidenceAttr table could not be exported!")

    def export_host(self, p_format):
        try:
            # self.stdout.write("Exporting EvidenceFormat")
            print("Exporting Host")
            from assets.resources import HostResource
            aresource = HostResource()
            # queryset = EvidenceFormat.objects.filter(pk=1)
            # dataset = aresource.export(queryset)
            dataset = aresource.export()
            tablename = 'Host'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("Host table could not be exported!")

    def export_hostname(self, p_format):
        try:
            # self.stdout.write("Exporting EvidenceFormat")
            print("Exporting Hostname")
            from assets.resources import HostnameResource
            aresource = HostnameResource()
            # queryset = EvidenceFormat.objects.filter(pk=1)
            # dataset = aresource.export(queryset)
            dataset = aresource.export()
            tablename = 'Hostname'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("Hostname table could not be exported!")

    def export_ipaddress(self, p_format):
        try:
            # self.stdout.write("Exporting EvidenceFormat")
            print("Exporting Ipaddress")
            from assets.resources import IpaddressResource
            aresource = IpaddressResource()
            # queryset = EvidenceFormat.objects.filter(pk=1)
            # dataset = aresource.export(queryset)
            dataset = aresource.export()
            tablename = 'Ipaddress'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("Ipaddress table could not be exported!")

    def export_profile(self, p_format):
        try:
            # self.stdout.write("Exporting EvidenceFormat")
            print("Exporting Profile")
            from assets.resources import ProfileResource
            aresource = ProfileResource()
            # queryset = EvidenceFormat.objects.filter(pk=1)
            # dataset = aresource.export(queryset)
            dataset = aresource.export()
            tablename = 'Profile'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("Profile table could not be exported!")

    def export_invstatus(self, p_format):
        try:
            print("Exporting InvStatus")
            from invs.resources import InvStatusResource
            aresource = InvStatusResource()
            dataset = aresource.export()
            tablename = 'InvStatus'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("InvStatus table could not be exported!")

    def export_invseverity(self, p_format):
        try:
            print("Exporting InvSeverity")
            from invs.resources import InvSeverityResource
            aresource = InvSeverityResource()
            dataset = aresource.export()
            tablename = 'InvSeverity'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("InvSeverity table could not be exported!")

    def export_invpriority(self, p_format):
        try:
            print("Exporting InvPriority")
            from invs.resources import InvPriorityResource
            aresource = InvPriorityResource()
            dataset = aresource.export()
            tablename = 'InvPriority'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("InvPriority table could not be exported!")

    def export_invphase(self, p_format):
        try:
            print("Exporting InvPhase")
            from invs.resources import InvPhaseResource
            aresource = InvPhaseResource()
            dataset = aresource.export()
            tablename = 'InvPhase'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("InvPhase table could not be exported!")

    def export_invcategory(self, p_format):
        try:
            print("Exporting InvCategory")
            from invs.resources import InvCategoryResource
            aresource = InvCategoryResource()
            dataset = aresource.export()
            tablename = 'InvCategory'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("InvCategory table could not be exported!")

    def export_invattackvector(self, p_format):
        try:
            print("Exporting InvAttackVector")
            from invs.resources import InvAttackVectorResource
            aresource = InvAttackVectorResource()
            dataset = aresource.export()
            tablename = 'InvAttackVector'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("InvAttackVector table could not be exported!")

    def export_invreviewrules(self, p_format):
        try:
            print("Exporting InvReviewRules")
            from invs.resources import InvReviewRulesResource
            aresource = InvReviewRulesResource()
            dataset = aresource.export()
            tablename = 'InvReviewRules'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("InvReviewRules table could not be exported!")

    def export_currencytype(self, p_format):
        try:
            print("Exporting CurrencyType")
            from invs.resources import CurrencyTypeResource
            aresource = CurrencyTypeResource()
            dataset = aresource.export()
            tablename = 'CurrencyType'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("CurrencyType table could not be exported!")

    def export_inv(self, p_format):
        try:
            print("Exporting Inv")
            from invs.resources import InvResource
            aresource = InvResource()
            # dataset = aresource.export()
            from invs.models import Inv
            queryset = Inv.objects.all().order_by('parent').reverse()
            dataset = aresource.export(queryset)

            tablename = 'Inv'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("Inv table could not be exported!")

    def export_actscriptos(self, p_format):
        try:
            print("Exporting ScriptOs")
            from tasks.resources import ScriptOsResource
            aresource = ScriptOsResource()
            dataset = aresource.export()
            tablename = 'ScriptOs'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("ScriptOs table could not be exported!")

    def export_actscriptcategory(self, p_format):
        try:
            print("Exporting ScriptCategory")
            from tasks.resources import ScriptCategoryResource
            aresource = ScriptCategoryResource()
            dataset = aresource.export()
            tablename = 'ScriptCategory'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("ScriptCategory table could not be exported!")

    def export_actscripttype(self, p_format):
        try:
            print("Exporting ScriptType")
            from tasks.resources import ScriptTypeResource
            aresource = ScriptTypeResource()
            dataset = aresource.export()
            tablename = 'ScriptType'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("ScriptType table could not be exported!")

    def export_actoutputtarget(self, p_format):
        try:
            print("Exporting OutputTarget")
            from tasks.resources import OutputTargetResource
            aresource = OutputTargetResource()
            dataset = aresource.export()
            tablename = 'OutputTarget'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("OutputTarget table could not be exported!")

    def export_actscriptoutput(self, p_format):
        try:
            print("Exporting ScriptOutput")
            from tasks.resources import ScriptOutputResource
            aresource = ScriptOutputResource()
            dataset = aresource.export()
            tablename = 'ScriptOutput'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("ScriptOutput table could not be exported!")


    def export_actscriptinput(self, p_format):
        try:
            print("Exporting ScriptInput")
            from tasks.resources import ScriptInputResource
            aresource = ScriptInputResource()
            dataset = aresource.export()
            tablename = 'ScriptInput'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("ScriptInput table could not be exported!")


    def export_acttype(self, p_format):
        try:
            print("Exporting Type")
            from tasks.resources import TypeResource
            aresource = TypeResource()
            dataset = aresource.export()
            tablename = 'Type'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("Type table could not be exported!")

    def export_taskcategory(self, p_format):
        try:
            print("Exporting TaskCategory")
            from tasks.resources import TaskCategoryResource
            aresource = TaskCategoryResource()
            dataset = aresource.export()
            tablename = 'TaskCategory'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("TaskCategory table could not be exported!")

    def export_taskpriority(self, p_format):
        try:
            print("Exporting TaskPriority")
            from tasks.resources import TaskPriorityResource
            aresource = TaskPriorityResource()
            dataset = aresource.export()
            tablename = 'TaskPriority'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("TaskPriority table could not be exported!")

    def export_taskstatus(self, p_format):
        try:
            print("Exporting TaskStatus")
            from tasks.resources import TaskStatusResource
            aresource = TaskStatusResource()
            dataset = aresource.export()
            tablename = 'TaskStatus'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("TaskStatus table could not be exported!")

    def export_tasktype(self, p_format):
        try:
            print("Exporting TaskType")
            from tasks.resources import TaskTypeResource
            aresource = TaskTypeResource()
            dataset = aresource.export()
            tablename = 'TaskType'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("TaskType table could not be exported!")

    def export_task(self, p_format):
        try:
            print("Exporting Task")
            from tasks.resources import TaskResource
            aresource = TaskResource()
            from tasks.models import Task
            queryset = Task.objects.all().order_by('parent').reverse()
            dataset = aresource.export(queryset)
            # dataset = aresource.export()

            tablename = 'Task'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("Task table could not be exported!")

    def export_tasktemplate(self, p_format):
        try:
            print("Exporting TaskTemplate")
            from tasks.resources import TaskTemplateResource
            aresource = TaskTemplateResource()
            from tasks.models import TaskTemplate
            queryset = TaskTemplate.objects.all().order_by('actiontarget').reverse()
            dataset = aresource.export(queryset)
            # dataset = aresource.export()

            tablename = 'TaskTemplate'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("TaskTemplate table could not be exported!")

    def export_taskvar(self, p_format):
        try:
            print("Exporting TaskVar")
            from tasks.resources import TaskVarResource
            aresource = TaskVarResource()
            dataset = aresource.export()
            tablename = 'TaskVar'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("TaskVar table could not be exported!")

    def export_playbook(self, p_format):
        try:
            print("Exporting Playbook")
            from tasks.resources import PlaybookResource
            aresource = PlaybookResource()
            dataset = aresource.export()
            tablename = 'Playbook'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("Playbook table could not be exported!")

    def export_playbooktemplate(self, p_format):
        try:
            print("Exporting PlaybookTemplate")
            from tasks.resources import PlaybookTemplateResource
            aresource = PlaybookTemplateResource()
            dataset = aresource.export()
            tablename = 'PlaybookTemplate'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("PlaybookTemplate table could not be exported!")

    def export_playbooktemplateitem(self, p_format):
        try:
            print("Exporting PlaybookTemplateItem")
            from tasks.resources import PlaybookTemplateItemResource
            aresource = PlaybookTemplateItemResource()
            from tasks.models import PlaybookTemplateItem
            queryset = PlaybookTemplateItem.objects.all().order_by('prevtask','nexttask')
            dataset = aresource.export(queryset)
            # dataset = aresource.export()
            tablename = 'PlaybookTemplateItem'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("PlaybookTemplateItem table could not be exported!")

    def export_taskvarcategory(self, p_format):
        try:
            print("Exporting TaskVarCategory")
            from tasks.resources import TaskVarCategoryResource
            aresource = TaskVarCategoryResource()
            dataset = aresource.export()
            tablename = 'TaskVarCategory'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("TaskVarCategory table could not be exported!")

    def export_taskvartype(self, p_format):
        try:
            print("Exporting TaskVarType")
            from tasks.resources import TaskVarTypeResource
            aresource = TaskVarTypeResource()
            dataset = aresource.export()
            tablename = 'TaskVarType'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("TaskVarType table could not be exported!")

    def export_action(self, p_format):
        try:
            print("Exporting Action")
            from tasks.resources import ActionResource
            aresource = ActionResource()
            dataset = aresource.export()
            tablename = 'Action'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("Action table could not be exported!")

    def export_actionqstatus(self, p_format):
        try:
            print("Exporting ActionQStatus")
            from tasks.resources import ActionQStatusResource
            aresource = ActionQStatusResource()
            dataset = aresource.export()
            tablename = 'ActionQStatus'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("ActionQStatus table could not be exported!")

    def export_actiongroup(self, p_format):
        try:
            print("Exporting ActionGroup")
            from tasks.resources import ActionGroupResource
            aresource = ActionGroupResource()
            dataset = aresource.export()
            tablename = 'ActionGroup'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("ActionGroup table could not be exported!")

    def export_actiongroupmember(self, p_format):
        try:
            print("Exporting ActionGroupMember")
            from tasks.resources import ActionGroupMemberResource
            aresource = ActionGroupMemberResource()
            dataset = aresource.export()
            tablename = 'ActionGroupMember'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("ActionGroupMember table could not be exported!")

    def export_actionq(self, p_format):
        try:
            print("Exporting ActionQ")
            from tasks.resources import ActionQResource
            aresource = ActionQResource()
            dataset = aresource.export()
            tablename = 'ActionQ'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("ActionQ table could not be exported!")

    def export_updatepackage(self, p_format):
        try:
            print("Exporting UpdatePackage")
            from configuration.resources import UpdatePackageResource
            aresource = UpdatePackageResource()
            dataset = aresource.export()
            tablename = 'UpdatePackage'
            if p_format == "json":
                self.save_to_file(a_filename=tablename+'.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename+'.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("UpdatePackage table could not be exported!")

    def export_connectionitem(self, p_format):
        try:
            print("Exporting ConnectionItem")
            from configuration.resources import ConnectionItemResource
            aresource = ConnectionItemResource()
            dataset = aresource.export()
            tablename = 'ConnectionItem'
            if p_format == "json":
                self.save_to_file(a_filename=tablename + '.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename + '.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("ConnectionItem table could not be exported!")

    def export_connectionitemfield(self, p_format):
        try:
            print("Exporting ConnectionItemField")
            from configuration.resources import ConnectionItemFieldResource
            aresource = ConnectionItemFieldResource()
            dataset = aresource.export()
            tablename = 'ConnectionItemField'
            if p_format == "json":
                self.save_to_file(a_filename=tablename + '.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename + '.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("ConnectionItemField table could not be exported!")

    def export_useraudit(self, p_format):
        try:
            print("Exporting UserAudit")
            from accounts.resources import UserAuditResource
            aresource = UserAuditResource()
            dataset = aresource.export()
            tablename = 'UserAudit'
            if p_format == "json":
                self.save_to_file(a_filename=tablename + '.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename + '.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("UserAudit table could not be exported!")

    def export_automation(self, p_format):
        try:
            print("Exporting Automation")
            from tasks.resources import AutomationResource
            aresource = AutomationResource()
            dataset = aresource.export()
            tablename = 'Automation'
            if p_format == "json":
                self.save_to_file(a_filename=tablename + '.json',
                                  a_content=dataset.json)
            elif p_format == "csv":
                self.save_to_file(a_filename=tablename + '.csv',
                                  a_content=dataset.csv)
        except Exception:
            raise CommandError("Automation table could not be exported!")

    # def export_XXX(self, p_format):
    #     try:
    #         print("Exporting XXX")
    #         from configuration.resources import XXXResource
    #         aresource = XXXResource()
    #         dataset = aresource.export()
    #         tablename = 'XXX'
    #         if p_format == "json":
    #             self.save_to_file(a_filename=tablename + '.json',
    #                               a_content=dataset.json)
    #         elif p_format == "csv":
    #             self.save_to_file(a_filename=tablename + '.csv',
    #                               a_content=dataset.csv)
    #     except Exception:
    #         raise CommandError("XXX table could not be exported!")
