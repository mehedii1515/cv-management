#!/usr/bin/env python3
"""
Production server startup script using Waitress
Optimized for Windows office environment with multiple users
"""
import os
import sys
import logging
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Change working directory to backend
os.chdir(backend_dir)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_parser.settings')

try:
    import django
    django.setup()
except ImportError:
    raise ImportError(
        "Django is not installed or not properly configured. "
        "Make sure you have installed requirements and set up the environment."
    )

def setup_logging():
    """Setup production logging"""
    import logging.config
    
    LOGGING_CONFIG = {
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
                'filename': 'logs/django_production.log',
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
        },
    }
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)  # Create logs in root directory
    
    logging.config.dictConfig(LOGGING_CONFIG)

def main():
    """Start the production server"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        from waitress import serve
        from django.core.wsgi import get_wsgi_application
        
        # Get the WSGI application
        application = get_wsgi_application()
        
        # Production server configuration for office environment
        logger.info("Starting production server with Waitress...")
        logger.info("Server will be available for office users")
        logger.info("Access the application at: http://localhost:8000")
        
        serve(
            application,
            host='0.0.0.0',  # Listen on all interfaces for office network access
            port=8000,
            threads=16,  # Increased threads for multiple office users
            connection_limit=1000,  # Support more concurrent connections
            cleanup_interval=30,  # Clean up connections every 30 seconds
            channel_timeout=120,  # 2 minutes timeout for long requests
            max_request_body_size=52428800,  # 50MB for file uploads
            send_bytes=18000,  # Optimize for office network
            
            # Windows-specific optimizations
            asyncore_use_poll=False,  # Better for Windows
            
            # Logging
            _quiet=False,  # Show startup messages
        )
        
    except ImportError:
        logger.error("Waitress is not installed. Install with: pip install waitress")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
