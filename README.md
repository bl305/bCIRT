#Balazs's Computer Incident Response Tool (bCIRT)

## What is it?
This is an incident response team tool, that can be utilized to\
automate the response procedures and keep record of the performed\
actions.
It will be integrated it with external tools via scripts and APIs.

## What is it not?
It is not a SIEM or a log management tool. It's purpose is not to collect\
logs from other systems, however I plan integration with SIEM tools.
It is not a helpdesk system either, there are cool solutions out there.

## License
I provide this tool for free of charge for ANYONE who needs it.\
I will NOT restrict it, because I want everyone to benefit from it who wants.\
Of course if you find this tool useful and make a billion dollar business out of it\
please think about me and invite me for a lunch or so:)\
It is using multiple third-party tools/scripts that I found awesome!!!\
Please think about those people also when using this tool, I'll provide a detailed\
list with licenses for each on this page.\
I never wanted to misuse a license or a tool, so if you notice that I am not following\
an of the licenses as much as possible, please let me know and I'll try to fix it.\
All external tools/ideas integrated into this I find brilliant and **THANK YOU**!!!

## Distribution
It is primarily a package of Python Django scripts, but I plan to provide\
either a Virtual Machine or a script that installs the necessary tools\
to support easy deployment and a demo environment.
I will share the code as I develop it, 

## Warning
Although it is about information security, the tool is heavily leveraging\
Django's security features and nothing is perfect. For this reason I\
recommend securig the tool and it's environment as much as possible.
I am NOT a developer, I am far away from being one! So this code is probably\
not the most effective, "ugly", "bad". If you wish to educate me, you are\
more than welcome, I appreciate any advice.

## What is the driver of this project:
* learn the Python Django framework because it's cool
* develop a tool that I can customize as needed
* give back to the community by sharing the tool

## Long term goals for the tool:
* Case management
* Task management
* Automated and manual Script, command and tool execution
* Playbook creation
* Email notification
* External authentication (minimum Active Directory, maybe SAML)
* potentially internationalize the strings

## Issue/Bug tracking and TODO/NEXT list:
1. fix concurrency issues by atomizing database edits
2. integrate MITRE/ATTACK framework
3. upload screenshots and the first beta
