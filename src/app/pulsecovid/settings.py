"""
Django settings for pulsecovid project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'pulseapp/staticfiles')
]

###########
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=0))
DJANGO_ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS")

if DJANGO_ALLOWED_HOSTS is None:
    DEBUG = 1
#DEBUG = 1

if DEBUG:
    from dotenv import load_dotenv
    from pathlib import Path

    dotenv_path = Path('../.env.prod')
    load_dotenv(dotenv_path=dotenv_path)
################

DJANGO_ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS")
DATABASE=os.environ.get("DATABASE")
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

#ALLOWED_HOSTS = os.environ.get("").split(" ")
ALLOWED_HOSTS = DJANGO_ALLOWED_HOSTS.split(" ")

REVERSEPROXY = int(os.environ.get("REVERSEPROXY"))
#REVERSEPROXY = int(REVERSEPROXY)
REVERSEPROXYURL = os.environ.get("REVERSEPROXYURL")
#REVERSEPROXYURL = REVERSEPROXYURL


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pulsecovid',
    'pulseapp',
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

ROOT_URLCONF = 'pulsecovid.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

WSGI_APPLICATION = 'pulsecovid.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

#if DEBUG:
DATABASES = {
    'default': {
        "ENGINE": os.environ.get("SQL_ENGINE"),
        "NAME": os.environ.get("SQL_DATABASE"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": os.environ.get("SQL_PORT"),
    }
}
# else:
#     DATABASES = {
#         'default': {
#             "ENGINE": SQL_ENGINE,
#             "NAME": SQL_DATABASE,
#             "USER": SQL_USER,
#             "PASSWORD": SQL_PASSWORD,
#             "HOST": SQL_HOST,
#             "PORT": SQL_PORT,
#         }
#     }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Nicosia'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

if DEBUG == 1:
    STATIC_URL = "/staticfiles/"
else:
    if REVERSEPROXY == 1:
        STATIC_URL = "/"+REVERSEPROXYURL+"/staticfiles/"
    else:
        #STATIC_URL = "/staticfiles/"
        STATIC_URL = 'https://kiosapps2.ucy.ac.cy/pulse' + "/staticfiles/"

if DEBUG == 1:
    STATIC_ROOT = "/staticfiles"
else:
    STATIC_ROOT = "/home/app/web/staticfiles"

LOGOUT_REDIRECT_URL = "/"

if DEBUG == 1:
    LOGIN_REDIRECT_URL = "/sampledata/"
else:
    if REVERSEPROXY == 1:
        LOGIN_REDIRECT_URL = "/"+REVERSEPROXYURL+"/sampledata/"
    else:
        LOGIN_REDIRECT_URL = "/sampledata/"

LOGIN_URL = "/"

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True

SESSION_EXPIRE_SECONDS = 3600
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 60
if DEBUG == 1:
    SESSION_TIMEOUT_REDIRECT = '/'
else:
    if REVERSEPROXY == 1:
        SESSION_TIMEOUT_REDIRECT = "/"+REVERSEPROXYURL
    else:
        SESSION_TIMEOUT_REDIRECT = "/"

USE_X_FORWARDED_HOST = True
if DEBUG == 1:
    FORCE_SCRIPT_NAME = "/"
else:
    if REVERSEPROXY == 1:
        FORCE_SCRIPT_NAME = "/"+REVERSEPROXYURL
    else:
        FORCE_SCRIPT_NAME = "/"

### COMMENT FOR WORK CSRF / UNCOMMENT FOR PROD

if DEBUG == 0:
    CSRF_COOKIE_SECURE = True
    # CSRF_COOKIE_HTTPONLY = True

CSP_DEFAULT_SRC = ("'none'",)
CSP_STYLE_SRC = ("'self'","'unsafe-inline'")
CSP_SCRIPT_SRC = ("'self'","'unsafe-inline'")
CSP_FONT_SRC = ("'self'")
CSP_IMG_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# PGCrypto
PGCRYPTO_KEY = SECRET_KEY
