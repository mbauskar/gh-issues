"""
Django settings for gh_issues project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import json
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_PACKAGE = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_PACKAGE.parent

try:
    with open(os.path.join(DATA_DIR, 'secret.json'), 'r') as secret_json:
        SECRET = json.loads(secret_json.read())
except Exception as e:
    SECRET = {
        'secret_key': 'a'
    }


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET.get('secret_key', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = SECRET.get('debug', True)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'issues'
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

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_PACKAGE, "templates")
        ],
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

WSGI_APPLICATION = 'base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': SECRET.get('db_name', 'livehealthreach'),
        'USER': SECRET.get('db_user', 'root'),
        'PASSWORD': SECRET.get('db_password', 'livehealthreach'),
        'HOST': SECRET.get('db_host', 'localhost'),
        'PORT': SECRET.get('db_port', '3306'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(PROJECT_PACKAGE), "static"),
)
STATIC_ROOT = ''
STATIC_URL = '/static/'

AUTH_USER_MODEL = 'issues.GitHubUser'

# github username and password

GH_USERNAME = SECRET.get('gh_username', 'gh_username')
GH_PASSWORD = SECRET.get('gh_password', 'gh_password')

GH_ACCESS_TOKEN = SECRET.get('gh_access_token', 'some-random-token')

