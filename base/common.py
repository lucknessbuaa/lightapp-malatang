import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

LOGIN_URL= "/app/login"

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'backend',
    "django_tables2"
)

BD_CLIENT_ID = 'PMQTgEz4V3IerHkX4lfvVh55'
BD_CLIENT_SECRET = 'dRdXrBFN2s2mzFr3T8BRxMnRRh7Plome'
BD_REDIRECT_URI = 'http://xa.limijiaoyin.com/app/auth/baidu'

WB_CLIENT_ID = '431302758'
WB_CLIENT_SECRET = '66a0b230e2d0db8607f9686448fb78b4'
WB_REDIRECT_URI = 'http://xa.limijiaoyin.com/app/auth/weibo'

QQ_CLIENT_ID = 'PMQTgEz4V3IerHkX4lfvVh55'
QQ_CLIENT_SECRET = 'dRdXrBFN2s2mzFr3T8BRxMnRRh7Plome'
QQ_REDIRECT_URI = 'http://xa.limijiaoyin.com/app/auth/qq'

AUTHENTICATION_BACKENDS = (
    'backend.backends.BaiduBackend',
    'backend.backends.WeiboBackend',
    'backend.backends.QQBackend',
    'django.contrib.auth.backends.ModelBackend'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'base.urls'

WSGI_APPLICATION = 'base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_mysqlpool.backends.mysqlpool',
        'NAME': 'malatang_dev',
        'USER': 'root',
        'PASSWORD': 'nameLR9969',
        'HOST': 'localhost',
        'PORT': '3306'
    }
} 

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "assets"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request"
)

