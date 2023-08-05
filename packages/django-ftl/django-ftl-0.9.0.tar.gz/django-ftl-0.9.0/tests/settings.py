# -*- coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "-vgnk4x&72$zmxhp$q6sch83v%@mp()&6*+kf2du0r7l#8i2v-"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django_ftl",
    "tests",
]

SITE_ID = 1

MIDDLEWARE = ()

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': []
        },
    },
]

LANGUAGE_CODE = 'en'
