# Balazs's Computer Incident Response Tool (bCIRT)

## What is it?
This is an incident response team case management "tool", that can be utilized to automate the response procedures and keep record of the performed actions.
It will be integrated with external tools via scripts and APIs.

## What is it not?
It is not a SIEM or a log management tool. It's purpose is not to collect logs from other systems, however I plan integration with SIEM tools.
It is not a helpdesk system either, there are cool solutions out there.

## Screenshots
See them at the bottom of this page or in the bCIRT_Screenshots folder.

## License
I provide this tool for free of charge for ANYONE who needs it.\
I will NOT restrict it, because I want everyone to benefit from it who wants.
Of course if you find this tool useful and make a billion dollar business out of it please think about me and invite me for a lunch or so:)\
It is using multiple third-party tools/scripts that I found awesome!!! Please think about those people also when using this tool, I'll provide a detailed list with licenses for each on this page.\
I never wanted to misuse a license or a tool, so if you notice that I am not following an of the licenses as much as possible, please let me know and I'll try to fix it.\
All external tools/ideas integrated into this I find brilliant and **THANK YOU**!!!

## Distribution
It is primarily a package of Python Django scripts, but I plan to provide either a Virtual Machine or a script that installs the necessary tools to support easy deployment and a demo environment.
I will share the code as I develop it.

## Warning
Although it is about information security, the tool is heavily leveraging Django's security features and nothing is perfect. For this reason I recommend securig the tool and it's environment as much as possible.\
I am NOT a developer, I am far away from being one! So this code is probably not the most effective, "ugly", "bad". If you wish to educate me, you are more than welcome, I appreciate any advice.
This is a tool in development, not intended for production use. It will likely not lose any data, but anyways, use it at your own risk!
Don't install this on a server where the users of it should not have admin access, as the current controls allow easy takeover of the host server (via script executions). This will be managed later, right now I don't have issue with being admin of the server.

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
* Potentially internationalize the strings

## Issue/Bug tracking and TODO/NEXT list:
1. integrate MITRE/ATTACK framework
2. create indicators like url, file, hash etc for evidences
3. remove buttons based on permissions and fix any potential permission issues - not tested in detail yet
4. enable command history/logging
5. concurrent edit of records in two browsers/windows - latest wins
6. builtin scripts/task templates etc
7. field validation for future indicators
8. GET/POST request additional value validation on the server side
9. workflow controls, like don't allow to close an investigation with open tasks
10. a few more fixes

## Documentation
https://bcirt.readthedocs.io/en/latest/

## Docker version
1. Clone the repo: git clone https://github.com/bl305/bCIRT
2. Install docker and docker-compose in your host
3. If you want your own certificates for prod, put them in the ./bCIRT/osbuilds/certs in the proper directory
4. If you want to generate new certificates (you should), use the script ./bCIRT/osbuilds/certs/certgen.sh after 
setting the  proper values in the certconf* files.  
3. Make sure you are in the bCIRT root
4. To build development accessible on "http://127.0.0.1:8000": 
./mydocker_build_docker_dev_postgre.sh
5. To build production accessible on "https://127.0.0.1:443":
 ./mydocker_build_Ubuntu_bionic1804_apache2_postgre.sh
6. Default credentials are set in the "docker-compose*" files: 'admin'/'Password1.' 

## Install guide for demo-ing
Key steps to get going:
1. Download the source code
2. Install virtual envrionment
3. Install Django and install supporting python dependency packages
4. Change defaults
5. Init database
6. Start django

### 1. download sourcecode
Click on the download icon and save the zip file somewhere.

### 2. install virtual environment (Linux)
Go to a directory where you would like to have your virtual environment and create a standar python virtual env, like:
Follow this for more details: https://packaging.python.org/guides/installing-using-pip-and-virtualenv/
Basically, run:
```python
python3 -m virtualenv env
source env/bin/activate
```

### 3. Install Django and other python packages
Go to the virtual environment by activating it, then:
```python
pip install django
```
The next will install a bunch of dependencies and you might need to do some additional stuff to get weasyprint run, then go to https://weasyprint.readthedocs.io/en/stable/install.html
```python
pip install django-weasyprint cairocffi django-bootstrap-4 django-tinymce4-lite misaka import-export
```
### 4. Change default values
Go to the bCIRT/settings.py and change the followings:
```text
DEBUG = "FALSE"
BASE_URL = "http://127.0.0.1:8000"
ALLOWED_HOSTS = ['127.0.0.1']
INTERNAL_IPS = ['127.0.0.1']

```
Go to the bCIRT/custom_variables.py and change:
```text
ALLOWED_HOSTS = ['127.0.0.1']

Optionally also modify:
BCIRT_PATH
BCIRT_MEDIA_ROOT
MYDB

```

### 5. Init database
To init the database with default values, run this command:
```python
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
#follow steps
python3 manage.py initdb --all
```
Tables can be added by applications, using the
 ```python
 python3 manage.py initdb -i appname
 ```
### 6. Start Django
Simply run in the virtual env:
```python
python3 manage.py runserver
```

## Used tools, modules, respect to the developers!
Any coding I did not following best practices is my fault, don't blame any of the tools which I might not use properly:)

First of all I used this website a lot, a LOT, many thanks: https://simpleisbetterthancomplex.com/
Favourite editors for home users: https://www.jetbrains.com/pycharm/, https://atom.io/

Tools integrated in the bCIRT:
bootstrap (MIT): https://getbootstrap.com/  
bootstrap table (MIT): https://github.com/wenzhixin/bootstrap-table  
bootstrap-datepicker (Apache 2.0): https://github.com/uxsolutions/bootstrap-datepicker  
bootstrap-select (MIT): https://github.com/snapappointments/bootstrap-select  
Fontawesome (Free/Open source GPL friendly): https://github.com/FortAwesome/Font-Awesome  
jquery (MIT): https://jquery.com  
jquery UI (MIT): https://jqueryui.com  
django-bootstrap-4 (BSD-3-Clause): https://github.com/zostera/django-bootstrap4  
django-tinymce4-lite (MIT): https://github.com/romanvm/django-tinymce4-lite  
misaka (MIT): https://pypi.org/project/misaka  
weasyprint (BSD): https://weasyprint.org PyPI: https://pypi.org/project/WeasyPrint  

### Screenshots
![Pic1](https://github.com/bl305/bCIRT/raw/master/bCIRT_Screenshots/01_bCIRT_login.png)
![Pic1](https://github.com/bl305/bCIRT/raw/master/bCIRT_Screenshots/01_bCIRT_login.png)
![Pic2](https://github.com/bl305/bCIRT/raw/master/bCIRT_Screenshots/02_bCIRT_index.png)
![Pic3](https://github.com/bl305/bCIRT/raw/master/bCIRT_Screenshots/03_bCIRT_investigation_details.png)
![Pic4](https://github.com/bl305/bCIRT/raw/master/bCIRT_Screenshots/04_bCIRT_tasks.png)
![Pic5](https://github.com/bl305/bCIRT/raw/master/bCIRT_Screenshots/05_bCIRT_evidences.png)
![Pic6](https://github.com/bl305/bCIRT/raw/master/bCIRT_Screenshots/06_bCIRT_actions.png)
![Pic7](https://github.com/bl305/bCIRT/raw/master/bCIRT_Screenshots/07_bCIRT_automation.png)
