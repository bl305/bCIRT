# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : bCIRT/settings.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Settings file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
"""
Django settings for bCIRT project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
# Custom parameters should dbe set in the following files instead of modifying this file:
# custom_variables.py
try:
    from bCIRT.custom_variables import MYDB
except Exception:
    MYDB = None
try:
    from bCIRT.custom_variables import MYPATH
except Exception:
    MYPATH = None
try:
    from bCIRT.custom_variables import MYALLOWED_HOSTS
except Exception:
    MYALLOWED_HOSTS = None
try:
    from bCIRT.custom_variables import LOGLEVEL
except Exception:
    LOGLEVEL = 0

# custom backup constants start
# PROJECT_ROOT = '/home/bali/PycharmProjects/bCIRT'
PROJECT_ROOT = None
if MYPATH is None:
    PROJECT_ROOT = '/var/www/html/bCIRT'
else:
    PROJECT_ROOT = MYPATH

MAXBYTES = 104857600  # 1024*1024*100, # 100MB
LFILENAME = 'logs.txt'
LOG_PATH = os.path.join(PROJECT_ROOT, 'log', LFILENAME)

DFILENAME = 'debug.txt'
DEBUGLOG_PATH = os.path.join(PROJECT_ROOT, 'log', DFILENAME)

BACKUPCOUNT = 5
# custom backup constants end

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
BASE_URL = "http://127.0.0.1:8000"

ANONYMOUS_USER_ID = -1


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'moyg9_u$c$gg=0y_ou557!w8kkq7z4ze4_ua*0(l*i(39%*c*p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']
if MYALLOWED_HOSTS is not None:
    for myhosts in MYALLOWED_HOSTS:
        ALLOWED_HOSTS.append(myhosts)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'session_security',
    'bootstrap4',
    'tinymce',
    'accounts',
    'configuration',
    'users',
    'invs',
    'tasks',
    'assets',
    'reports',
    'import_export',
]
IMPORT_EXPORT_USE_TRANSACTIONS = True


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bCIRT.urls'
SESSION_SECURITY_WARN_AFTER = 2700
SESSION_SECURITY_EXPIRE_AFTER = 3600
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
            'libraries': {
                         'field_type': 'invs.templatetags.field_type',
                         }
        },
    },
]

WSGI_APPLICATION = 'bCIRT.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = None
if not MYDB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = MYDB

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(module)s [PID:%(process)d] [%(name)s.%(funcName)s:%(lineno)d]'
                      ' %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console_simple': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file_simple': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            #            'class': 'logging.FileHandler',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': MAXBYTES,
            'backupCount': BACKUPCOUNT,
            'filename': LOG_PATH,
            'formatter': 'simple'
        },
        'console_verbose': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file_verbose': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['require_debug_true'],
            'maxBytes': MAXBYTES,
            'backupCount': BACKUPCOUNT,
            'filename': DEBUGLOG_PATH,
            'formatter': 'verbose'
        },
        # Send info messages to syslog
        # TBD
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local2',
            'address': '/dev/log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        # Enabling this will log all django logs
        # 'django': {
        #     'handlers': ['console_verbose', 'file_verbose'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
        'log_all_simple': {
            'handlers': ['console_simple', 'file_simple'],
            'level': 'WARNING',
            'propagate': True,
        },
        'log_all_verbose': {
            'handlers': ['console_verbose', 'file_verbose'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'log_file_simple': {
            'handlers': ['file_simple'],
            'level': 'WARNING',
            'propagate': True,
        },
        'log_file_verbose': {
            'handlers': ['file_verbose'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'log_console_simple': {
            'handlers': ['console_simple'],
            'level': 'WARNING',
            'propagate': True,
        },
        'log_console_verbose': {
            'handlers': ['console_verbose'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Logging sample
# import logging
# def sample_function(secret_parameter):
#     logger = logging.getLogger(__name__)  # __name__=projectA.moduleB
#     logger.debug("Going to perform magic with '%s'",  secret_parameter)
#
#     try:
#         result = do_magic(secret_parameter)
#     except IndexError:
#         logger.exception("OMG it happened again, someone please tell Laszlo")
#     except:
#         logger.info("Unexpected exception", exc_info=True)
#         raise
#     else:
#         logger.info("Magic with '%s' resulted in '%s'", secret_parameter, result, stack_info=True)

# this goes into the files that log
# import logging

# logger = logging.getLogger('log_all_verbose')
# loggerd = logging.getLogger('django')
# logger.debug("AAA DEBUG")
# logger.info("AAA INFO")
# logger.warn("AAA WARNING")
# logger.error("AAA ERROR")
# logger.critical("AAA CRITICAL")

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
# ADDED FOR PDF SUPPORT ONLY
STATIC_ROOT = '/'
# static root must be set to the full path, and calling "python3 manage.py collectstatic" to get the admin css
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "home"
INTERNAL_IPS = ['127.0.0.1']

# Session timeout
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# hard coded session close - this will expire regardless of activity
# SESSION_COOKIE_AGE = 5 * 60 #5 minutes
# SESSION_COOKIE_AGE = 60 * 60  # 1 hour
SESSION_SAVE_EVERY_REQUEST = True  # refresh session timeout
# TBD session timeout - it's only client side

# TinyMCE config
TINYMCE_DEFAULT_CONFIG = {
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': 'autoresize advlist autolink lists link image charmap print preview anchor searchreplace visualblocks'
               ' code fullscreen insertdatetime media table contextmenu paste codesample',
    'paste_data_images': True,
    'toolbar1': 'insertfile undo redo | styleselect | fontselect formatselect fontsizeselect bold italic underline'
                ' | alignleft aligncenter alignright alignjustify'
                '| bullist numlist outdent indent | table | link image | codesample | preview code',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'inline': False,
    'statusbar': True,
    #    'height': 300,
    #    'readonly': 1,
    'branding': False,
    'custom_undo_redo_levels': 20,
}


DIS_TINYMCE_DEFAULT_CONFIG = {
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': 'link image paste preview codesample contextmenu table code lists autoresize',
    'toolbar1': 'fontselect formatselect fontsizeselect bold italic underline | alignleft aligncenter alignright'
                ' alignjustify '
                '| bullist numlist | outdent indent | table | link image | codesample | preview code',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'inline': False,
    'statusbar': True,
    #    'height': 300,
    #    'readonly': 1,
    'branding': False,
    'custom_undo_redo_levels': 20,
    'paste_data_images': True,
    #    'autoresize_overflow_padding': 50,
}

DIS_TINYMCE_DEFAULT_CONFIG2 = {
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    # 'paste_as_text': True,
    # 'paste_text_sticky': True,
    # 'paste_remove_styles': 'true',
    # 'paste_remove_styles_if_webkit': 'true',
    # 'paste_strip_class_attributes': 'all',
    'plugins': '''
            paste textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

INVESTIGATIONS_ROOT = os.path.join(BASE_DIR, 'invs')
INVESTIGATIONS_URL = '/inv/'

TASKS_ROOT = os.path.join(BASE_DIR, 'tasks')
TASKS_URL = '/task/'
FILE_UPLOAD_MAX_MEMORY_SIZE = 262144000  # =250 MB
