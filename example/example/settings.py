"""
Django settings for example project.

Generated by Cookiecutter Django Package

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "oooooooooooooooooooooooooooooooooooooooooooooooooo"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_rq',
    #'django_task.apps.DjangoTaskConfig',
    'django_task',
    'example',
    'tasks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'example.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'example.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

#
# Redis config
#

#REDIS_URL = 'redis://localhost:6379/0'
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = 6379
REDIS_URL = 'redis://%s:%d/0' % (redis_host, redis_port)

# CACHES = {
#     'default': {
#         'BACKEND': 'redis_cache.RedisCache',
#         'LOCATION': REDIS_URL
#     },
# }

# SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

#
# RQ config
#

RQ_SHOW_ADMIN_LINK = False
DJANGOTASK_LOG_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'protected', 'tasklog'))
DJANGOTASK_ALWAYS_EAGER = False
DJANGOTASK_JOB_TRACE_ENABLED = False
DJANGOTASK_REJECT_IF_NO_WORKER_ACTIVE_FOR_QUEUE = True

QUEUE_DEFAULT = 'default'
QUEUE_LOW = 'low'
QUEUE_HIGH = 'high'


def rq_queue_name(prefix, name):
    return prefix + '_' + name


def setup_rq_queues(prefix):
    """
    Purposes:
        - setup RQ_PREFIX setting for later inspection
        - setup RQ_QUEUES dictionary with instance-specific queues

    Invoke once from local.py providing an instance specific prefix;
    example:

        RQ_PREFIX = "myproject"
        RQ_QUEUES = setup_rq_queues(RQ_PREFIX)

    Alternatively, provide a fully customized RQ_QUEUES dictionary in local.py
    """
    data = {
        QUEUE_DEFAULT: {
            'URL': REDIS_URL,
            #'PASSWORD': 'some-password',
            #'DEFAULT_TIMEOUT': 5 * 60,
            'DEFAULT_TIMEOUT': -1,  # -1 means infinite
        },
        QUEUE_LOW: {
            'URL': REDIS_URL,
            #'ASYNC': False,
        },
        QUEUE_HIGH: {
            'URL': REDIS_URL,
            'DEFAULT_TIMEOUT': 500,
        },
    }

    queues = {rq_queue_name(prefix, key): value for key, value in data.items()}
    return queues

#
# RQ local configuration
#

RQ_PREFIX = "example"
RQ_QUEUES = setup_rq_queues(RQ_PREFIX)

print('RQ_QUEUES: ')
print(RQ_QUEUES)


