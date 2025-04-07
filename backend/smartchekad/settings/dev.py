from .base import *

# Debug mode for development
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database (PostgreSQL for development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='mycrm_dev'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='yourpassword'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}