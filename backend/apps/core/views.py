from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.db import connection


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint to verify system status
    """
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Check Gemini API key
    gemini_status = "configured" if settings.GEMINI_API_KEY else "not configured"
    
    return Response({
        "status": "healthy",
        "database": db_status,
        "gemini_api": gemini_status,
        "version": "1.0.0"
    }) 