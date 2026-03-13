import os
from pathlib import Path
import dj_database_url
from datetime import timedelta

# Жобаның негізгі жолы
BASE_DIR = Path(__file__).resolve().parent.parent

# Қауіпсіздік (DEBUG-ты Render-де False қылған дұрыс)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-key-here')
DEBUG = True  # Қателерді көру үшін әзірше True қалдыр

ALLOWED_HOSTS = ['*', 'instagram-clone-1-7wmz.onrender.com', 'localhost', '127.0.0.1']

# 1. ҚОЛДАНБАЛАР (Бәрі осында болуы керек)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Сыртқы пакеттер
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # Сенің қолданбаң
    'pages',
]

# 2. MIDDLEWARE (Реттілігін бұзба!)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Статика үшін
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS міндетті түрде Common-нан жоғары
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

# 3. БАЗА (Render Postgres + Local SQLite)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600
    )
}

# 4. REST FRAMEWORK & JWT (Токен алу үшін)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}

# Токеннің өмір сүру уақыты (тексеруге ыңғайлы болу үшін)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Қолданушы моделі (Сенің pages қолданбаңдағы User)
AUTH_USER_MODEL = 'pages.User'

# CORS (Postman-нан кедергісіз жіберу үшін)
CORS_ALLOW_ALL_ORIGINS = True

# Статикалық файлдар
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'