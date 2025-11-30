# Windows Production Deployment Configuration
# Additional Django settings for production with multiple office users

import os
from pathlib import Path

# Production-specific settings that extend the base settings

# Database connection pooling for multiple users
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        # SQLite optimizations for Windows + multiple users
        'OPTIONS': {
            'timeout': 30,  # 30 second timeout for busy database
            'init_command': (
                'PRAGMA foreign_keys=ON;'
                'PRAGMA journal_mode=WAL;'  # Write-Ahead Logging for better concurrency
                'PRAGMA synchronous=NORMAL;'  # Balance between safety and performance
                'PRAGMA cache_size=10000;'  # Increase cache size
                'PRAGMA temp_store=MEMORY;'  # Store temp tables in memory
                'PRAGMA mmap_size=268435456;'  # 256MB memory-mapped I/O
            ),
        },
    }
}

# For even better performance with many users, consider PostgreSQL:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'resume_parser_db',
#         'USER': 'resume_parser_user',
#         'PASSWORD': 'your_password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#         'OPTIONS': {
#             'MAX_CONNS': 20,  # Connection pooling
#         },
#     }
# }

# Cache configuration for better performance
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'resume-parser-cache',
        'TIMEOUT': 300,  # 5 minutes default timeout
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# Security settings for office environment
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    # Office server IP addresses
    '192.168.1.2',  # Your office server IP
    '192.168.1.152',  # Your PC IP address
    # Add additional office network IPs if needed
    # '192.168.1.*',  # Uncomment if you want to allow entire subnet
]

# Session configuration for office users
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 86400  # 24 hours for office work day
SESSION_SAVE_EVERY_REQUEST = False  # Don't save on every request for performance

# File upload settings for resume parsing
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB in memory before writing to disk
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB max request size
FILE_UPLOAD_PERMISSIONS = 0o644

# Media files configuration for backend/media folder
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# Static files optimization
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging configuration for production monitoring
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
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django_errors.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# Performance optimizations
USE_TZ = True
USE_I18N = False  # Disable if not using internationalization
USE_L10N = False  # Disable if not using localization

# Security for office environment
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Email settings for error reporting (optional)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'your-office-smtp-server.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@office.com'
# EMAIL_HOST_PASSWORD = 'your-email-password'
# 
# ADMINS = [
#     ('Admin', 'admin@office.com'),
# ]
# 
# SERVER_EMAIL = 'server@office.com'
