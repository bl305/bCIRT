# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : invs/management/comands/dbimport_new.py
# Author            : Balazs Lendvay
# Date created      : 2019.12.29
# Purpose           : dbimport file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.12.29  Lendvay     1      Initial file
# **********************************************************************;
# https://github.com/django-import-export/django-import-export/issues/397
#
# NEED TO TRY TO CREATE THE RECORDS IN ADVANCE??? CAN THIS BE PERFORMED BECAUSE OF FOREIGN KEYS?
# USE THE BEFORE IMPORT TO CREATE THE LIST OF ITEMS WITH EMPTY VALUES
#

from django.core.management.base import BaseCommand, CommandError
import tablib
from importlib import import_module
import os
from django.contrib.auth import get_user_model

User = get_user_model()

# users_models_package = 'django.contrib.auth.models'
users_models_package = 'users.resources'
users_models_class_name = ['User', 'Group']

evidences_models_package = 'tasks.resources'
evidences_models_class_name = ['EvidenceFormat','EvidenceAttrFormat','EvReputation',
                               'MitreAttck_Techniques','MitreAttck_Tactics']

evidencefinals_models_package = 'tasks.resources'
evidencefinals_models_class_name = ['Evidence','EvidenceAttr']

configurations_models_package = 'configuration.resources'
configurations_models_class_name = ['UpdatePackage']

assets_models_package = 'assets.resources'
assets_models_class_name = ['Host', 'Hostname', 'Ipaddress', 'Profile']

# invs_models_package = 'invs.resources'
# invs_models_class_name = ['InvSeverity', 'InvStatus', 'InvCategory', 'InvPhase', 'InvPriority',
#                           'InvAttackVector', 'CurrencyType', 'InvReviewRules', 'Inv']

invs_models_package = 'invs.resources'
invs_models_class_name = ['InvSeverity', 'InvStatus', 'InvCategory', 'InvPhase', 'InvPriority',
                          'InvAttackVector', 'CurrencyType', 'InvReviewRules']

invsfinal_models_package = 'invs.resources'
invsfinal_models_class_name = ['Inv']

tasks_models_package = 'tasks.resources'
tasks_models_class_name = ['TaskStatus', 'TaskCategory', 'TaskPriority', 'TaskType',
                           'TaskVarCategory', 'TaskVarType']

taskfinals_models_package = 'tasks.resources'
taskfinals_models_class_name = ['Playbook', 'Task', 'TaskTemplate', 'TaskVar',
                                'PlaybookTemplate', 'PlaybookTemplateItem']

automations_models_package = 'tasks.resources'
automations_models_class_name = ['Automation']

actions_models_package = 'tasks.resources'
actions_models_class_name = ['ScriptOs', 'ScriptCategory', 'ScriptType', 'ScriptOutput', 'OutputTarget',
                             'Type', 'Action']

actiongroups_models_package = 'tasks.resources'
actiongroups_models_class_name = ['ActionGroup', 'ActionGroupMember']

actionqs_models_package = 'tasks.resources'
actionqs_models_class_name = ['ActionQStatus', 'ActionQ']


connections_models_package = 'configuration.resources'
connections_models_class_name = ['ConnectionItem', 'ConnectionItemField']

audit_models_package = 'accounts.resources'
audit_models_class_name = ['UserAudit']

class Command(BaseCommand):
    help = 'Imports the database from backup'
    p_dir = None
    p_format = None

    def add_arguments(self, parser):
        # parser.add_argument('-a', '--all', action='store_true', help='Run all')
        parser.add_argument('-d', '--dir', type=str, help='Import from this directory')
        parser.add_argument('-f', '--format', type=str, help='Import from this format: "json/csv"')

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        pass

    def handle(self, *args, **options):
        # def handle(self, *args, **kwargs):
        self.p_dir = str(options['dir'])
        self.p_format = str(options['format'])
        # self.p_dir = str(p_dir)
        if self.p_dir is not None and self.p_format:  # == 'json':
            for class_name in users_models_class_name:
                self.import_modelcontents(self.p_format, users_models_package, class_name)

            for class_name in connections_models_class_name:
                self.import_modelcontents(self.p_format, connections_models_package, class_name)

            for class_name in configurations_models_class_name:
                self.import_modelcontents(self.p_format, configurations_models_package, class_name)

            for class_name in invs_models_class_name:
                self.import_modelcontents(self.p_format, invs_models_package, class_name)

            for class_name in tasks_models_class_name:
                self.import_modelcontents(self.p_format, tasks_models_package, class_name)

            for class_name in automations_models_class_name:
                self.import_modelcontents(self.p_format, automations_models_package, class_name)

            for class_name in actions_models_class_name:
                self.import_modelcontents(self.p_format, actions_models_package, class_name)

            for class_name in audit_models_class_name:
                self.import_modelcontents(self.p_format, audit_models_package, class_name)

            for class_name in evidences_models_class_name:
                self.import_modelcontents(self.p_format, evidences_models_package, class_name)

            for class_name in invsfinal_models_class_name:
                self.import_modelcontents(self.p_format, invsfinal_models_package, class_name)

            for class_name in taskfinals_models_class_name:
                self.import_modelcontents(self.p_format, taskfinals_models_package, class_name)

            for class_name in evidencefinals_models_class_name:
                self.import_modelcontents(self.p_format, evidencefinals_models_package, class_name)

            for class_name in assets_models_class_name:
                self.import_modelcontents(self.p_format, assets_models_package, class_name)

            for class_name in actiongroups_models_class_name:
                self.import_modelcontents(self.p_format, actiongroups_models_package, class_name)

            for class_name in actionqs_models_class_name:
                self.import_modelcontents(self.p_format, actionqs_models_package, class_name)

            # self.import_inv(self.p_format)
            # self.import_profile(self.p_format)
            # self.import_task(self.p_format)
            # self.import_tasktemplate(self.p_format)
            # self.import_taskvar(self.p_format)
            # self.import_playbook(self.p_format)
            # self.import_playbooktemplate(self.p_format)
            # self.import_playbooktemplateitem(self.p_format)
            # self.import_evidence(self.p_format)
            # self.import_evidenceattr(self.p_format)
            # self.import_actionq(self.p_format)

            print("Database import from " + self.p_dir + " finished.")
        else:
            print(r"""
usage: manage.py dbimport [-h] [-d IMPORTDIR] [-f json/csv] [--version]
        [-v {0,1,2,3}] [--settings SETTINGS]
        [--pythonpath PYTHONPATH] [--traceback] [--no-color]
            """)
        pass

    def dynamic_import(self, abs_module_path, class_name):
        module_object = import_module(abs_module_path)
        target_class = getattr(module_object, class_name)
        return target_class

    def import_modelcontents(self, p_format, package, class_name):
        class_name_resource = class_name+"Resource"
        fname = os.path.join(self.p_dir, class_name + '.' + p_format)
        fname_readable = os.access(fname, os.R_OK)
        if fname_readable:
            # try:
            imported_model = self.dynamic_import(package, class_name_resource)
            aresource = imported_model()

            # from users.resources import UserResource
            # imported_model = UserResource()
            # print(imported_model)
            dataset = tablib.Dataset().load(open(fname).read())
            result = aresource.import_data(dataset, dry_run=True, raise_errors=True)
            if not result.has_errors():
                aresource.import_data(dataset, dry_run=False, use_transactions=True)  # Actually import now
                print('[+] ' + class_name + " imported successfully")
            else:
                print('[-] ' + class_name + " ERROR importing")
                raise CommandError('[!] ' + class_name + " table could not be imported!")
            # except Exception:
            #     raise CommandError('[!] ' + class_name + " table could not be imported!")
        else:
            print('[-]' + fname + " is not readable!")

