# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zuvp4036q9zpc!)0sac=qhk!%udh^5dcavrr@lc6c)m41f3nz%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['*']

from base.common import *

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)

from base.loggers import LOGGING

