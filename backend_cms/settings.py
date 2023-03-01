"""
Django settings for backend_cms project.

Generated by 'django-admin startproject' using Django 3.2.15.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


# read environment variables
my_env = environ.Env()
environ.Env.read_env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = my_env("DJ_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# get from .env file
DEBUG = my_env("DEBUG")

ALLOWED_HOSTS = [
    "backend-cms3.eba-fdjnmcbd.ap-southeast-1.elasticbeanstalk.com",
    "www.backend-cms3.eba-fdjnmcbd.ap-southeast-1.elasticbeanstalk.com",
    # Django site can serve all host/domain names
    "*"
]

CORS_ALLOWED_ORIGINS = [
    # "https://example.com",
    # "https://sub.example.com",
    "http://localhost:8200",
    "http://127.0.0.1:8200",
    # The url below represents android mobile devices
    "http://localhost",

    # netlify frontend
    "https://bejewelled-marshmallow-b949b6.netlify.app",
    "http://bejewelled-marshmallow-b949b6.netlify.app",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    # Django site can accept any types of headers, including customised ones
    # eg. Content-Disposition
    "*"
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'corsheaders',
    'users',
    'appointment',
    'clinic',
    'voice_recognition',
    'encounter',
    'diagnosis',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend_cms.urls'

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

WSGI_APPLICATION = 'backend_cms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DB_DATABASE_NAME = my_env("DB_NAME")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': my_env("DB_HOST"),
        'NAME': my_env("DB_NAME"),
        'USER': my_env("DB_USER"),
        'PASSWORD': my_env("DB_PASS"),
        'PORT': my_env("DB_PORT"),
        'TEST': {
            'NAME': 'mytestdatabase'
        }
    }
}


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "users.User"
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'
}