from datetime import timedelta
from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("❌ DJANGO_SECRET_KEY environment variable is not set!")

DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN and not DEBUG:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN environment variable is not set!")

TELEGRAM_BOT_WEBHOOK_URL = os.environ.get('TELEGRAM_BOT_WEBHOOK_URL', '')
MINI_APP_URL = os.environ.get('MINI_APP_URL', 'https://app-vercel-drab.vercel.app')


SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False') == 'True'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'False') == 'True'

SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 0))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'False') == 'True'
SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', 'False') == 'True'

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'


CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'ngrok-skip-browser-warning',
    'x-telegram-init-data',
]

# ============================================================================
# APPLICATION DEFINITION
# ============================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    'drf_yasg',
    'django_filters',
    'djoser',
    'rest_framework_simplejwt',
    'corsheaders',

    # Local apps
    'products',
    'telegram_bot'
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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# ============================================================================
# DATABASE
# ============================================================================
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DB_NAME', 'mini_shop'),
        'USER': os.environ.get('DB_USER', 'telegram_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'ui_telegram_user'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Database connection pooling
CONN_MAX_AGE = int(os.environ.get('CONN_MAX_AGE', 0))

# ============================================================================
# CACHE & SESSIONS
# ============================================================================
REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Session caching (Redis da session saqlash)
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# ============================================================================
# STATIC & MEDIA FILES
# ============================================================================
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# File upload limits
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# ============================================================================
# LOGGING
# ============================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django-errors.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'telegram_bot': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}

# ============================================================================
# ERROR REPORTING
# ============================================================================
ADMINS = [('Admin', os.environ.get('ADMIN_EMAIL', 'admin@example.com'))]
MANAGERS = ADMINS

# ============================================================================
# INTERNATIONALIZATION
# ============================================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ============================================================================
# DEFAULT PRIMARY KEY
# ============================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================================
# REST FRAMEWORK & JWT
# ============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ============================================================================
# DOCKER SPECIFIC SETTINGS
# ============================================================================
IS_DOCKER = os.environ.get('IS_DOCKER', 'False') == 'True'

if IS_DOCKER:
    # Docker da database host container nomiga o'zgaradi
    DATABASES['default']['HOST'] = os.environ.get('DB_HOST', 'db')

    # Redis URL ni container nomiga moslash
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/1')
    CACHES['default']['LOCATION'] = REDIS_URL

    # Media va static fayllar volume path
    MEDIA_ROOT = '/app/media'
    STATIC_ROOT = '/app/staticfiles'

    # Logs papkasini yaratish
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)