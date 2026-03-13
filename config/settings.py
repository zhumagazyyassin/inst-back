import os
from pathlib import Path
import dj_database_url  # requirements.txt-те болуы керек

# Жобаның негізгі папкасы
BASE_DIR = Path(__file__).resolve().parent.parent
CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
]

# Қауіпсіздік баптаулары (Render environment variables-тен оқылады)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['instagram-clone-1-7wmz.onrender.com', 'localhost', '127.0.0.1']
# Қолданбалар тізімі (Қолданбаларыңызды қосыңыз)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Қолданбаларыңыз:
    'main',
    'pages',
    'posts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise қосу
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs баптауы (config папкасында орналасқан)
ROOT_URLCONF = 'config.urls'  # ТҮЗЕТІЛДІ

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# WSGI баптауы
WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'), 
        conn_max_age=600
    )
}

# Статикалық файлдар баптаулары (PRODUCTION үшін)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # ТҮЗЕТІЛДІ: Бұл жолды қосыңыз егер static папкаңыз болса

# WhiteNoise баптауы
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Медиа файлдар (суреттер)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Қолданушы моделін өзгерту
AUTH_USER_MODEL = 'pages.User' # ТҮЗЕТІЛДІ: Бұл жолды қосыңыз!
# REST_FRAMEWORK сөздігі осылай жабылуы керек
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny', 
    ),
} # Осы жақша міндетті түрде болуы керек!

# МЫНА ЖОЛДАР СӨЗДІКТЕН БӨЛЕК, ТӨМЕНДЕ ТҰРУЫ ТИІС:
CORS_ALLOW_ALL_ORIGINS = True  
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https'),

