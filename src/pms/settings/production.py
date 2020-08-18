from pms.settings.common import *

SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('GROUPNAME', 'pms'),
        'USER': os.environ.get('GROUPNAME', 'root'),
        'PASSWORD': os.environ.get('PASSWORD', ''),
        'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.environ.get('MYSQL_PORT', '3306'),
    }
}

# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']

CORS_ORIGIN_WHITELIST = []

DATA_UPLOAD_MAX_MEMORY_SIZE = 41943040
