import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*2^-hf$%)08eyj7*1&_q%fs_5j7*1&_q%fs_5j7*1&_q%fs_5b0h&qm0$u)#!f0cy0g*9eq)*b0h&qm0$u)#!f0cy0g*9eq)*b0h&qm0$u)#!f0cy0g*9eq)*b0h&qm0$u)#!f0cy0g*9eq)*b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['idsbiolozi.com', 'www.idsbiolozi.com', '127.0.0.1', '34.141.0.143',]

INTERNAL_IPS = [
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django_filters',
    'honeypot',
    'journal',
    'debug_toolbar',
    'autoslug',
    'rest_framework',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sci.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sci.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/Users/yellowflash/PycharmProjects/sci/db.sqlite3',
        # 'NAME': '/home/anovindooel/apps/bsrs/db.sqlite3',
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

MAIL_PASS = 'afdsvwroucagsnkn'
AUTOSTOP_MAIL_PASS = 'ktgucaaqrbtuqdjc'
TBT_MAIL_PASS = 'hzikdxeyswxjlzqf'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'anovski3@gmail.com'
EMAIL_HOST_PASSWORD = 'afdsvwroucagsnkn'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'anovski3@gmail.com'

PWA_APP_NAME = 'Bulletin of the Biology Students Research Society'
PWA_APP_DESCRIPTION = 'The Bulletin of the Biology Students’ Research Society is a scientific journal that is being' \
                      ' published once in a few years. This closes the circle in the process of professional growth of ' \
                      'biologists during their undergraduate studies.'
PWA_APP_THEME_COLOR = '#e5e5e5'
PWA_APP_BACKGROUND_COLOR = '#e1e2e5'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'

PWA_APP_ICONS = [
    {
        'src': 'static/img/logo.png',
        'sizes': '160x160'
    },
    {
        'src': 'static/img/maskable_icon_x48.png',
        'sizes': '48x48'
    },
    {
        'src': 'static/img/maskable_icon_x72.png',
        'sizes': '72x72'
    },
    {
        'src': 'static/img/maskable_icon_x96.png',
        'sizes': '96x96'
    },
    {
        'src': 'static/img/maskable_icon_x128.png',
        'sizes': '128x128'
    },
    {
        'src': 'static/img/maskable_icon_x192.png',
        'sizes': '192x192'
    },
    {
        'src': 'static/img/maskable_icon_x512.png',
        'sizes': '512x512'
    }
]

PWA_APP_ICONS_APPLE = [{'src': 'static/img/logo.png', 'sizes': '160x160'}]

PWA_APP_SPLASH_SCREEN = [
    {
        'src': 'static/img/logo.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
