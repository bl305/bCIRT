# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : invs/management/commands/initdb.py
# Author            : Balazs Lendvay
# Date created      : 2019.08.19
# Purpose           : Initdb file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# 2019.08.19  Lendvay     1      Added domain to the attributes
# 2019.12.13  Lendvay     1      Fixes
# 2020.04.18  Lendvay     1      New tables
# **********************************************************************;

from django.core.management.base import BaseCommand, CommandError
from invs.models import InvStatus, InvPriority, InvCategory, InvPhase, InvAttackVector, CurrencyType, InvReviewRules
from invs.models import InvSeverity, InvSeverityCriteria, InvSeverityCriteriaCategory
# InvSeverityContact, InvSeverityContactRef
from tasks.models import MitreAttck_Tactics, MitreAttck_Techniques
from tasks.models import TaskVarType, TaskVarCategory, TaskType, TaskCategory, TaskStatus, TaskPriority
from tasks.models import ScriptOs, ScriptType, ScriptCategory, Action, Type, ActionQStatus, OutputTarget, ScriptOutput
from tasks.models import Automation
from tasks.models import EvidenceFormat, EvidenceAttrFormat, EvReputation, ScriptInput
from users.models import Profile
from knowledgebase.models import KnowledgeBase, KnowledgeBaseFormat
from configuration.models import SettingsCategory, SettingsUser, SettingsSystem
from bCIRT.custom_variables import bcolors
# from bCIRT.settings import PROJECT_ROOT
# from os import path
from django.contrib.auth import get_user_model
User = get_user_model()

class Command(BaseCommand):
    help = 'Initiates the database with pre-defined values'

    def add_arguments(self, parser):
        # parser.add_argument('-a', '--all', action='store_true', help='Run all')
        parser.add_argument('-a', '--all', action='store_true', help='Init the whole database')
        parser.add_argument('-c', '--clear', action='store_true', help='Clear standard tables')
        parser.add_argument('-i', '--table_name', type=str, help='Init the specified module tables')

    def __init__(self, *args, **kwargs):
        print("[i] This adds an admin user if the database has no users yet!")
        print("[i] Make sure you change the admin password after install!!!")
        if User.objects.count() == 0:
            adminpw = "Password1."
            User.objects.create_superuser('admin', 'admin@example.com', adminpw)
            # print("[!] Added default user admin: %s" % adminpw)
            print(f"{bcolors.FAIL}[!] Added default user admin: %s{bcolors.ENDC}" % adminpw)
        super(Command, self).__init__(*args, **kwargs)
        pass

    def handle(self, *args, **options):
        print("[i] Initiating database, will only run once!")
        print("[i] This will only run, if there is a file called 'init.check' in the root with the content:'1'")
        print("[i] Once the init ran, it will empty the file.")
        resetfile=False
        try:
            with open('init.check', 'r') as file:
                data = file.read().replace('\n', '')
                if data == "1":
                    print("[i] Running init")
                    resetfile = True
                else:
                    print("[!] No init.check file with content '1', so not running init, exiting")
                    exit(1)
        except Exception as ex1:
            print("[!] Exception: No init.check file with content '1', so not running init, exiting| %s"%ex1)
        # checking for the init file value
            exit(1)

        if resetfile:
            file = open('init.check', 'w')
            file.write("Replace this with a '1' if you want to enable init")
            file.close()
            print("[i] Reset init.check file")

        print("[i] Use 'python3 manage.py initdb --help' for options")
        # def handle(self, *args, **kwargs):
        p_all = options['all']
        p_clear = options['clear']
        p_table = options['table_name']
        if p_all:
            self.populate_evidenceformat()
            self.populate_evidenceattrformat()
            self.populate_evreputation()

            self.populate_currencytype()
            self.populate_invseverity()
            self.populate_invstatus()
            self.populate_invcategory()
            self.populate_invphase()
            self.populate_invpriority()
            self.populate_invattackvector()
            self.populate_InvSeverityCriteriaCategory()
            self.populate_InvSeverityCriteria()
            self.populate_userprofile()
            self.populate_InvReviewRules()

            self.populate_taskstatus()
            self.populate_taskcategory()
            self.populate_taskpriority()
            self.populate_tasktype()

            self.populate_taskvarcategory()
            self.populate_taskvartype()

            self.populate_actscriptos()
            self.populate_actscriptcategory()
            self.populate_actscripttype()
            self.populate_actscriptoutput()
            self.populate_actscriptinput()
            self.populate_actoutputtarget()
            self.populate_acttype()
            self.populate_actionqstatus()
            # self.populate_action()
            self.populate_automation()

            self.populate_settingscategory()
            self.populate_settingsuser()
            self.populate_settingssystem()

            self.populate_KnowledgeBaseFormat()
            self.populate_KnowledgeBase()

            self.populate_mitreattck_tactics()
            # self.populate_mitreattck_techniques()
        elif p_clear:
            print("clear")
        elif p_table:
            if p_table == "investigations":
                self.populate_currencytype()
                self.populate_invseverity()
                self.populate_invstatus()
                self.populate_invcategory()
                self.populate_invphase()
                self.populate_invpriority()
                self.populate_invattackvector()
                self.populate_InvSeverityCriteriaCategory()
                self.populate_InvSeverityCriteria()
                self.populate_userprofile()
                self.populate_InvReviewRules()
            elif p_table == "evidences":
                self.populate_evidenceformat()
                self.populate_evidenceattrformat()
                self.populate_evreputation()
            elif p_table == "tasks":
                self.populate_taskstatus()
                self.populate_taskcategory()
                self.populate_taskpriority()
                self.populate_tasktype()
            elif p_table == "taskvars":
                self.populate_taskvarcategory()
                self.populate_taskvartype()
            elif p_table == "actions":
                self.populate_actscriptos()
                self.populate_actscriptcategory()
                self.populate_actscripttype()
                self.populate_actscriptoutput()
                self.populate_actscriptinput()
                self.populate_actoutputtarget()
                self.populate_acttype()
                self.populate_actionqstatus()
                # self.populate_action()
            elif p_table == "settings":
                self.populate_settingscategory()
                self.populate_settingsuser()
                self.populate_settingssystem()
            elif p_table == "knowledgebase":
                self.populate_KnowledgeBaseFormat()
                self.populate_KnowledgeBase()
            elif p_table == "mitre":
                self.populate_mitreattck_tactics()
                # self.populate_mitreattck_techniques()
            else:
                print("Wrong parameter! Options:\ninvestigations / tasks / taskvars / actions / evidences / mitre"
                      " / settings / knowledgebase \n")
        else:
            print(r"""
usage: manage.py initdb [-h] [-a] [-c] [-i TABLE_NAME] [--version]
            [-v {0,1,2,3}] [--settings SETTINGS]
            [--pythonpath PYTHONPATH] [--traceback] [--no-color]
            """)
        print("Database initiation is finished.")
        pass

    def populate_evidenceformat(self):
        evidenceformat = [
            {
                "name": "RAW",
                "enabled": "1",
                "description": "RAW type of evidence"
            },
            {
                "name": "TinyMCE",
                "enabled": "1",
                "description": "TinyMCE rich text/html"
            },
        ]
        try:
            self.stdout.write("Initiating EvidenceFormat")
            for evformatitem in evidenceformat:
                EvidenceFormat.objects.create(
                    name=evformatitem['name'],
                    enabled=evformatitem['enabled'],
                    description=evformatitem['description']
                )
        except Exception:
            raise CommandError("EvidenceFormat table could not be updated!")

    def populate_evidenceattrformat(self):
        evidenceattrformat = [
            {
                "name": "Unknown",
                "enabled": "1",
                "description": "Unknown type"
            },
            {
                "name": "UserName",
                "enabled": "1",
                "description": "Name of a user"
            },
            {
                "name": "Email",
                "enabled": "1",
                "description": "Email address of a user"
            },
            {
                "name": "HostName",
                "enabled": "1",
                "description": "Hostname of a device"
            },
            {
                "name": "IPv4",
                "enabled": "1",
                "description": "IPv4 address of a device"
            },
            {
                "name": "IPv6",
                "enabled": "1",
                "description": "IPv6 address of a device"
            },
            {
                "name": "URL",
                "enabled": "1",
                "description": "URL value"
            },
            {
                "name": "FileName",
                "enabled": "1",
                "description": "Name of a file"
            },
            {
                "name": "Hash_MD5",
                "enabled": "1",
                "description": "MD5 hash of something"
            },
            {
                "name": "Hash_SHA1",
                "enabled": "1",
                "description": "SHA1 hash of something"
            },
            {
                "name": "Hash_SHA256",
                "enabled": "1",
                "description": "SHA256 hash of something"
            },
            {
                "name": "Hash_SHA512",
                "enabled": "1",
                "description": "SHA512 hash of something"
            },
            {
                "name": "Reputation",
                "enabled": "1",
                "description": "Reputation of something"
            },
            {
                "name": "UserID",
                "enabled": "1",
                "description": "UserID of a user"
            },
            {
                "name": "Domain",
                "enabled": "1",
                "description": "Domain address"
            },
            {
                "name": "Question",
                "enabled": "1",
                "description": "Question"
            },
       ]
        try:
            self.stdout.write("Initiating EvidenceAttrFormat")
            for evattrformatitem in evidenceattrformat:
                EvidenceAttrFormat.objects.create(
                    name=evattrformatitem['name'],
                    enabled=evattrformatitem['enabled'],
                    description=evattrformatitem['description']
                )
        except Exception:
            raise CommandError("EvidenceAttrFormat table could not be updated!")

    def populate_evreputation(self):
        evreputation = [
            {
                "name": "Unknown",
                "enabled": "1",
                "description": "Item has been checked, but reputation databases have no good or bad reputation value "
                               "for this item."
            },
            {
                "name": "Clean",
                "enabled": "1",
                "description": "Reputation database contains the item and it is clean."
            },
            {
                "name": "Suspicious",
                "enabled": "1",
                "description": "Reputation database contains some information but cannot tell for sure."
            },
            {
                "name": "Malicious",
                "enabled": "1",
                "description": "The item is malicious."
            }
        ]
        try:
            self.stdout.write("Initiating Evreputation")
            for evreputationitem in evreputation:
                EvReputation.objects.create(
                    name=evreputationitem['name'],
                    enabled=evreputationitem['enabled'],
                    description=evreputationitem['description']
                )
        except Exception:
            raise CommandError("Evidence Reputation table could not be updated!")

    def populate_currencytype(self):
        currencytype = [
            {
                "currencyname": "Euro",
                "currencyshortname": "EUR",
                "enabled": "1",
            },
            {
                "currencyname": "USA Dollar",
                "currencyshortname": "USD",
                "enabled": "1",
            },
        ]
        try:
            self.stdout.write("Initiating CurrencyType")
            for currencytypeitem in currencytype:
                CurrencyType.objects.create(
                    currencyname=currencytypeitem['currencyname'],
                    enabled=currencytypeitem['enabled'],
                    currencyshortname=currencytypeitem['currencyshortname']
                )
        except Exception:
            raise CommandError("CurrencyType table could not be updated!")

    def populate_invstatus(self):
        invstatus = [
            {
                "name": "Open",
                "enabled": "1",
                "description": "Open Investigation"
            },
            {
                "name": "Closed",
                "enabled": "1",
                "description": "Closed Investigation"
            },
            {
                "name": "Assigned",
                "enabled": "1",
                "description": "Assigned Investigation"
            },
            {
                "name": "Archived",
                "enabled": "1",
                "description": "Archived Investigation"
            },
            {
                "name": "Review1",
                "enabled": "1",
                "description": "#1 reviewer"
            },
            {
                "name": "Review2",
                "enabled": "1",
                "description": "#2 reviewer"
            },

        ]
        try:
            self.stdout.write("Initiating InvStatus")
            for invstatitem in invstatus:
                InvStatus.objects.create(
                    name=invstatitem['name'],
                    enabled=invstatitem['enabled'],
                    description=invstatitem['description']
                )
        except Exception:
            raise CommandError("InvStatus table could not be updated!")

    def populate_invseverity(self):
        invseverity = [
            {
                "name": "S0 Baseline",
                "enabled": "1",
                "description": "S0 Baseline",
                "color": "ffffff",
                "notificationfrequency": "0",
            },
            {
                "name": "S1 Low",
                "enabled": "1",
                "description": "S1 Low",
                "color": "9afc9f",
                "notificationfrequency": "0",
            },
            {
                "name": "S2 Medium",
                "enabled": "1",
                "description": "S2 Medium",
                "color": "ace0fc",
                "notificationfrequency": "8",
            },
            {
                "name": "S3 High",
                "enabled": "1",
                "description": "S3 High",
                "color": "fff200",
                "notificationfrequency": "4",
            },
            {
                "name": "S4 Severe",
                "enabled": "1",
                "description": "S4 Severe",
                "color": "FFA500",
                "notificationfrequency": "2",
            },
            {
                "name": "S5 Emergency",
                "enabled": "1",
                "description": "S5 Emergency",
                "color": "ff6666",
                "notificationfrequency": "1",
            },
        ]

        try:
            self.stdout.write("Initiating InvSeverity")
            for invsevitem in invseverity:
                InvSeverity.objects.create(
                    name=invsevitem['name'],
                    enabled=invsevitem['enabled'],
                    description=invsevitem['description'],
                    color=invsevitem['color'],
                    notificationfrequency=invsevitem['notificationfrequency']
                )
        except Exception:
            raise CommandError("InvSeverity table could not be updated!")

    def populate_invpriority(self):
        invpriority = [
            {
                "name": "Low",
                "enabled": "1",
                "description": "Low"
            },
            {
                "name": "Medium",
                "enabled": "1",
                "description": "Medium"
            },
            {
                "name": "High",
                "enabled": "1",
                "description": "High"
            },
        ]
        try:
            self.stdout.write("Initiating InvPriority")
            for invprioitem in invpriority:
                InvPriority.objects.create(
                    name=invprioitem['name'],
                    enabled=invprioitem['enabled'],
                    description=invprioitem['description']
                )
        except Exception:
            raise CommandError("InvPriority table could not be updated!")

    def populate_invphase(self):
        invphase = [
            {
                "name": "P1 Preparation",
                "enabled": "1",
                "description": "P1 Preparation"
            },
            {
                "name": "P2 Detection, Analysis",
                "enabled": "1",
                "description": "P2 Detection, Analysis"
            },
            {
                "name": "P3 Containment, Eradication,Recovery",
                "enabled": "1",
                "description": "P3 Containment, Eradication,Recovery"
            },
            {
                "name": "P4 Post-Incident",
                "enabled": "1",
                "description": "P4 Post-Incident"
            },

        ]
        try:
            self.stdout.write("Initiating InvPhase")
            for invphaitem in invphase:
                InvPhase.objects.create(
                    name=invphaitem['name'],
                    enabled=invphaitem['enabled'],
                    description=invphaitem['description']
                )
        except Exception:
            raise CommandError("InvPhase table could not be updated!")

    def populate_invcategory(self):
        invcategory = [
            {
                "name": "Exercise/Network Defense Testing",
                "enabled": "1",
                "reporting_timeframe": "Not Applicable; this category is for each agency's internal use during"
                                       " exercises.",
                "catid": "CAT 0",
                "description": "This category is used during state, federal, national, international exercises"
                               " and approved activity testing of internal/external network defenses or responses."
            },
            {
                "name": "Unauthorized Access",
                "enabled": "1",
                "reporting_timeframe": "Within one (1) hour of discovery/detection.",
                "catid": "CAT 1",
                "description": "In this category an individual gains logical or physical access without permission to"
                               " a federal agency network, system, application, data, or other resource"
            },
            {
                "name": "Denial of Service (DoS)",
                "enabled": "1",
                "reporting_timeframe": "Within two (2) hours of discovery/detection if the successful attack is still "
                                       "ongoing and the agency is unable to successfully mitigate activity.",
                "catid": "CAT 2",
                "description": "An attack that successfully prevents or impairs the normal authorized functionality"
                               " of networks, systems or applications by exhausting resources. This activity includes"
                               " being the victim or participating in the DoS."
            },
            {
                "name": "Malicious Code",
                "enabled": "1",
                "reporting_timeframe": "Daily \nNote: Within one (1) hour of discovery/detection if widespread across "
                                       "agency.",
                "catid": "CAT 3",
                "description": "Successful installation of malicious software (e.g., virus, worm, Trojan horse, "
                               "or other code-based malicious entity) that infects an operating system or application."
                               " Agencies are NOT required to report malicious logic that has been successfully"
                               " quarantined by antivirus (AV) software."
            },
            {
                "name": "Improper Usage",
                "enabled": "1",
                "reporting_timeframe": "Monthly\nNote: If system is classified, report within one (1) hour of "
                                       "discovery.",
                "catid": "CAT 4",
                "description": "This category includes any activity that seeks to access or identify a federal agency"
                               " computer, open ports, protocols, service, or any combination for later exploit. This"
                               " activity does not directly result in a compromise or denial of service."
            },
            {
                "name": 'Scans/Probes/Attempted Access',
                "enabled": "1",
                "reporting_timeframe": "Monthly\nNote: If system is classified, report within one (1) hour of "
                                       "discovery.",
                "catid": "CAT 5",
                "description": "This category includes any activity that seeks to access or identify a computer,"
                               " open ports, protocols, service, or any combination for later exploit. "
                               "This activity does not directly result in a compromise or denial of service."
            },
            {
                "name": "Investigation",
                "enabled": "1",
                "reporting_timeframe": "Not Applicable; this category is for each agency's use to categorize a"
                                       " potential incident that is currently being investigated.",
                "catid": "CAT 6",
                "description": "Unconfirmed incidents that are potentially malicious or anomalous activity deemed by"
                               " the reporting entity to warrant further review."
            },
        ]
        try:
            self.stdout.write("Initiating InvCategory")
            for invcatitem in invcategory:
                InvCategory.objects.create(
                    name=invcatitem['name'],
                    enabled=invcatitem['enabled'],
                    reporting_timeframe=invcatitem['reporting_timeframe'],
                    catid=invcatitem['catid'],
                    description=invcatitem['description']
                )
        except Exception:
            raise CommandError("InvCategory table could not be updated!")

    def populate_invattackvector(self):
        invattackvector = [
            {
                "name": "Unknown",
                "enabled": "1",
                "description": "Unknown attack vector"
            },
            {
                "name": "Account compromise",
                "enabled": "1",
                "description": "Account compromise or misuse"
            },
            {
                "name": "Data Breach / Data Leak",
                "enabled": "1",
                "description": "Data breach or data leak"
            },
            {
                "name": "Denial of Service",
                "enabled": "1",
                "description": "Malware, Virus, Ransomware, malicious code"
            },
            {
                "name": "Fraud",
                "enabled": "1",
                "description": "Financial fraud"
            },
            {
                "name": "Lost/Stolen device",
                "enabled": "1",
                "description": "Lost or stolen device, laptop, smartphone, external drive etc."
            },
            {
                "name": "Malware",
                "enabled": "1",
                "description": "Malware, Virus, Ransomware, malicious code"
            },
            {
                "name": "Phishing",
                "enabled": "1",
                "description": "Phishing incident"
            },
            {
                "name": "Social Engineering",
                "enabled": "1",
                "description": "Social Engineering other than phishing"
            },
            {
                "name": "False Positive",
                "enabled": "1",
                "description": "False positive, not a security incident"
            },
        ]
        try:
            self.stdout.write("Initiating InvAttackVecotr")
            for invattackvectoritem in invattackvector:
                InvAttackVector.objects.create(
                    name=invattackvectoritem['name'],
                    enabled=invattackvectoritem['enabled'],
                    description=invattackvectoritem['description']
                )
        except Exception:
            raise CommandError("InvAttackVector table could not be updated!")

    def populate_InvSeverityCriteriaCategory(self):
        invsevecitycriteriacategory = [
            {
                "name": "Business Impact",
                "enabled": "1",
                "description": "Determines the business impact",
            },
            {
                "name": "Functional Impact",
                "enabled": "1",
                "description": "Determines the financial impact",
            },
            {
                "name": "Manufacturing Impact",
                "enabled": "1",
                "description": "Determines the manufacturing impact",
            },
            {
                "name": "Recoverability Impact",
                "enabled": "1",
                "description": "Determines the impact on the recover procedures",
            },
            {
                "name": "Information Impact",
                "enabled": "1",
                "description": "Determines the impact on information security",
            },
        ]

        try:
            self.stdout.write("Initiating InvSeverityCriteriaCategory")
            for invseveritycriteriacategoryitem in invsevecitycriteriacategory:
                InvSeverityCriteriaCategory.objects.create(
                    name=invseveritycriteriacategoryitem['name'],
                    enabled=invseveritycriteriacategoryitem['enabled'],
                    description=invseveritycriteriacategoryitem['description']
                )
        except Exception:
            raise CommandError("InvSeverityCriteriaCategory table could not be updated!")

    def populate_InvSeverityCriteria(self):
        invsevecitycriteria = [
            {
                "severity": InvSeverity.objects.get(pk=1),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=1),
                "enabled": "1",
                "description": "Greater than 14 days without adversely impacting the business process it supports.",
            },
            {
                "severity": InvSeverity.objects.get(pk=1),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=2),
                "enabled": "1",
                "description": "No effect to the organization’s ability to provide all services to all users.",
            },
            {
                "severity": InvSeverity.objects.get(pk=1),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=3),
                "enabled": "1",
                "description": "Manufacturing is not degraded.",
            },
            {
                "severity": InvSeverity.objects.get(pk=1),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=4),
                "enabled": "1",
                "description": "Time to recovery is predictable with existing resources.",
            },
            {
                "severity": InvSeverity.objects.get(pk=1),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=5),
                "enabled": "1",
                "description": "No information was exfiltrated, changed, deleted, or otherwise compromised.",
            },
            {
                "severity": InvSeverity.objects.get(pk=2),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=1),
                "enabled": "1",
                "description": "7 to 14 days without adversely impacting the business process it supports.",
            },
            {
                "severity": InvSeverity.objects.get(pk=2),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=2),
                "enabled": "1",
                "description": "Non-critical system(s) availability is impacted.",
            },
            {
                "severity": InvSeverity.objects.get(pk=2),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=3),
                "enabled": "1",
                "description": "Manufacturing is degraded but functioning.",
            },
            {
                "severity": InvSeverity.objects.get(pk=2),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=4),
                "enabled": "1",
                "description": "Time to recovery is predictable with additional resources.",
            },
            {
                "severity": InvSeverity.objects.get(pk=2),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=5),
                "enabled": "1",
                "description": "Sensitive information was accessed internally.",
            },
            {
                "severity": InvSeverity.objects.get(pk=3),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=1),
                "enabled": "1",
                "description": "4 to 7 days without adversely impacting the business process it supports.",
            },
            {
                "severity": InvSeverity.objects.get(pk=3),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=2),
                "enabled": "1",
                "description": "Critical services lost efficiency.",
            },
            {
                "severity": InvSeverity.objects.get(pk=3),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=3),
                "enabled": "1",
                "description": "Manufacturing outage for less than 8 hours.",
            },
            {
                "severity": InvSeverity.objects.get(pk=3),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=4),
                "enabled": "1",
                "description": "Time to recovery is predictable; additional resources and outside help are needed.",
            },
            {
                "severity": InvSeverity.objects.get(pk=3),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=5),
                "enabled": "1",
                "description": "Sensitive information was accessed externally.",
            },
            {
                "severity": InvSeverity.objects.get(pk=4),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=1),
                "enabled": "1",
                "description": "0 to 3 days likely impacting business process it supports.",
            },
            {
                "severity": InvSeverity.objects.get(pk=4),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=2),
                "enabled": "1",
                "description": "Critical services not available to a subset of system users.",
            },
            {
                "severity": InvSeverity.objects.get(pk=4),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=3),
                "enabled": "1",
                "description": "Manufacturing outage for more than 24 hours.",
            },
            {
                "severity": InvSeverity.objects.get(pk=4),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=4),
                "enabled": "1",
                "description": "Time to recovery is unpredictable; additional resources and outside help are needed",
            },
            {
                "severity": InvSeverity.objects.get(pk=4),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=5),
                "enabled": "1",
                "description": "Some sensitive information was exfiltrated.",
            },
            {
                "severity": InvSeverity.objects.get(pk=5),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=1),
                "enabled": "1",
                "description": "Impacting systems always required to be available (24x7x365).",
            },
            {
                "severity": InvSeverity.objects.get(pk=5),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=2),
                "enabled": "1",
                "description": "Critical services are not available.",
            },
            {
                "severity": InvSeverity.objects.get(pk=5),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=3),
                "enabled": "1",
                "description": "Manufacturing is impacted for longer than 24 hours.",
            },
            {
                "severity": InvSeverity.objects.get(pk=5),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=4),
                "enabled": "1",
                "description": "Recovery from the incident is not possible (e.g., sensitive data posted publicly).",
            },
            {
                "severity": InvSeverity.objects.get(pk=5),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=5),
                "enabled": "1",
                "description": "Large amount of sensitive information was changed or deleted or exfiltrated.",
            },
            {
                "severity": InvSeverity.objects.get(pk=6),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=1),
                "enabled": "1",
                "description": "",
            },
            {
                "severity": InvSeverity.objects.get(pk=6),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=2),
                "enabled": "1",
                "description": "",
            },
            {
                "severity": InvSeverity.objects.get(pk=6),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=3),
                "enabled": "1",
                "description": "",
            },
            {
                "severity": InvSeverity.objects.get(pk=6),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=4),
                "enabled": "1",
                "description": "",
            },
            {
                "severity": InvSeverity.objects.get(pk=6),
                "criteriacategory": InvSeverityCriteriaCategory.objects.get(pk=5),
                "enabled": "1",
                "description": "",
            },
        ]

        try:
            self.stdout.write("Initiating InvSeverityCriteria")
            for invseveritycriteriaitem in invsevecitycriteria:
                InvSeverityCriteria.objects.create(
                    severity=invseveritycriteriaitem['severity'],
                    criteriacategory=invseveritycriteriaitem['criteriacategory'],
                    enabled=invseveritycriteriaitem['enabled'],
                    description=invseveritycriteriaitem['description']
                )
        except Exception:
            raise CommandError("InvSeverityCriteria table could not be updated!")

    def populate_userprofile(self):
        pass


    def populate_InvReviewRules(self):
        invreviewrules = [
            {
                "bypassreview": "0",
                "rulename": "default-no review",
                "severity": InvSeverity.objects.get(pk=2),
                "category": None,
                "priority": None,
                "attackvector": None,
                "potentialloss": "0",
                "monetaryloss": "0",
                "review1": "0",
                "review2": "0",
                "enabled": "1",
            },
            {
                "bypassreview": "0",
                "rulename": "Bypass phishing rev2",
                "severity": InvSeverity.objects.get(pk=2),
                "category": None,
                "priority": None,
                "attackvector": InvAttackVector.objects.get(pk=8),
                "potentialloss": "0",
                "monetaryloss": "0",
                "review1": "1",
                "review2": "0",
                "enabled": "0",
            },
        ]

        try:
            self.stdout.write("Initiating InvReviewRules")
            for invreviewrulesitem in invreviewrules:
                InvReviewRules.objects.create(
                    bypassreview=invreviewrulesitem['bypassreview'],
                    rulename=invreviewrulesitem['rulename'],
                    severity=invreviewrulesitem['severity'],
                    category=invreviewrulesitem['category'],
                    priority=invreviewrulesitem['priority'],
                    attackvector=invreviewrulesitem['attackvector'],
                    potentialloss=invreviewrulesitem['potentialloss'],
                    monetaryloss=invreviewrulesitem['monetaryloss'],
                    review1=invreviewrulesitem['review1'],
                    review2=invreviewrulesitem['review2'],
                    enabled=invreviewrulesitem['enabled'],
                )
        except Exception:
            raise CommandError("InvReviewRules table could not be updated!")


    def populate_actscriptos(self):
        actscriptos = [
            {
                "name": "Windows 10",
                "version": "1803",
                "enabled": "1",
                "description": "Windows 10 1803"
            },
            {
                "name": "Linux",
                "version": "Ubuntu 18.04",
                "enabled": "1",
                "description": "Ubuntu 18.04 LTS"
            },
        ]
        try:
            self.stdout.write("Initiating ActScriptOs")
            for actscriptositem in actscriptos:
                ScriptOs.objects.create(
                    name=actscriptositem['name'],
                    version=actscriptositem['version'],
                    enabled=actscriptositem['enabled'],
                    description=actscriptositem['description']
                )
        except Exception:
            raise CommandError("ActionScriptOs table could not be updated!")

    def populate_actscriptcategory(self):
        actscriptcategory = [
            {
                "name": "Generic",
                "enabled": "1",
                "description": "Generic script",
            },
        ]

        try:
            self.stdout.write("Initiating ActScriptCategory")
            for actscriptcategoryitem in actscriptcategory:
                ScriptCategory.objects.create(
                    name=actscriptcategoryitem['name'],
                    enabled=actscriptcategoryitem['enabled'],
                    description=actscriptcategoryitem['description']
                )
        except Exception:
            raise CommandError("ActionScriptCategory table could not be updated!")

    def populate_actscripttype(self):
        actscripttype = [
            {
                "name": "Python",
                "enabled": "1",
                "description": "Runs the OS default Python",
                "version": "any",
                "os": ScriptOs.objects.get(pk=2),
                "interpreter": "/usr/bin/python"
            },
            {
                "name": "Custom Python 3.6",
                "enabled": "1",
                "description": "Custom Python virtual environment",
                "version": "3.6+",
                "os": ScriptOs.objects.get(pk=2),
                "interpreter": "/home/bali/PycharmProjects/bCIRT_venv_Actions/bin/python3"
            },
            {
                "name": "Custom Python 2.6",
                "enabled": "1",
                "description": "Custom Python virtual environment",
                "version": "2.7",
                "os": ScriptOs.objects.get(pk=2),
                "interpreter": "/home/bali/PycharmProjects/bCIRT_venv2_Actions/bin/python2.7"
            },
            {
                "name": "Bash",
                "enabled": "1",
                "description": "Bash script",
                "version": "4.4.19",
                "os": ScriptOs.objects.get(pk=2),
                "interpreter": "/bin/bash"
            },
        ]
        try:
            self.stdout.write("Initiating ActScriptType")
            for actscripttypeitem in actscripttype:
                ScriptType.objects.create(
                    name=actscripttypeitem['name'],
                    enabled=actscripttypeitem['enabled'],
                    description=actscripttypeitem['description'],
                    version=actscripttypeitem['version'],
                    os=actscripttypeitem['os'],
                    interpreter=actscripttypeitem['interpreter']
                )
        except Exception:
            raise CommandError("ActionScriptType table could not be updated!")

    def populate_actoutputtarget(self):
        actoutputtarget = [
            {
                "name": "Description",
                "shortname": "D",
                "enabled": "1",
                "description": "Output goes to the description field.",
            },
            {
                "name": "Attribute",
                "shortname": "A",
                "enabled": "1",
                "description": "Output goes to the attribute field.",
            },
            {
                "name": "File",
                "shortname": "F",
                "enabled": "1",
                "description": "Output goes to the file attachment.",
            },
            {
                "name": "DropIt",
                "shortname": "X",
                "enabled": "1",
                "description": "Output goes to the bin, not captured.",
            },
        ]
        try:
            self.stdout.write("Initiating ActOutputTarget")
            for actscripttypeitem in actoutputtarget:
                OutputTarget.objects.create(
                    name=actscripttypeitem['name'],
                    enabled=actscripttypeitem['enabled'],
                    description=actscripttypeitem['description'],
                )
        except Exception:
            raise CommandError("ActionOutputTarget table could not be updated!")

    def populate_actscriptoutput(self):
        actscriptoutput = [
            {
                "name": "Default",
                "enabled": "1",
                "delimiter": '',
                "description": "Use output as it is",
            },
            {
                "name": "CSV",
                "enabled": "1",
                "delimiter": ',',
                "description": "Comma separated values",
            },
            {
                "name": "Line-by-Line",
                "enabled": "1",
                "delimiter": '',
                "description": "Newline separated values",
            },
            {
                "name": "List",
                "enabled": "1",
                "delimiter": '',
                "description": "List type of values",
            },
        ]
        try:
            self.stdout.write("Initiating ActScriptOutput")
            for actscriptoutputitem in actscriptoutput:
                ScriptOutput.objects.create(
                    name=actscriptoutputitem['name'],
                    enabled=actscriptoutputitem['enabled'],
                    delimiter=actscriptoutputitem['delimiter'],
                    description=actscriptoutputitem['description'],
                )
        except Exception:
            raise CommandError("ActionScriptOutput table could not be updated!")

    def populate_actscriptinput(self):
        actscriptinput = [
            {
                "name": "Description",
                "shortname": "D",
                "enabled": "1",
                "description": "Evidence description field",
            },
            {
                "name": "File",
                "shortname": "F",
                "enabled": "1",
                "description": "File based",
            },
            {
                "name": "Attribute",
                "shortname": "A",
                "enabled": "1",
                "description": "Evidence Attribute field",
            },
        ]
        try:
            self.stdout.write("Initiating ActScriptInput")
            for actscriptinputitem in actscriptinput:
                ScriptInput.objects.create(
                    name=actscriptinputitem['name'],
                    enabled=actscriptinputitem['enabled'],
                    description=actscriptinputitem['description'],
                )
        except Exception:
            raise CommandError("ActionScriptInput table could not be updated!")

    def populate_acttype(self):
        acttype = [
            {
                "name": "Command",
                "enabled": "1",
                "description": "Simple command to be executed",
            },
            {
                "name": "Executable",
                "enabled": "1",
                "description": "Executable binary",
            },
            {
                "name": "Script",
                "enabled": "1",
                "description": "Script",
            },
            {
                "name": "Script_b64",
                "enabled": "1",
                "description": "Script accepting b64 encrypted arguments",
            },
            {
                "name": "Internal",
                "enabled": "1",
                "description": "Internal command/script",
            },
        ]
        try:
            self.stdout.write("Initiating ActType")
            for acttypeitem in acttype:
                Type.objects.create(
                    name=acttypeitem['name'],
                    enabled=acttypeitem['enabled'],
                    description=acttypeitem['description'],
                )
        except Exception:
            raise CommandError("ActionType table could not be updated!")

    def populate_taskcategory(self):
        taskcategory = [
            {
                "catid": "C01",
                "acknowledge_required": "1",
                "resolution_required": "1",
                "name": "Generic",
                "enabled": "1",
                "description": "Generic task"
            },
            {
                "catid": "C02",
                "acknowledge_required": "1",
                "resolution_required": "1",
                "name": "Email",
                "enabled": "1",
                "description": "Email related task"
            },
            {
                "catid": "C03",
                "acknowledge_required": "4",
                "resolution_required": "8",
                "name": "File analysis",
                "enabled": "1",
                "description": "File analysis related"
            },
            {
                "catid": "C04",
                "acknowledge_required": "4",
                "resolution_required": "8",
                "name": "Parser",
                "enabled": "1",
                "description": "Parse text for useful information pieces."
            },
            {
                "catid": "C05",
                "acknowledge_required": "4",
                "resolution_required": "8",
                "name": "Reputation",
                "enabled": "1",
                "description": "Check the reputation of an evidence."
            },
        ]

        try:
            self.stdout.write("Initiating TaskCategory")
            for taskcategoryitem in taskcategory:
                TaskCategory.objects.create(
                    name=taskcategoryitem['name'],
                    enabled=taskcategoryitem['enabled'],
                    description=taskcategoryitem['description'],
                    catid=taskcategoryitem['catid'],
                    acknowledge_required=taskcategoryitem['acknowledge_required'],
                    resolution_required=taskcategoryitem['resolution_required']
                )
        except Exception:
            raise CommandError("TaskCategory table could not be updated!")

    def populate_taskpriority(self):
        taskpriority = [
            {
                "name": "P3",
                "enabled": "1",
                "description": "Priority 3"
            },
            {
                "name": "P2",
                "enabled": "1",
                "description": "Priority 2"
            },
            {
                "name": "P1",
                "enabled": "1",
                "description": "Priority 1"
            },
        ]

        try:
            self.stdout.write("Initiating TaskPriority")
            for taskpriorityitem in taskpriority:
                TaskPriority.objects.create(
                    name=taskpriorityitem['name'],
                    enabled=taskpriorityitem['enabled'],
                    description=taskpriorityitem['description'],
                )
        except Exception:
            raise CommandError("TaskPriority table could not be updated!")

    def populate_taskstatus(self):
        taskstatus = [
            {
                "name": "Open",
                "enabled": "1",
                "description": "New Task"
            },
            {
                "name": "Completed",
                "enabled": "1",
                "description": "Completed"
            },
            {
                "name": "Assigned",
                "enabled": "1",
                "description": "Assigned"
            },
            {
                "name": "Skipped",
                "enabled": "1",
                "description": "Skipped"
            },
            {
                "name": "Waiting",
                "enabled": "1",
                "description": "Waiting"
            },
        ]

        try:
            self.stdout.write("Initiating TaskStatus")
            for taskstatusitem in taskstatus:
                TaskStatus.objects.create(
                    name=taskstatusitem['name'],
                    enabled=taskstatusitem['enabled'],
                    description=taskstatusitem['description'],
                )
        except Exception:
            raise CommandError("TaskStatus table could not be updated!")

    def populate_tasktype(self):
        tasktype = [
            {
                "name": "Automated",
                "enabled": "1",
                "description": "Sample automated task",
                "typeid": "T01"
            },
            {
                "name": "Manual",
                "enabled": "1",
                "description": "Manual intervention required",
                "typeid": "T02"
            },
        ]

        try:
            self.stdout.write("Initiating TaskType")
            for tasktypeitem in tasktype:
                TaskType.objects.create(
                    name=tasktypeitem['name'],
                    enabled=tasktypeitem['enabled'],
                    description=tasktypeitem['description'],
                    typeid=tasktypeitem['typeid']
                )
        except Exception:
            raise CommandError("TaskType table could not be updated!")

    def populate_taskvarcategory(self):
        taskvarcategory = [
            {
                "name": "INPUT",
                "enabled": "1",
                "description": "Input varables"
            },
            {
                "name": "OUTPUT",
                "enabled": "1",
                "description": "Output variables"
            },
        ]

        try:
            self.stdout.write("Initiating TaskVarCategory")
            for taskvarcategoryitem in taskvarcategory:
                TaskVarCategory.objects.create(
                    name=taskvarcategoryitem['name'],
                    enabled=taskvarcategoryitem['enabled'],
                    description=taskvarcategoryitem['description'],
                )
        except Exception:
            raise CommandError("TaskVarCategory table could not be updated!")

    def populate_taskvartype(self):
        taskvartype = [
            {
                "name": "String",
                "enabled": "1",
                "description": "String type variable"
            },
            {
                "name": "Integer",
                "enabled": "1",
                "description": "Integer type variable"
            },
            {
                "name": "Boolean",
                "enabled": "1",
                "description": "Boolean type variable"
            },
            {
                "name": "File",
                "enabled": "1",
                "description": "Provide the file as an evidence record. It will get the attachment from the referred"
                               " evidence."
            },
            {
                "name": "List",
                "enabled": "1",
                "description": "List of types separated by commas"
            },
        ]

        try:
            self.stdout.write("Initiating TaskVarType")
            for taskvartypeitem in taskvartype:
                TaskVarType.objects.create(
                    name=taskvartypeitem['name'],
                    enabled=taskvartypeitem['enabled'],
                    description=taskvartypeitem['description'],
                )
        except Exception:
            raise CommandError("TaskVarType table could not be updated!")

    def populate_action(self):
        # from django.core.files import File

        actions = [
            {
                "enabled": "1",
                "user": User.objects.get(pk=1),
                "title": "Hello World CMD",
                "version": "1",
                "automationid": None,
                # "scriptoutput": ScriptOutput.objects.get(pk=1),
                # "scriptoutputtype": EvidenceAttrFormat.objects.get(pk=1),
                # "scriptinput": ScriptInput.objects.get(pk=1),
                # "scriptinputattrtype": EvidenceAttrFormat.objects.get(pk=1),
                # "runonsaveattr" : False,
                # "scriptinputattrtypeall": False,
                # "outputtarget": OutputTarget.objects.get(pk=1),
                # "outputdescformat": EvidenceFormat.objects.get(pk=1),
                # "argument": None,
                # "connectionitemid": None,
                # "timeout": "300",
                # "fileName": "",
                # "fileRef": None,
                "created_by": "admin",
                "modified_by": "admin",
                "description": None,

                # "code": r"""
# echo "Hello World"
# sleep 2 &
#                                 """,
#                 "description": "<p>Prints a hello world</p>",
#                 "script_type": ScriptType.objects.get(pk=2),
#                 "script_category": ScriptCategory.objects.get(pk=1),
#                 "type": Type.objects.get(pk=1),
#                 "code_file": "0",
#                 "code_file_path": path.join(PROJECT_ROOT,"/tasks/scripts/2/2_2019-01-20_21-11-28"),
#                 "code_file_name": "2_2019-01-20_21-11-28",



            },
        ]

        try:
            self.stdout.write("Initiating Action tables")
            for actionitem in actions:
                # m=Action.objects.create(
                m = Action.objects.create(
                    enabled=actionitem['enabled'],
                    user=actionitem['user'],
                    title=actionitem['title'],
                    version=actionitem['version'],
                    automationid=actionitem['automationid'],
                    # code=actionitem['code'],
                    description=actionitem['description'],
                    # script_type=actionitem['script_type'],
                    # script_category=actionitem['script_category'],
                    # type=actionitem['type'],
                    # code_file=actionitem['code_file'],
                    # code_file_path=actionitem['code_file_path'],
                    # code_file_name=actionitem['code_file_name'],
                    # fileName=actionitem['fileName'],
                    # timeout=actionitem['timeout'],
                    # argument=actionitem['argument'],
                    created_by=actionitem['created_by'],
                    modified_by=actionitem['modified_by']
                )
                m.save()  # this creates the scripts in the folders
                # This line below will be useful to define builtin script locations...otherwise the model pk=None if
                # called from here
                # Action.objects.filter(pk=m.pk).update(code_file_name=actionitem['code_file_name'])
        except Exception:
            raise CommandError("Action table could not be updated!")

    def populate_actionqstatus(self):
        actionqstatus = [
            {
                "name": "Started",
                "enabled": "1",
                "description": "Started Action"
            },
            {
                "name": "Finished",
                "enabled": "1",
                "description": "Finished Action"
            },
        ]
        try:
            self.stdout.write("Initiating ActionQStatus")
            for actstatitem in actionqstatus:
                ActionQStatus.objects.create(
                    name=actstatitem['name'],
                    enabled=actstatitem['enabled'],
                    description=actstatitem['description']
                )
        except Exception:
            raise CommandError("InvStatus table could not be updated!")

    def populate_automation(self):
        automation = [
            {
                "enabled": "1",
                "user": User.objects.get(pk=1),
                "type": Type.objects.get(pk=3),
                "name": "test",
                "version": "1.0",
                "script_type": ScriptType.objects.first(),
                "script_category": ScriptCategory.objects.first(),
                "code": "print(\"whoami\")",
                "autorequirements": None,
                "description": "Test automation",
            },
        ]
        try:
            self.stdout.write("Initiating Automation")
            for automationitem in automation:
                Automation.objects.create(
                    enabled=automationitem['enabled'],
                    user=automationitem['user'],
                    type=automationitem['type'],
                    name=automationitem['name'],
                    version=automationitem['version'],
                    script_type=automationitem['script_type'],
                    script_category=automationitem['script_category'],
                    code=automationitem['code'],
                    autorequirements=automationitem['autorequirements'],
                    description=automationitem['description']
                )
        except Exception:
            raise CommandError("InvStatus table could not be updated!")

    def populate_settingscategory(self):
        settingscategory = [
            {
                "user": None,
                "categoryname": "Generic",
                "enabled": "1",
                "description": ""
            },
            {
                "user": None,
                "categoryname": "Exclude",
                "enabled": "1",
                "description": ""
            },
        ]
        try:
            self.stdout.write("Initiating SettingsCategory")
            for settingscategoryitem in settingscategory:
                SettingsCategory.objects.create(
                    user=settingscategoryitem['user'],
                    categoryname=settingscategoryitem['categoryname'],
                    enabled=settingscategoryitem['enabled'],
                    description=settingscategoryitem['description']
                )
        except Exception:
            raise CommandError("SettingsCategory table could not be updated!")


    def populate_settingsuser(self):
        settingsuser = [
            {
                "user": User.objects.first(),
                "settingname": "GUITheme",
                "settingvalue": None,
                "settingcategory": SettingsCategory.objects.get(pk=1),
                "enabled": "1",
                "description": "Default GUI Theme"
            },
        ]
        try:
            self.stdout.write("Initiating SettingsUser")
            for settingsuseritem in settingsuser:
                SettingsUser.objects.create(
                    user=settingsuseritem['user'],
                    settingname=settingsuseritem['settingname'],
                    settingvalue=settingsuseritem['settingvalue'],
                    settingcategory=settingsuseritem['settingcategory'],
                    enabled=settingsuseritem['enabled'],
                    description=settingsuseritem['description']
                )
        except Exception:
            raise CommandError("SettingsUser table could not be updated!")

    def populate_settingssystem(self):
        settingssystem = [
            {
                "user": None,
                "settingname": "excl.attr.alreadyseen",
                "settingvalue": "d41d8cd98f00b204e9800998ecf8427e",
                "settingcategory": SettingsCategory.objects.get(pk=2),
                "enabled": "1",
                "description": "Known good hash"
            },
            {
                "user": None,
                "settingname": "excl.attr.alreadyseen",
                "settingvalue": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
                "settingcategory": SettingsCategory.objects.get(pk=2),
                "enabled": "1",
                "description": "Known good hash"
            },
            {
                "user": None,
                "settingname": "excl.attr.alreadyseen",
                "settingvalue": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "settingcategory": SettingsCategory.objects.get(pk=2),
                "enabled": "1",
                "description": "Known good hash"
            },
        ]
        try:
            self.stdout.write("Initiating SettingsSystem")
            for settingssystemitem in settingssystem:
                SettingsSystem.objects.create(
                    user=settingssystemitem['user'],
                    settingname=settingssystemitem['settingname'],
                    settingvalue=settingssystemitem['settingvalue'],
                    settingcategory=settingssystemitem['settingcategory'],
                    enabled=settingssystemitem['enabled'],
                    description=settingssystemitem['description']
                )
        except Exception:
            raise CommandError("SettingsSystem table could not be updated!")

    def populate_KnowledgeBaseFormat(self):
        knowledgebaseformat = [
            {
                "name": "RAW",
                "enabled": "1",
                "description": "RAW type of evidence"
            },
            {
                "name": "TinyMCE",
                "enabled": "1",
                "description": "TinyMCE rich text/html"
            },
        ]
        try:
            self.stdout.write("Initiating KnowledgeBaseFormat")
            for kbformatitem in knowledgebaseformat:
                KnowledgeBaseFormat.objects.create(
                    name=kbformatitem['name'],
                    enabled=kbformatitem['enabled'],
                    description=kbformatitem['description']
                )
        except Exception:
            raise CommandError("KnowledgeBaseFormat table could not be updated!")

    def populate_KnowledgeBase(self):
        knowledgebase = [
            {
                "builtin": "1",
                "enabled": "1",
                "description": "First KnowledgeBase item - you can replace this!",
                "kbformat": KnowledgeBaseFormat.objects.get(pk=1),
                "title": "First KB Item!"
            },
        ]
        try:
            self.stdout.write("Initiating KnowledgeBase")
            for kbitem in knowledgebase:
                KnowledgeBase.objects.create(
                    builtin=kbitem['builtin'],
                    enabled=kbitem['enabled'],
                    description=kbitem['description'],
                    kbformat=kbitem['kbformat'],
                    title=kbitem['title'],
                )
        except Exception:
            raise CommandError("KnowledgeBase table could not be updated!")

    def populate_mitreattck_tactics(self):
        mitretactics = [
            {
                "matacid": "NA",
                "name": "NA",
                "enabled": "1",
                "description": "NA"
            },
            {
                "matacid": "TA0001",
                "name": "Initial Access",
                "enabled": "1",
                "description": "The initial access tactic represents the vectors adversaries use to gain an initial "
                               "foothold within a network."
            },
            {
                "matacid": "TA0002",
                "name": "Execution",
                "enabled": "1",
                "description": "The execution tactic represents techniques that result in execution of "
                               "adversary-controlled code on a local or remote system. This tactic is often used in "
                               "conjunction with initial access as the means of executing code once access is obtained"
                               ", and lateral movement to expand access to remote systems on a network."
            },
            {
                "matacid": "TA0003",
                "name": "Persistence",
                "enabled": "1",
                "description": "Persistence is any access, action, or configuration change to a system that gives an"
                               " adversary a persistent presence on that system. Adversaries will often need to "
                               "maintain access to systems through interruptions such as system restarts, loss of "
                               "credentials, or other failures that would require a remote access tool to restart or "
                               "alternate backdoor for them to regain access."
            },
            {
                "matacid": "TA0004",
                "name": "Privilege Escalation",
                "enabled": "1",
                "description": "Privilege escalation is the result of actions that allows an adversary to obtain a "
                               "higher level of permissions on a system or network. Certain tools or actions require "
                               "a higher level of privilege to work and are likely necessary at many points throughout"
                               " an operation. Adversaries can enter a system with unprivileged access and must take"
                               " advantage of a system weakness to obtain local administrator or SYSTEM/root level "
                               "privileges. A user account with administrator-like access can also be used. User "
                               "accounts with permissions to access specific systems or perform specific functions "
                               "necessary for adversaries to achieve their objective may also be considered an "
                               "escalation of privilege."
            },
            {
                "matacid": "TA0005",
                "name": "Defense Evasion",
                "enabled": "1",
                "description": "Defense evasion consists of techniques an adversary may use to evade detection or "
                               "avoid other defenses. Sometimes these actions are the same as or variations of "
                               "techniques in other categories that have the added benefit of subverting a particular "
                               "defense or mitigation. Defense evasion may be considered a set of attributes the "
                               "adversary applies to all other phases of the operation."
            },
            {
                "matacid": "TA0006",
                "name": "Credential Access",
                "enabled": "1",
                "description": "Credential access represents techniques resulting in access to or control over "
                               "system, domain, or service credentials that are used within an enterprise environment."
                               " Adversaries will likely attempt to obtain legitimate credentials from users or "
                               "administrator accounts (local system administrator or domain users with administrator"
                               " access) to use within the network. This allows the adversary to assume the identity"
                               " of the account, with all of that account's permissions on the system and network, "
                               "and makes it harder for defenders to detect the adversary. With sufficient access "
                               "within a network, an adversary can create accounts for later use within the "
                               "environment."
            },
            {
                "matacid": "TA0007",
                "name": "Discovery",
                "enabled": "1",
                "description": "Discovery consists of techniques that allow the adversary to gain knowledge about"
                               " the system and internal network. When adversaries gain access to a new system, "
                               "they must orient themselves to what they now have control of and what benefits "
                               "operating from that system give to their current objective or overall goals during "
                               "the intrusion. The operating system provides many native tools that aid in this "
                               "post-compromise information-gathering phase."
            },
            {
                "matacid": "TA0008",
                "name": "Lateral Movement",
                "enabled": "1",
                "description": "Lateral movement consists of techniques that enable an adversary to access and "
                               "control remote systems on a network and could, but does not necessarily, include "
                               "execution of tools on remote systems. The lateral movement techniques could allow "
                               "an adversary to gather information from a system without needing additional tools,"
                               " such as a remote access tool."
            },
            {
                "matacid": "TA0009",
                "name": "Collection",
                "enabled": "1",
                "description": "Collection consists of techniques used to identify and gather information, such as"
                               " sensitive files, from a target network prior to exfiltration. This category also "
                               "covers locations on a system or network where the adversary may look for information"
                               " to exfiltrate."
            },
            {
                "matacid": "TA0010",
                "name": "Exfiltration",
                "enabled": "1",
                "description": "Exfiltration refers to techniques and attributes that result or aid in the adversary"
                               " removing files and information from a target network. This category also covers "
                               "locations on a system or network where the adversary may look for information to "
                               "exfiltrate."
            },
            {
                "matacid": "TA0011",
                "name": "Command and Control",
                "enabled": "1",
                "description": "The command and control tactic represents how adversaries communicate with systems "
                               "under their control within a target network. There are many ways an adversary can "
                               "establish command and control with various levels of covertness, depending on system"
                               " configuration and network topology. Due to the wide degree of variation available "
                               "to the adversary at the network level, only the most common factors were used to "
                               "describe the differences in command and control. There are still a great many specific"
                               " techniques within the documented methods, largely due to how easy it is to define"
                               " new protocols and use existing, legitimate protocols and network services for"
                               " communication. The resulting breakdown should help convey the concept that detecting"
                               " intrusion through command and control protocols without prior knowledge is a "
                               "difficult proposition over the long term. Adversaries' main constraints in "
                               "network-level defense avoidance are testing and deployment of tools to rapidly "
                               "change their protocols, awareness of existing defensive technologies, and access "
                               "to legitimate Web services that, when used appropriately, make their tools difficult "
                               "to distinguish from benign traffic."
            },
            {
                "matacid": "TA0040",
                "name": "Impact",
                "enabled": "1",
                "description": "The Impact tactic represents techniques whose primary objective directly reduces the "
                               "availability or integrity of a system, service, or network; including manipulation of"
                               " data to impact a business or operational process. These techniques may represent an "
                               "adversary's end goal, or provide cover for a breach of confidentiality."
            },
        ]
        try:
            self.stdout.write("Initiating MitreAttck_Tactics")
            for mitretacticsitem in mitretactics:
                MitreAttck_Tactics.objects.create(
                    matacid=mitretacticsitem['matacid'],
                    name=mitretacticsitem['name'],
                    enabled=mitretacticsitem['enabled'],
                    description=mitretacticsitem['description']
                )
        except Exception:
            raise CommandError("MitreAttck_Tactics table could not be updated!")


    def populate_mitreattck_techniques(self):
        mitretechniques = [
            {
                "matacref": "",
                "matecid": "",
                "name": "",
                "enabled": "1",
                "description": ""
            },
        ]
        try:
            self.stdout.write("Initiating MitreAttck_Techniques")
            for mitretechniquesitem in mitretechniques:
                MitreAttck_Techniques.objects.create(
                    matacref=mitretechniquesitem['matacref'],
                    matecid=mitretechniquesitem['matecid'],
                    name=mitretechniquesitem['name'],
                    enabled=mitretechniquesitem['enabled'],
                    description=mitretechniquesitem['description']
                )
        except Exception:
            raise CommandError("MitreAttck_Techniques table could not be updated!")
