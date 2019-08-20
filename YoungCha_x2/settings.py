"""
Django settings for YoungCha_x2 project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import os
import json

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Env for dev / deploy
def get_env(setting, envs):
    try:
        return envs[setting]
    except KeyError:
        error_msg = "You SHOULD set {} environ".format(setting)
        raise ImproperlyConfigured(error_msg)

DEV_ENVS = os.path.join(BASE_DIR, "envs_dev.json")
DEPLOY_ENVS = os.path.join(BASE_DIR, "envs.json")

if os.path.exists(DEV_ENVS): # Develop Env
    env_file = open(DEV_ENVS, encoding='UTF-8')
elif os.path.exists(DEPLOY_ENVS): # Deploy Env
    env_file = open(DEPLOY_ENVS, encoding='UTF-8')
else:
    env_file = None

if env_file is None: # System environ
    try:
        FACEBOOK_KEY = os.environ['FACEBOOK_KEY']
        FACEBOOK_SECRET = os.environ['FACEBOOK_SECRET']
        GOOGLE_KEY = os.environ['GOOGLE_KEY']
        GOOGLE_SECRET = os.environ['GOOGLE_SECRET']
    except KeyError as error_msg:
        raise ImproperlyConfigured(error_msg)
else: # JSON env
    envs = json.loads(env_file.read())
    FACEBOOK_KEY = get_env('FACEBOOK_KEY', envs)
    FACEBOOK_SECRET = get_env('FACEBOOK_SECRET', envs)
    GOOGLE_KEY = get_env('GOOGLE_KEY', envs)
    GOOGLE_SECRET = get_env('GOOGLE_SECRET', envs)

###########################

# SocialLogin: Facebook
SOCIAL_AUTH_FACEBOOK_KEY = FACEBOOK_KEY
SOCIAL_AUTH_FACEBOOK_SECRET = FACEBOOK_SECRET
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email'
}

# SocialLogin: Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = GOOGLE_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = GOOGLE_SECRET
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']
###########################################
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*eq(2zom)y7q^1#r+(o^b=vyf%tw=gzyma%r8pdzwegxu#iz5q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [

    '127.0.0.1',
    'http://127.0.0.1:8000/admin',
    'kiljaeeun.pythonanywhere.com'

]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'goologin.apps.GoologinConfig',

    # what we did
    'data',
    'haru',
    'accounts',
    # 안되는 친구들 ######################################
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # # provider 구글, 페이스북, 카톡, 깃헙
    # 'allauth.socialaccount.providers.google',  #### 제발 콤마 확인해줘..
    ################################################
    'social_django',  # 소셜로그인 관련처리 어플

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

ROOT_URLCONF = 'YoungCha_x2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'YoungCha_x2', 'templates'),

        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                ##############social로그인 관련 tmeplate 추가 부분
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',

            ],
        },
    },
]

WSGI_APPLICATION = 'YoungCha_x2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static',)
STATIC_DIRS  = (
    os.path.join(BASE_DIR, 'static'),

)


AUTH_USER_MODEL = "users_management.UserManage"

from django.urls import reverse_lazy

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('accounts:history')

# 로그인 후 프로필로 이동하숑의 뜻
LOGOUT_REDIRECT_URL = reverse_lazy('accounts:history')

AUTH_USER_MODEL = 'accounts.User'

SITE_ID = 1
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SOCIAL_AUTH_URL_NAMESPACE = 'social'
AUTHENTICATION_BACKENDS = (



    'social_core.backends.google.GoogleOAuth2',  # Google
    'social_core.backends.facebook.FacebookOAuth2',  # Facebook

    'django.contrib.auth.backends.ModelBackend',  # Django 기본 유저모델

)

# # 클라이언트 아이디
# SOCIAL_AUTH_GOOGLE_PLUS_KEY = "236597964596-2i25tsfs1339sbf1m2ujhrl8mpcnk4t9.apps.googleusercontent.com"
# SOCIAL_AUTH_GOOGLE_PLUS_SECRET = "xlu3l3WZImyRMyrf48zJ58C4"
# # 보안비밀
