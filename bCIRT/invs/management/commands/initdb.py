from django.core.management.base import BaseCommand, CommandError
from invs.models import InvStatus, InvPriority, InvCategory, InvPhase, InvSeverity
from tasks.models import TaskVarType, TaskVarCategory, TaskType, TaskCategory, TaskStatus, TaskPriority
from tasks.models import ScriptOs, ScriptType, ScriptCategory, Action, Type, ActionQStatus, OutputTarget, ScriptOutput
from tasks.models import EvidenceFormat, EvidenceAttrFormat
from bCIRT.settings import PROJECT_ROOT
from os import path
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
        super(Command, self).__init__(*args, **kwargs)
        pass

    def handle(self, *args, **options):
        # def handle(self, *args, **kwargs):
        p_all = options['all']
        p_clear = options['clear']
        p_table = options['table_name']
        if p_all:
            self.populate_evidenceformat()
            self.populate_evidenceattrformat()

            self.populate_invseverity()
            self.populate_invstatus()
            self.populate_invcategory()
            self.populate_invphase()
            self.populate_invpriority()

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
            self.populate_actoutputtarget()
            self.populate_acttype()
            self.populate_actionqstatus()
            self.populate_action()
        elif p_clear:
            print("clear")
        elif p_table:
            if p_table == "investigations":
                self.populate_invseverity()
                self.populate_invstatus()
                self.populate_invcategory()
                self.populate_invphase()
                self.populate_invpriority()
            elif p_table == "evidences":
                self.populate_evidenceformat()
                self.populate_evidenceattrformat()
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
                self.populate_actoutputtarget()
                self.populate_acttype()
                self.populate_actionqstatus()
                self.populate_action()
            else:
                print("Wrong parameter! Options:\ninvestigations / tasks / taskvars / actions / evidences\n")
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
        except:
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
        ]
        try:
            self.stdout.write("Initiating EvidenceAttrFormat")
            for evattrformatitem in evidenceattrformat:
                EvidenceAttrFormat.objects.create(
                    name=evattrformatitem['name'],
                    enabled=evattrformatitem['enabled'],
                    description=evattrformatitem['description']
                )
        except:
            raise CommandError("EvidenceAttrFormat table could not be updated!")

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
            }
        ]
        try:
            self.stdout.write("Initiating InvStatus")
            for invstatitem in invstatus:
                InvStatus.objects.create(
                    name=invstatitem['name'],
                    enabled=invstatitem['enabled'],
                    description=invstatitem['description']
                )
        except:
            raise CommandError("InvStatus table could not be updated!")

    def populate_invseverity(self):
        invseverity = [
            {
                "name": "S0 Baseline",
                "enabled": "1",
                "description": "S0 Baseline"
            },
            {
                "name": "S1 Low",
                "enabled": "1",
                "description": "S1 Low"
            },
            {
                "name": "S2 Medium",
                "enabled": "1",
                "description": "S2 Medium"
            },
            {
                "name": "S3 High",
                "enabled": "1",
                "description": "S3 High"
            },
            {
                "name": "S4 Severe",
                "enabled": "1",
                "description": "S4 Severe"
            },
            {
                "name": "S5 Emergency",
                "enabled": "1",
                "description": "S5 Emergency"
            },
        ]

        try:
            self.stdout.write("Initiating InvSeverity")
            for invsevitem in invseverity:
                InvSeverity.objects.create(
                    name=invsevitem['name'],
                    enabled=invsevitem['enabled'],
                    description=invsevitem['description']
                )
        except:
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
        except:
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
        except:
            raise CommandError("InvPhase table could not be updated!")

    def populate_invcategory(self):
        invcategory = [
            {
                "name": "Exercise/Network Defense Testing",
                "enabled": "1",
                "reporting_timeframe": "Not Applicable; this category is for each agency's internal use during exercises.",
                "catid": "CAT 0",
                "description": "This category is used during state, federal, national, international exercises and approved activity testing of internal/external network defenses or responses."
            },
            {
                "name": "Unauthorized Access",
                "enabled": "1",
                "reporting_timeframe": "Within one (1) hour of discovery/detection.",
                "catid": "CAT 1",
                "description": "In this category an individual gains logical or physical access without permission to a federal agency network, system, application, data, or other resource"
            },
            {
                "name": "Denial of Service (DoS)",
                "enabled": "1",
                "reporting_timeframe": "Within two (2) hours of discovery/detection if the successful attack is still ongoing and the agency is unable to successfully mitigate activity.",
                "catid": "CAT 2",
                "description": "An attack that successfully prevents or impairs the normal authorized functionality of networks, systems or applications by exhausting resources. This activity includes being the victim or participating in the DoS."
            },
            {
                "name": "Malicious Code",
                "enabled": "1",
                "reporting_timeframe": "Daily \nNote: Within one (1) hour of discovery/detection if widespread across agency.",
                "catid": "CAT 3",
                "description": "Successful installation of malicious software (e.g., virus, worm, Trojan horse, or other code-based malicious entity) that infects an operating system or application. Agencies are NOT required to report malicious logic that has been successfully quarantined by antivirus (AV) software."
            },
            {
                "name": "Improper Usage",
                "enabled": "1",
                "reporting_timeframe": "Monthly\nNote: If system is classified, report within one (1) hour of discovery.",
                "catid": "CAT 4",
                "description": "This category includes any activity that seeks to access or identify a federal agency computer, open ports, protocols, service, or any combination for later exploit. This activity does not directly result in a compromise or denial of service."
            },
            {
                "name": "Investigation",
                "enabled": "1",
                "reporting_timeframe": "Not Applicable; this category is for each agency's use to categorize a potential incident that is currently being investigated.",
                "catid": "CAT 6",
                "description": "Unconfirmed incidents that are potentially malicious or anomalous activity deemed by the reporting entity to warrant further review."
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
        except:
            raise CommandError("InvCategory table could not be updated!")

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
        except:
            raise CommandError("ActionScriptOs table could not be updated!")

    def populate_actscriptcategory(self):
        actscriptcategory = [
            {
                "name": "Generic",
                "enabled": "1",
                "description": "Generic script",
            },
            {
                "name": "FileBased",
                "enabled": "1",
                "description": "Performs actions based on the files in the evidence",
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
        except:
            raise CommandError("ActionScriptCategory table could not be updated!")

    def populate_actscripttype(self):
        actscripttype = [
            {
                "name": "Python",
                "enabled": "1",
                "description": "Runs on all Linux with compatible Python",
                "version": "3.6",
                "os": ScriptOs.objects.get(pk=2),
                "interpreter": "/usr/bin/python3"
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
        except:
            raise CommandError("ActionScriptType table could not be updated!")

    def populate_actoutputtarget(self):
        actoutputtarget = [
            {
                "name": "Description",
                "enabled": "1",
                "description": "Output goes to the description field.",
            },
            {
                "name": "Attribute",
                "enabled": "1",
                "description": "Output goes to the attribute field.",
            },
            {
                "name": "File",
                "enabled": "1",
                "description": "Output goes to the file attachment.",
            },
            {
                "name": "DropIt",
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
        except:
            raise CommandError("ActionOutputTarget table could not be updated!")

    def populate_actscriptoutput(self):
        actscriptoutput = [
            {
                "name": "Default",
                "enabled": "1",
                "description": "Use output as it is",
            },
            {
                "name": "CSV",
                "enabled": "1",
                "description": "Comma separated values",
            },
            {
                "name": "Line-by-Line",
                "enabled": "1",
                "description": "Newline separated values",
            },
        ]
        try:
            self.stdout.write("Initiating ActScriptOutput")
            for actscriptoutputitem in actscriptoutput:
                ScriptOutput.objects.create(
                    name=actscriptoutputitem['name'],
                    enabled=actscriptoutputitem['enabled'],
                    description=actscriptoutputitem['description'],
                )
        except:
            raise CommandError("ActionScriptOutput table could not be updated!")

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
        ]
        try:
            self.stdout.write("Initiating ActType")
            for acttypeitem in acttype:
                Type.objects.create(
                    name=acttypeitem['name'],
                    enabled=acttypeitem['enabled'],
                    description=acttypeitem['description'],
                )
        except:
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
        except:
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
        except:
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
        ]

        try:
            self.stdout.write("Initiating TaskStatus")
            for taskstatusitem in taskstatus:
                TaskStatus.objects.create(
                    name=taskstatusitem['name'],
                    enabled=taskstatusitem['enabled'],
                    description=taskstatusitem['description'],
                )
        except:
            raise CommandError("TaskStatus table could not be updated!")

    def populate_tasktype(self):
        tasktype = [
            {
                "name": "Automated Task",
                "enabled": "1",
                "description": "Sample automated task",
                "typeid": "T01"
            },
            {
                "name": "Manual task",
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
        except:
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
        except:
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
                "description": "Provide the file as an evidence record. It will get the attachment from the referred evidence."
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
        except:
            raise CommandError("TaskVarType table could not be updated!")

    def populate_action(self):
        from django.core.files import File

        actions = [
            {
                "title": "Hello World CMD",
                "code": r"""
echo "Hello World"
sleep 2 &                
                                """,
                "description": "<p>Prints a hello world</p>",
                "script_type": ScriptType.objects.get(pk=2),
                "script_category": ScriptCategory.objects.get(pk=1),
                "user": User.objects.get(pk=1),
                "version": "1",
                "enabled": "1",
                "type": Type.objects.get(pk=1),
                "code_file": "0",
                "code_file_path": path.join(PROJECT_ROOT,"/tasks/scripts/2/2_2019-01-20_21-11-28"),
                "code_file_name": "2_2019-01-20_21-11-28",
                "fileName": "",
                "timeout": "300",
                "argument": "",
                "created_by": "admin",
                "modified_by": "admin"
            },
        ]

        try:
            self.stdout.write("Initiating Action tables")
            for actionitem in actions:
                # m=Action.objects.create(
                m = Action.objects.create(
                    title=actionitem['title'],
                    code=actionitem['code'],
                    description=actionitem['description'],
                    script_type=actionitem['script_type'],
                    script_category=actionitem['script_category'],
                    user=actionitem['user'],
                    version=actionitem['version'],
                    enabled=actionitem['enabled'],
                    type=actionitem['type'],
                    code_file=actionitem['code_file'],
                    code_file_path=actionitem['code_file_path'],
                    code_file_name=actionitem['code_file_name'],
                    fileName=actionitem['fileName'],
                    timeout=actionitem['timeout'],
                    argument=actionitem['argument'],
                    created_by=actionitem['created_by'],
                    modified_by=actionitem['modified_by']
                )
                m.save()  #  this creates the scripts in the folders
                # This line below will be useful to define builtin script locations...otherwise the model pk=None if
                # called from here
                # Action.objects.filter(pk=m.pk).update(code_file_name=actionitem['code_file_name'])
        except:
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
        except:
            raise CommandError("InvStatus table could not be updated!")
