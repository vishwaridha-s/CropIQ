"""
Django settings for dspsoil project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from django.conf import settings

 
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR,".env"))
# DEBUG = os.getenv("DEBUG", "False") == "True"
MONGO_URI=os.getenv("MONGO_URI")
# SECRET_KEY = os.getenv("SECRET_KEY", "Rgbegk7S2xtTONxSqKIvDxAU-cajnLj_O5i1xUyf8UZ5vGEkTquGKXc4psjFrldznac")
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["new"]
mongo_users = mongo_db["users"]
mongo_data = mongo_db["data"]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ozy*cjf)v_#&5e4!!jw446iw@zjrql1aro%#wz)!r27xz38u_0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend',
    'rest_framework',
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

ROOT_URLCONF = 'dspsoil.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'dspsoil.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {},
    'mongo':{
        'ENGINE':'djongo',
         'NAME':'new',
         'CLIENT':{
             'host':MONGO_URI,         
             }
    }

}
# from pymongo import MongoClient
# mongo_client = MongoClient(MONGO_URI)
# mongo_db = mongo_client["new"]  # name of your database
# mongo_users = mongo_db["users"]
# mongo_data=mongo_db["data"]
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
from django.conf import settings as django_settings

SETTINGS_VARS = {
    "mongo_client": mongo_client,
    "mongo_db": mongo_db,
    "mongo_users": mongo_users,
    "mongo_data": mongo_data
}

globals().update(SETTINGS_VARS)

from django.conf import settings as django_settings

django_settings.mongo_client = mongo_client
django_settings.mongo_db = mongo_db
django_settings.mongo_users = mongo_users
django_settings.mongo_data = mongo_data
