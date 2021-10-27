from .base import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'api.apps.ApiConfig',
  'rest_framework',
  'django_filters',
  'herokuapp'
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)
