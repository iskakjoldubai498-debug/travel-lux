import os
from pathlib import Path
import cloudinary
import dj_database_url

# Долбоордун негизги папкасы
BASE_DIR = Path(__file__).resolve().parent.parent

# --- КООПСУЗДУК ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key')

# Ноутбукта иштеп жатканда DEBUG дайыма True болушу керек
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Бардык домендерге жана IP даректерге уруксат берүү
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'cloudinary_storage', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'tours', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
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
        'DIRS': [BASE_DIR / 'templates'],
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

# --- МААЛЫМАТ БАЗАСЫ (Локалдык жана Railway үчүн) ---
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Railway же башка серверде иштегенде
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
    DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}
else:
    # Ноутбукта локалдык иштегенде (db.sqlite3 колдонулат)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# --- ТИЛ ЖАНА УБАКЫТ ---
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_TZ = True

# --- CLOUDINARY (Сүрөттөр үчүн) ---
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dtuyalp6m',
    'API_KEY': '636667862685854',
    'API_SECRET': 'PgRp9Z7dBhdkoVTk0K1sa1I1390'
}

cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET'],
    secure=True
)

# --- СТАТИКАЛЫК ФАЙЛДАР ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise статиканы иштетүү үчүн
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- МЕДИА ФАЙЛДАР ---
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CSRF ЖӨНДӨӨЛӨРҮ ---
CSRF_TRUSTED_ORIGINS = [
    "https://*.up.railway.app",
    "https://travel-lux-production.up.railway.app",
    "http://10.174.189.71:8000", # Ноутбуктун IP дареги
]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')