from os.path import join as path_join

MYALLOWED_HOSTS = ['192.168.56.101']

MYPATH = '/home/bali/PycharmProjects/bCIRT'

MYMEDIA_ROOT = path_join(MYPATH, 'media')

MYDB = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': path_join(MYPATH, 'db.sqlite3'),
    }
}

BASE = 'base.html'
BASE_THEME = 'dark'  # not in use yet
PROJECTNAME = 'bCIRT'
PROJECT_TITLE = 'bCIRT'
TIMEFORMAT = "Y/m/d H:i:s"
