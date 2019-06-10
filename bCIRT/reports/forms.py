from django import forms
# Get the user so we can use this
from django.contrib.auth import get_user_model
import logging
logger = logging.getLogger('log_file_verbose')
User = get_user_model()


