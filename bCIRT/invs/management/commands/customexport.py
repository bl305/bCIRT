# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : invs/management/commands/customexport.py
# Author            : Balazs Lendvay
# Date created      : 2019.12.27
# Purpose           : dbexport file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.12.27  Lendvay     1      Initial file
# **********************************************************************;

from django.core.management.base import BaseCommand, CommandError
from base64 import b64encode
from importlib import import_module
# from invs.models import InvStatus, InvPriority, InvAttackVector, InvCategory, InvPhase, InvSeverity
# from tasks.models import TaskVarType, TaskVarCategory, TaskType, TaskCategory, TaskStatus, TaskPriority
# from tasks.models import ScriptOs, ScriptType, ScriptCategory, Action, Type, ActionQStatus, OutputTarget, ScriptOutput
# from tasks.models import EvidenceFormat, EvidenceAttr, EvidenceAttrFormat
from os import path
from django.contrib.auth import get_user_model
User = get_user_model()

users_models_package = 'django.contrib.auth.models'
users_models_class_name = ['User', 'Group']

evidences_models_package = 'tasks.models'
evidences_models_class_name = ['EvidenceFormat','EvidenceAttrFormat','EvReputation',
                           'MitreAttck_Techniques','MitreAttck_Tactics','Evidence','EvidenceAttr']

configurations_models_package = 'configuration.models'
configurations_models_class_name = ['UpdatePackage']

assets_models_package = 'assets.models'
assets_models_class_name = ['Host','Hostname','Ipaddress','Profile']

invs_models_package = 'invs.models'
invs_models_class_name = ['InvSeverity','InvStatus','InvCategory','InvPhase','InvPriority',
                          'InvAttackVector','CurrencyType','InvReviewRules','Inv']

tasks_models_package = 'tasks.models'
tasks_models_class_name = ['TaskStatus','TaskCategory','TaskPriority','TaskType','Task','TaskTemplate',
                           'Playbook','PlaybookTemplate','PlaybookTemplateItem',
                           'TaskVarCategory','TaskVarType','TaskVar']

actions_models_package = 'tasks.models'
actions_models_class_name = ['ScriptOs','ScriptCategory','ScriptType','ScriptOutput','OutputTarget',
                             'Type','ActionQStatus','ActionQ','ActionGroup','ActionGroupMember','Action']

connections_models_package = 'configuration.models'
connections_models_class_name = ['ConnectionItem','ConnectionItemField']

automations_models_package = 'tasks.models'
automations_models_class_name = ['Automation']

audit_models_package = 'accounts.models'
audit_models_class_name = ['UserAudit']

class Command(BaseCommand):
    help = 'Exports the database to backup in a custom way'
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
            for class_name in users_models_class_name:
                self.export_modelcontents(p_format, users_models_package, class_name)

            for class_name in evidences_models_class_name:
                self.export_modelcontents(p_format, evidences_models_package, class_name)

            for class_name in configurations_models_class_name:
                self.export_modelcontents(p_format, configurations_models_package, class_name)

            for class_name in assets_models_class_name:
                self.export_modelcontents(p_format, assets_models_package, class_name)

            for class_name in invs_models_class_name:
                self.export_modelcontents(p_format, invs_models_package, class_name)

            for class_name in tasks_models_class_name:
                self.export_modelcontents(p_format, tasks_models_package, class_name)

            for class_name in actions_models_class_name:
                self.export_modelcontents(p_format, actions_models_package, class_name)

            for class_name in connections_models_class_name:
                self.export_modelcontents(p_format, connections_models_package, class_name)

            for class_name in automations_models_class_name:
                self.export_modelcontents(p_format, automations_models_package, class_name)

            for class_name in audit_models_class_name:
                self.export_modelcontents(p_format, audit_models_package, class_name)

            print("[+] Database export to " + p_dir + " finished.")
        elif p_table and p_dir is not None and p_format: # == "json":
            if p_table == "investigations":
                # self.export_invseverity(p_format)
                # self.export_invstatus(p_format)
                # self.export_invcategory(p_format)
                # self.export_invphase(p_format)
                # self.export_invpriority(p_format)
                # self.export_invattackvector(p_format)
                # self.export_mitreattck_techniques(p_format)
                # self.export_mitreattck_tactics(p_format)
                # self.export_invreviewrules(p_format)
                # self.export_currencytype(p_format)
                # self.export_inv(p_format)
                print("[+] Database export to " + p_dir + " finished.")
            elif p_table == "evidences":
                # self.export_evidenceformat(p_format)
                # self.export_evidenceattrformat(p_format)
                # self.export_evreputation(p_format)
                # self.export_evidence(p_format)
                # self.export_evidenceattr(p_format)
                print("[+] Database export to " + p_dir + " finished.")
            elif p_table == "hosts":
                # self.export_host(p_format)
                # self.export_hostname(p_format)
                # self.export_ipaddress(p_format)
                # self.export_profile(p_format)
                print("[+] Database export to " + p_dir + " finished.")
            elif p_table == "tasks":
                # self.export_taskstatus(p_format)
                # self.export_taskcategory(p_format)
                # self.export_taskpriority(p_format)
                # self.export_tasktype(p_format)
                # self.export_task(p_format)
                # self.export_tasktemplate(p_format)
                # self.export_playbook(p_format)
                # self.export_playbooktemplate(p_format)
                # self.export_playbooktemplateitem(p_format)
                print("[+] Database export to " + p_dir + " finished.")
            elif p_table == "taskvars":
                # self.export_taskvarcategory(p_format)
                # self.export_taskvartype(p_format)
                # self.export_taskvar(p_format)
                print("[+] Database export to " + p_dir + " finished.")
            elif p_table == "actions":
                # self.export_actscriptos(p_format)
                # self.export_actscriptcategory(p_format)
                # self.export_actscripttype(p_format)
                # self.export_actscriptoutput(p_format)
                # self.export_actoutputtarget(p_format)
                # self.export_acttype(p_format)
                # self.export_actionqstatus(p_format)
                # self.export_actionq(p_format)
                # self.export_actiongroup(p_format)
                # self.export_actiongroupmember(p_format)
                # self.export_action(p_format)
                print("[+] Database export to " + p_dir + " finished.")
            elif p_table == "configuration":
                # self.export_updatepackage(p_format)
                print("[+] Database export to " + p_dir + " finished.")
            elif p_table == "connection":
                # self.export_connectionitem(p_format)
                # self.export_connectionitemfield(p_format)
                print("[+] Database export to " + p_dir + " finished.")
            elif p_table == "audit":
                # self.export_useraudit(p_format)
                print("[+] Database export to " + p_dir + " finished.")
            elif p_table == "automation":
                # self.export_automation(p_format)
                print("[+] Database export to " + p_dir + " finished.")
            elif p_table == "user":
                # self.export_user(p_format)
                # self.export_group(p_format)
                print("[+] Database export to " + p_dir + " finished.")
            else:
                print("[-] Wrong parameter! Options:\ninvestigations / tasks / taskvars / actions / evidences / "
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
            print('[-] Error occured while trying to write file: ' + destpath)


    def dynamic_import(self, abs_module_path, class_name):
        module_object = import_module(abs_module_path)
        target_class = getattr(module_object, class_name)
        return target_class

    def dynamic_import2(self, abs_module_path, class_name):
        imported = getattr(__import__(abs_module_path, fromlist=[class_name]), class_name)
        return imported


    def export_modelcontents(self, p_format, package, class_name):
        print("[i] Exporting " + class_name)
        try:
            # from tasks.models import EvidenceFormat
            imported_model = self.dynamic_import(package, class_name)
            queryset = imported_model.objects.all().values()#.values_list('username', flat=True)
            # fieldlistraw = EvidenceFormat._meta.get_fields()
            fieldlistraw = [x for x in imported_model().__dict__.keys() if not x.startswith('_')]
            fieldlist=fieldlistraw
            dataset = str()
            for queryitem in queryset:
                dataset = dataset + "{"
                for fieldname in fieldlist:
                    fname = str(fieldname)
                    b64value = b64encode(str(queryitem[fname]).encode()).decode()
                    dataset = "%s \"%s\": \"%s\"," % (dataset, fname, b64value)
                dataset = dataset[:-1] + "},"
            dataset = "[%s]" % dataset[:-1]
            if p_format == "b64":
                self.save_to_file(a_filename=class_name+'.'+p_format,
                                  a_content=dataset)
        except Exception:
            raise CommandError("[!] " + class_name + " table could not be exported!")
