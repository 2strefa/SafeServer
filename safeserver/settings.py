#-*- encoding: utf-8 -*-
# Django settings for safeserver project.

import os

DEBUG = True

TEMPLATE_DEBUG = DEBUG
# wygasanie sesji logowania w min
AUTO_LOGOUT_DELAY = 100

ADMINS = (

     ('Albert', 'biuro@safeserver.pl'),

)

DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'biuro@safeserver.pl'
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.safeserver.pl'
EMAIL_HOST_USER = 'biuro@safeserver.pl'
EMAIL_HOST_PASSWORD = '1981pionier'
EMAIL_PORT = 25

MANAGERS = ADMINS



DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.

        'NAME': 'druga_safeserver',                      # Or path to database file if using sqlite3.

        'USER': 'druga_safe',                      # Not used with sqlite3.

        'PASSWORD': '1981MOJAniunia',                  # Not used with sqlite3.

        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.

        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.

    }

}

# Hosts/domain names that are valid for this site; required if DEBUG is False

# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts

ALLOWED_HOSTS = []



# Local time zone for this installation. Choices can be found here:

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name

# although not all choices may be available on all operating systems.

# In a Windows environment this must be set to your system time zone.

TIME_ZONE = 'Europe/Warsaw'



# Language code for this installation. All choices can be found here:

# http://www.i18nguy.com/unicode/language-identifiers.html

LANGUAGE_CODE = 'pl'



SITE_ID = 1



# If you set this to False, Django will make some optimizations so as not

# to load the internationalization machinery.

USE_I18N = True



# If you set this to False, Django will not format dates, numbers and

# calendars according to the current locale.

USE_L10N = True



# If you set this to False, Django will not use timezone-aware datetimes.

USE_TZ = True



# Absolute filesystem path to the directory that will hold user-uploaded files.

# Example: "/home/media/media.lawrence.com/media/"

MEDIA_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), 'media/'))



# URL that handles the media served from MEDIA_ROOT. Make sure to use a

# trailing slash.

# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"

MEDIA_URL = '/media/'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'



# Absolute path to the directory static files should be collected to.

# Don't put anything in this directory yourself; store your static files

# in apps' "static/" subdirectories and in STATICFILES_DIRS.

# Example: "/home/media/media.lawrence.com/static/"

STATIC_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), 'static/'))



# URL prefix for static files.

# Example: "http://media.lawrence.com/static/"

STATIC_URL = '/static/'



# Additional locations of static files

STATICFILES_DIRS = (

    # Put strings here, like "/home/html/static" or "C:/www/django/static".

    # Always use forward slashes, even on Windows.

    # Don't forget to use absolute paths, not relative paths.

)



# List of finder classes that know how to find static files in

# various locations.

STATICFILES_FINDERS = (

    'django.contrib.staticfiles.finders.FileSystemFinder',

    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    # potrzebne do forum Dinette
    # 'compressor.finders.CompressorFinder',

)



# Make this unique, and don't share it with anybody.

SECRET_KEY = '+wg&amp;habc0i$%yo)5rw#a4i=n%7m93^&amp;$azyi$de=po)8kt_2xz'



# List of callables that know how to import templates from various sources.

TEMPLATE_LOADERS = (

    'django.template.loaders.filesystem.Loader',

    'django.template.loaders.app_directories.Loader',

#     'django.template.loaders.eggs.Loader',

)



MIDDLEWARE_CLASSES = (

    'django.middleware.common.CommonMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.contrib.auth.backends.ModelBackend',

    'konto.middleware.AutoLogout',

    # Uncomment the next line for simple clickjacking protection:

    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',

)



ROOT_URLCONF = 'safeserver.urls'

ACCOUNT_ACTIVATION_DAYS = 7

# Python dotted path to the WSGI application used by Django's runserver.

WSGI_APPLICATION = 'safeserver.wsgi.application'

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\','/'),)


INSTALLED_APPS = (

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.sites',

    'django.contrib.messages',

    'registration',

    #'django.contrib.staticfiles',

    # Uncomment the next line to enable the admin:

    'django.contrib.admin',

    'paypal.standard.ipn',

    'home',

    'oferta',

    'konto',

    'south',

)

# LOG_FILE_NAME = 'dinette.log'
# LOG_FILE_PATH = 'D:\Programy\Strona\safeserver.pl\safeserver'

# PROJECT_ROOT = os.path.dirname(__file__)
#
# LOG_FILE_NAME = "denette.log"
# LOG_FILE_PATH = os.path.join(PROJECT_ROOT, "logs")

PAYPAL_RECEIVER_EMAIL = "biuro@2strefa.pl"
PAYPAL_IMAGE = 'https://www.paypalobjects.com/webstatic/mktg/logo/AM_mc_vs_dc_ae.jpg'
SITE_NAME = 'http://safeserver.pl'

# A sample logging configuration. The only tangible logging

# performed by this configuration is to send an email to

# the site admins on every HTTP 500 error when DEBUG=False.

# See http://docs.djangoproject.com/en/dev/topics/logging for

# more details on how to customize your logging configuration.

LOGGING = {

    'version': 1,

    'disable_existing_loggers': False,

    'filters': {

        'require_debug_false': {

            '()': 'django.utils.log.RequireDebugFalse'

        }

    },

    'handlers': {

        'mail_admins': {

            'level': 'ERROR',

            'filters': ['require_debug_false'],

            'class': 'django.utils.log.AdminEmailHandler'

        }

    },

    'loggers': {

        'django.request': {

            'handlers': ['mail_admins'],

            'level': 'ERROR',

            'propagate': True,

        },

    }

}
