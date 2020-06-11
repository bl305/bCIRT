****************************
Installation as a web server
****************************


Ubuntu 18.04 Apache2, Postgresql, Python 3.x
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

bCIRT runs on almost any standard linux distro, let's start with Ubuntu 18.04 Bionic server.
Get Ubuntu from `Ubuntu home <https://ubuntu.com/#download>`_.

Always start with updating the operating system to the latest
supported version::

    sudo apt-get update
    sudo apt-get upgrade -y

This prepares your OS for the detailed installation.

Download the bCIRT package
--------------------------

First of all, download the latest package using wget for example from github:
https://github.com/bl305/bCIRT/tree/master/bCIRT_PackageReleases

For the sake of simplicity, I'll move all related stuff to the /bcirt directory. This can be replaced if you wish to
put the things somewhere else, but it will show you how to do it.
Create the base directory structure::

    sudo mkdir -p /bcirt/releases
    sudo mkdir -p /bcirt/venv
    sudo mkdir -p /bcirt/var/www/


Download example for v202::

    wget https://github.com/bl305/bCIRT/raw/master/bCIRT_PackageReleases/0112_bCIRT_v202_20200310.zip

Unzip it with your tool, move it to the destination::

    cd /bcirt/releases
    unzip 0112_bCIRT_v202_20200310.zip
    mv /bcirt/releases/bCIRT /bcirt/var/www/

Install the virtual environment for Python
------------------------------------------

Go to a directory where you would like to have your virtual environment and create a standard python virtual env, like:
Follow this for more details: https://packaging.python.org/guides/installing-using-pip-and-virtualenv/

For this you will need the virtualenv package::

    sudo apt install python3-venv -y

Basically select your home directory and run::

    sudo mkdir -p /bcirt/venv
    #cd /bcirt/venv
    sudo python3 -m venv /bcirt/venv/bCIRT_venv

Install Django and other python packages
----------------------------------------

First you need to install some packages to be able to build the necessary tools::

    sudo apt install gcc binutils cpp python3 python3-dev -y

You will need root privilege to compile the necessary tools::

    sudo su

Go to the virtual environment by activating it::

    source /bcirt/venv/bCIRT_venv/bin/activate

This should look like this::

    (bCIRT_venv) root@bcirtu18:/#

Now install the necessary packages.
Depending on you approach, you might want to install all requirements from the requirements.txt::

    pip install -r requirements.txt

Other option is to manually install packages one-by-one, installing the key ones will pull the dependencies.
The below one is for Ubuntu, but you can simply use the requirements file and remove the version restrictions,
it should work most of the time::

    pip3 install beautifulsoup4 bootstrap4 cryptography Django django-bootstrap4 django-debug-toolbar \
    django-import-export django-misaka django-session-security django-tinymce4-lite misaka pydot pygal \
    python-magic pytz PyYAML tablib wheel

Customizing default values
--------------------------

First determine your hostname and IP::

    hostname
    ifconfig

**Considering my local server IP is: 192.168.101.237**

Go to the bCIRT/custom_params.py and modify it. Settings in this file will overwrite the settings.py values if set::

    nano /bcirt/var/www/bCIRT/bCIRT/custom_variables.py

Modify contents, make sure you generate your own keys and adjust IP address and path etc...::

    BCIRT_ALLOWED_HOSTS = ['192.168.101.237']
    BCIRT_PATH = '/bcirt/var/www/bCIRT'
    # Recommend SecurityNow! grc.com :)
    ENCRYPTION_KEY_1 = "qDqiih0JQgtr6ahdKR0yieQf59MtweBYJ7GbDIA9cWgWBh53cT8j0Zvr1hFsgup"
    # Should be a 16byte random string in base64 encoded format
    # use this site:
    # https://nitratine.net/blog/post/encryption-and-decryption-in-python/
    SALT_1 = b'Pr1YFcgFTIQMZERvJf0ySpUEiAniiiRS6NEOkcVbHLQ='
    PROJECTNAME = 'bCIRT'
    PROJECT_TITLE = 'bCIRT'
    LOGLEVEL = 0  # off
    # LOGLEVEL = 1 #minimum
    # LOGLEVEL = 2 #standard
    # LOGLEVEL = 3 #verbose
    LOGSEPARATOR = ";"

Go to the bCIRT/settings.py and edit it::

    nano /bcirt/var/www/bCIRT/bCIRT/settings.py

Change the followings::

    BASE_URL = "http://192.168.101.237:8000"
    ALLOWED_HOSTS = ['127.0.0.1', '192.168.101.237']
    DEBUG = False

Init the database
-----------------

To init the database with default values, run this command::

    cd cd /bcirt/var/www/bCIRT/
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py createsuperuser
    #answer the questions
    #Username: admin
    #Email address: admin@mydomain.com
    #Password:
    #Password (again):
    #Superuser created successfully.

At this point you should be seeing a new SQLITE database file called 'db.sqlite3'::

    ls

Let's initiate the database with the default values::

    #initiate the database  with the built-in values for severities etc RECOMMENDED!
    python3 manage.py initdb --all
    # Unique tables can be added by application name, using the
    #python3 manage.py initdb -i <appname>

Start Django debug/development environment
------------------------------------------
To test if the system is working correctly, simply run in the virtual env::

    python3 manage.py runserver

You should see something like this::

    (bCIRT_venv) bali@master:~/PycharmProjects/bCIRT> python3 manage.py runserver
    Watching for file changes with StatReloader
    [2020-03-10 21:02:19,742] autoreload: INFO - Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    March 10, 2020 - 21:02:20
    Django version 3.0.3, using settings 'bCIRT.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.




CentOS 8 Apache2, Postgresql, Python 3.x
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

bCIRT runs on the CentOS distribution.
Get CentOS from `CentOS home <https://www.centos.org/>`_.
Always start with updating the operating system to the latest
supported version::

    sudo dnf update -y

This prepares your OS for the detailed installation.

