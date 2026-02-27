import os
from pathlib import Path
import dj_database_url  #requirements.txt-те болуы керек

BASE_DIR = Path(__file__).resolve().parent.parent

# Қауіпсіздік баптаулары (Render environment variables-тен оқылады)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']

# Дерекқор баптаулары (Render POSTGRESQL үшін)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# Статикалық файлдар баптаулары (PRODUCTION үшін)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'