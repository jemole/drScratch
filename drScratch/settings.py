from django.conf import global_settings

"""
Django settings for drScratch project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = '/var/www/drScratch/'

STATIC_URL = '/var/www/drScratch/static/'

STATICFILES_DIRS = (
os.path.join(BASE_DIR, '/var/www/drScratch/static'),
)

STATIC_ROOT = '/var/www/drScratch/static/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '...'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


TEMPLATE_DEBUG = True


TEMPLATE_LOADERS = (
'django.template.loaders.filesystem.Loader',
'django.template.loaders.app_directories.Loader',
#'django.template.loaders.eggs.Loader',
)


TEMPLATE_DIRS = ('/var/www/drScratch/templates',)

ALLOWED_HOSTS = [...]


# Application definition

INSTALLED_APPS = (
    'app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'drScratch.urls'

WSGI_APPLICATION = 'drScratch.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': ...,
	'USER': '',
	'PASSWORD':'',
	'HOST': '',
	'PORT': '',
    }
}

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = 'static'
MEDIA_URL = os.path.join(BASE_DIR,'static/img/')
# Internationalization

# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

_ = lambda s: s

LANGUAGES = (
    ('es', _('Spanish')),
    ('en', _('English')),
    ('ca', _('Catalan')),
    ('gl', _('Galician')),
    ('pt', _('Portuguese')),
    ('el', _('Greek')),
    ('eu', _('Basque')),
    ('it', _('Italiano')),
)


LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


EMAIL_BACKEND = ...
EMAIL_USE_TLS = False
EMAIL_HOST = ...
EMAIL_PORT = ...
EMAIL_HOST_USER = ...
EMAIL_HOST_PASSWORD = ...

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

