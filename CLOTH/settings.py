"""
Django settings for CLOTH project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from decouple import config, Csv
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = config('SECRET_KEY')
SECRET_KEY='03416278ee91db015da41f4464fc7533ea281fe6021d9f7dc5'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)


ALLOWED_HOSTS = ['onlineteeshop.herokuapp.com', '127.0.0.1'] #set to '*' if debug is false
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Application definition

INSTALLED_APPS = [
    'accounts', #stripe
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',
    'django.contrib.sites',  # for flat pages
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'catalog_app',
    'store_app',
    'search_app',
    'cart',
    'checkout',
    'stripe',
    'stats',
    'tagging',
    'marketing',
    'utils',
    's3boto', #name of the app we created to hold our boto files for media storage
    'storages',
]
 
# for use with URL Canonicalization Middleware:
# this is the canonical hostname to be used by your app (required)

# these are the hostnames that will be redirected to the CANON_URL_HOSTNAME 
# (optional; if not provided, all non-matching will be redirected)
# CANON_URLS_TO_REWRITE = ['tee-shop.com', 'tees-shop.com']

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # flat pages in middleware
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # canoncalization in middleware
    'marketing.urlcanon.URLCanonicalizationMiddleware',
]



ROOT_URLCONF = 'CLOTH.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['template'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.cloth',#context processor.py
            ],
        },
    },
]

WSGI_APPLICATION = 'CLOTH.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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





SITE_ID = 2

SITE_NAME = 'Tees Shop'
META_KEYWORDS = 'T-shirts, hoodies, sneakers, jeans'
META_DESCRIPTION = 'Teeshop is an online supplier of tees and sneakers'

PRODUCTS_PER_PAGE =6
PRODUCTS_PER_ROW =4

STRIPE_SECRET_KEY=config('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY=config('STRIPE_PUBLISHABLE_KEY')


LOGIN_REDIRECT_URL = 'my_account' #name of the url link for the login in our app
LOGOUT_REDIRECT_URL = 'accounts/logout/' #the redirect url is the same as the logout url used in our app url


SESSION_COOKIE_DAYS = 90
SESSION_COOKIE_AGE = 60 * 60 * 24 * SESSION_COOKIE_DAYS 

CACHE_TIMEOUT = 60 * 60

AWS_ACCESS_KEY_ID=config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=config("AWS_SECRET_ACCESS_KEY")
AWS_S3_OBJECT_PARAMETERS={'CacheControl':'max-age=86400',}

AWS_STORAGE_BUCKET_NAME='teeshop-static'

AWS_S3_REGION_NAME='us-east-2'

AWS_S3_CUSTOM_DOMAIN='%s.s3.%s.amazonaws.com'%(AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME)

AWS_S3_FILE_OVERWRITE=False
AWS_DEFAULT_ACL=None

AWS_LOCATION='static'

STATIC_URL = 'https://%s/%s/'%(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]


MEDIA_FILES_LOCATION='products_images'
MEDIA_URL = 'https://%s/%s/'%(AWS_S3_CUSTOM_DOMAIN, MEDIA_FILES_LOCATION)
MEDIA_ROOT = os.path.join(BASE_DIR, 'products_images')


# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage' 
DEFAULT_FILE_STORAGE = 's3boto.storage_backends.MediaStorage' #for the media files, where s3boto is the app we created

# 'https://teeshop-static.s3.us-east-2.amazonaws.com/products_images/products/main/about-banner-free-img-1024x683.jpg'
# "https://teeshop-static.s3.us-east-2.amazonaws.com/products_images/products/thumbnails/anchor-bracelet-blue-free-img.jpg
# 'https://teeshop-static.s3.us-east-2.amazonaws.com/products_images/products/thumbnails/T_4_front1.jpg'




MEDIA_URL = '/products_images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'products_images')


django_heroku.settings(locals())