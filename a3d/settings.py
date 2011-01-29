# Django settings for a3d project.

import os
import django
# calculated paths for django and the site
# used as starting points for various other paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
     'django.core.context_processors.request',
     'board.context_processors.base_template',
     'board.context_processors.personal_settings',
     'almparse.context_processors.available_macros',
)


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'a3d'             # Or path to database file if using sqlite3.
DATABASE_USER = 'a3d'             # Not used with sqlite3.
DATABASE_PASSWORD = 'a3d'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/a3dmedia/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a1h+9bg!#9=cj=_b63brdgk+(oyjw==35!+l=9g1k17il2qu-4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'denorm.middleware.DenormMiddleware',
    'board.middleware.CurrentUserPageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
#    'board.middleware.StatsMiddleware',

)

ROOT_URLCONF = 'a3d.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates')
)

AUTHENTICATION_BACKENDS = (
    'board.auth_backends.CaseInsensitiveModelBackend',
)

AUTH_PROFILE_MODULE = 'board.UserProfile'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.humanize',
    'profiles',
    'registration',
#    'denorm',
    'a3d.faves',
    'debug_toolbar',
    'a3d.almparse',
    'a3d.board',
    'south'
)


# TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.debug',)
INTERNAL_IPS = ('127.0.0.1',)

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.

# Various apps available
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.cache.CacheDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
DEBUG_TOOLBAR_CONFIG = {
     'INTERCEPT_REDIRECTS': False,
     'SHOW_TOOLBAR_CALLBACK': lambda req: DEBUG and req.session.get('_auth_user_id',0) == 77 #FIXME: Horrible hack!
}

#BOARD SPECIFIC SETTINGS
A3D_BASE_SETTINGS = {
    'min_rating_for_home':5,
    'min_rating_for_summary':6,
    'min_rating_for_display':0,
    'threshold_low_rating':-1,
    'threshold_high_rating':4,
    'post_per_page':10,
    'base_rating':1,
    'tags_fetch_interval': 180200,
    'mentions_fetch_interval': 71000,
    'favorites_fetch_interval': 60500,
    'new_content_fetch_interval': 30300,
}
