from django.http import JsonResponse
from django.db import connection
from django.conf import settings
import redis
from elasticsearch import Elasticsearch

def health_check(request):
    """Health check endpoint for Docker and monitoring"""
    status = {
        'status': 'healthy',
        'services': {}
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status['services']['database'] = 'healthy'
    except Exception as e:
        status['services']['database'] = f'unhealthy: {str(e)}'
        status['status'] = 'unhealthy'
    
    # Check Redis
    try:
        r = redis.from_url(settings.CELERY_BROKER_URL)
        r.ping()
        status['services']['redis'] = 'healthy'
    except Exception as e:
        status['services']['redis'] = f'unhealthy: {str(e)}'
    
    # Check Elasticsearch
    try:
        es_host = settings.ELASTICSEARCH_DSL['default']['hosts']
        es = Elasticsearch([es_host])
        if es.ping():
            status['services']['elasticsearch'] = 'healthy'
        else:
            status['services']['elasticsearch'] = 'unhealthy: cannot ping'
    except Exception as e:
        status['services']['elasticsearch'] = f'unhealthy: {str(e)}'
    
    return JsonResponse(status)
