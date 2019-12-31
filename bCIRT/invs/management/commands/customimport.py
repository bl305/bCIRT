# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : invs/management/comands/customimport.py
# Author            : Balazs Lendvay
# Date created      : 2019.12.28
# Purpose           : dbimport file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.12.28  Lendvay     1      Initial file
# **********************************************************************;
from django.core.management.base import BaseCommand, CommandError
import json
from base64 import b64decode
from importlib import import_module
import os
from django.contrib.auth import get_user_model
from tasks.models import EvReputation

User = get_user_model()

users_models_package = 'django.contrib.auth.models'
users_models_class_name = ['User', 'Group']

evidences_models_package = 'tasks.models'
evidences_models_class_name = ['EvidenceFormat','EvidenceAttrFormat','EvReputation',
                           'MitreAttck_Techniques','MitreAttck_Tactics','Evidence','EvidenceAttr']
# evidences_models_class_name = ['EvReputation']

configurations_models_package = 'configuration.models'
configurations_models_class_name = ['UpdatePackage']

assets_models_package = 'assets.models'
assets_models_class_name = ['Host', 'Hostname', 'Ipaddress', 'Profile']

invs_models_package = 'invs.models'
invs_models_class_name = ['InvSeverity', 'InvStatus', 'InvCategory', 'InvPhase', 'InvPriority',
                          'InvAttackVector', 'CurrencyType', 'InvReviewRules', 'Inv']

tasks_models_package = 'tasks.models'
tasks_models_class_name = ['TaskStatus', 'TaskCategory', 'TaskPriority', 'TaskType', 'Task', 'TaskTemplate',
                           'Playbook', 'PlaybookTemplate', 'PlaybookTemplateItem',
                           'TaskVarCategory', 'TaskVarType', 'TaskVar']
from tasks.models import PlaybookTemplate
actions_models_package = 'tasks.models'
actions_models_class_name = ['ScriptOs', 'ScriptCategory', 'ScriptType', 'ScriptOutput', 'OutputTarget',
                             'Type', 'ActionQStatus', 'ActionQ', 'ActionGroup', 'ActionGroupMember', 'Action']

connections_models_package = 'configuration.models'
connections_models_class_name = ['ConnectionItem', 'ConnectionItemField']

automations_models_package = 'tasks.models'
automations_models_class_name = ['Automation']

audit_models_package = 'accounts.models'
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
        p_format = str(options['format'])
        # self.self.p_dir = str(self.p_dir)
        if self.p_dir is not None and p_format:  # == 'json':

            for class_name in users_models_class_name:
                self.import_modelcontents(p_format, users_models_package, class_name)

            for class_name in evidences_models_class_name:
                self.import_modelcontents(p_format, evidences_models_package, class_name)

            for class_name in evidences_models_class_name:
                self.import_modelcontents(p_format, evidences_models_package, class_name)

            for class_name in configurations_models_class_name:
                self.import_modelcontents(p_format, configurations_models_package, class_name)

            for class_name in assets_models_class_name:
                self.import_modelcontents(p_format, assets_models_package, class_name)

            for class_name in invs_models_class_name:
                self.import_modelcontents(p_format, invs_models_package, class_name)

            for class_name in tasks_models_class_name:
                self.import_modelcontents(p_format, tasks_models_package, class_name)

            for class_name in actions_models_class_name:
                self.import_modelcontents(p_format, actions_models_package, class_name)

            for class_name in connections_models_class_name:
                self.import_modelcontents(p_format, connections_models_package, class_name)

            for class_name in automations_models_class_name:
                self.import_modelcontents(p_format, automations_models_package, class_name)

            for class_name in audit_models_class_name:
                self.import_modelcontents(p_format, audit_models_package, class_name)


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
        fname = os.path.join(self.p_dir, class_name + '.' + p_format)
        fname_readable = os.access(fname, os.R_OK)
        dataset = str()
        if fname_readable:
            try:
                with open(fname, 'rt') as f:
                    # dataset = dataset + str(f.readline())
                    dataset = json.load(f)
            except Exception:
                raise CommandError('[!] ' + class_name + " table could not be imported!")
            # dynamically creating a model reference
            imported_model = self.dynamic_import(package, class_name)
            for dataitem in dataset:
                # creating a new empty record for import
                actualid = None
                # newrecord = imported_model.objects.create()
                rawdataset = dict()
                # adding the key value pairs
                for akey,avalue in dataitem.items():
                    # decoding the base64 values
                    b64value = b64decode(str(avalue).encode()).decode()
                    # print("%s: %s" % (akey, b64value))
                    # updating the model
                    # setattr(newrecord,akey,avalue)
                    rawdataset[akey] = b64value
                aid = int(rawdataset['id'])
                act_obj = None
                if imported_model.objects.filter(pk=aid):
                    # need to update
                    # print("Updating %d"%aid)
                    act_obj = imported_model.objects.get(pk=aid)
                else:
                    # need to create
                    # print(class_name, str(aid))
                    if class_name == "User":
                        act_obj = imported_model.objects.create(pk=aid, username=str(aid))
                    else:
                        act_obj = imported_model.objects.create(pk=aid)
                    if act_obj and aid != act_obj.pk:
                        print("Different PK")
                    # print("Creating record %d as %d" % (aid, act_obj.pk))
                    pass
                # self.insert_many(act_obj, [act_obj])
                for akey,avalue in rawdataset.items():
                    if act_obj:
                        setattr(act_obj,akey,avalue)
                    else:
                        pass
            print('[+] ' + class_name + " imported successfully")
        else:
            print('[-]' + fname + " is not readable!")

    def insert_many(self, model_obj, my_objects):
        # list of ids where pk is unique
        in_db_ids = model_obj.__class__.objects.values_list(model_obj.__class__._meta.pk.name)
        if not in_db_ids:
            # nothing exists, save time and bulk_create
            model_obj.__class__.objects.bulk_create(my_objects)
        else:
            in_db_ids_list = [elem[0] for elem in in_db_ids]

            to_insert=[]
            for elem in my_objects:
                if not elem.pk in in_db_ids_list:
                    to_insert.append(elem)
            if to_insert:
                model_obj.__class__.objects.bulk_create(to_insert)