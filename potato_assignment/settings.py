"""
Django settings for potato_assignment project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from djangae.settings_base import * #Set up some AppEngine specific stuff

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

from .boot import get_app_config
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_app_config().secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
COMPRESS_ENABLED = True
TEMPLATE_DEBUG = False

ADMINS = (('Matteo Parrucci', 'parruc@gmail.com'),)

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]
COMPRESS_OFFLINE = True
# Application definition

ALLOWED_HOSTS = (
    "localhost",
    "potato-assignment.appspot.com")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sitemaps',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangosecure',
    'csp',
    'djangae.contrib.gauth',
    'djangae',
    'blog',
    'contacts',
    'compressor',
    'ckeditor',
    'url_tools',
]
TEST = False
if TEST:
    INSTALLED_APPS.append('django_nose')
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

    NOSE_ARGS = [
        '--with-coverage',
        '--cover-package=blog,contacts',
    ]

CKEDITOR_UPLOAD_PATH = "ck-uploads/"
CKEDITOR_CONFIGS = {'default': {'toolbar': 'full', }, }
MIDDLEWARE_CLASSES = (
    'djangae.contrib.security.middleware.AppEngineSecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'djangae.contrib.gauth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
    'session_csrf.CsrfMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "session_csrf.context_processor",
    "url_tools.context_processors.current_url",
)

TEMPLATE_DIRS = (
    "potato_assignment/templates"
)

def check_session_csrf_enabled():
    if "session_csrf.CsrfMiddleware" not in MIDDLEWARE_CLASSES:
        return [ "SESSION_CSRF_DISABLED"]

    return []
check_session_csrf_enabled.messages = { "SESSION_CSRF_DISABLED" : "Please add 'session_csrf.CsrfMiddleware' to MIDDLEWARE_CLASSES" }

SECURE_CHECKS = [
    "djangosecure.check.sessions.check_session_cookie_secure",
    "djangosecure.check.sessions.check_session_cookie_httponly",
    "djangosecure.check.djangosecure.check_security_middleware",
    "djangosecure.check.djangosecure.check_sts",
    "djangosecure.check.djangosecure.check_frame_deny",
    "djangosecure.check.djangosecure.check_ssl_redirect",
    "potato_assignment.settings.check_session_csrf_enabled"
]

ROOT_URLCONF = 'potato_assignment.urls'

WSGI_APPLICATION = 'potato_assignment.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

STATICFILES_DIRS = (
    'potato_assignment/static',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

CSP_DEFAULT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval")
CSP_CONNECT_SRC = ("'self'", "googe.com", "youtube.com", "twitter.com", "facebook.com", "ggpht.com")
CSP_IMG_SRC = ("'self'", "*.ggpht.com")
from djangae.contrib.gauth.settings import *
