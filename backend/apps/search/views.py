"""
Search API Views
REST endpoints for DTSearch-like functionality
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
import logging

from .services import search_service, SearchService

logger = logging.getLogger(__name__)

@api_view(['GET'])
def search_cvs(request):
    """
    Main search endpoint - DTSearch-like functionality
    
    GET /api/search/?q=python+developer&skills=python,django&page=1&size=20
    """
    try:
        # Get query parameters
        query = request.GET.get('q', '').strip()
        page = int(request.GET.get('page', 1))
        page_size = min(int(request.GET.get('size', 20)), 100)  # Max 100 per page
        
        # Get filters
        filters = {}
        
        if request.GET.get('file_type'):
            filters['file_type'] = request.GET.get('file_type')
        
        if request.GET.get('skills'):
            skills = [s.strip() for s in request.GET.get('skills').split(',') if s.strip()]
            if skills:
                filters['skills'] = skills
        
        if request.GET.get('date_from'):
            filters['date_from'] = request.GET.get('date_from')
        
        if request.GET.get('date_to'):
            filters['date_to'] = request.GET.get('date_to')
        
        if request.GET.get('min_file_size'):
            try:
                filters['min_file_size'] = int(request.GET.get('min_file_size'))
            except ValueError:
                pass
        
        # Perform search
        if not query:
            return Response({
                'error': 'Query parameter "q" is required',
                'example': '/api/search/?q=python+developer'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        results = search_service.search_documents(
            query=query,
            filters=filters,
            page=page,
            page_size=page_size
        )
        
        # Add pagination info
        results['pagination'] = {
            'current_page': page,
            'page_size': page_size,
            'has_next': len(results['hits']) == page_size,
            'has_previous': page > 1
        }
        
        # Add search metadata
        results['search_info'] = {
            'query': query,
            'filters_applied': filters,
            'search_time_ms': results.get('took', 0)
        }
        
        return Response(results, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Search API error: {e}")
        return Response({
            'error': 'Search failed',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def boolean_search(request):
    """
    Boolean search endpoint - DTSearch-style
    
    GET /api/search/boolean/?q=Python+AND+Django
    GET /api/search/boolean/?q=Manager+OR+Lead
    GET /api/search/boolean/?q=Java+NOT+JavaScript
    """
    try:
        query = request.GET.get('q', '').strip()
        
        if not query:
            return Response({
                'error': 'Query parameter "q" is required',
                'examples': [
                    '/api/search/boolean/?q=Python+AND+Django',
                    '/api/search/boolean/?q=Manager+OR+Lead',
                    '/api/search/boolean/?q=Java+NOT+JavaScript'
                ]
            }, status=status.HTTP_400_BAD_REQUEST)
        
        results = search_service.boolean_search(query)
        
        # Add search metadata
        results['search_info'] = {
            'query': query,
            'search_type': 'boolean',
            'operators_detected': [],
            'search_time_ms': results.get('took', 0)
        }
        
        # Detect operators used
        query_upper = query.upper()
        if ' AND ' in query_upper:
            results['search_info']['operators_detected'].append('AND')
        if ' OR ' in query_upper:
            results['search_info']['operators_detected'].append('OR')
        if ' NOT ' in query_upper:
            results['search_info']['operators_detected'].append('NOT')
        
        return Response(results, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Boolean search API error: {e}")
        return Response({
            'error': 'Boolean search failed',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def search_suggestions(request):
    """
    Auto-complete suggestions endpoint
    
    GET /api/search/suggest/?q=pyth&limit=10
    """
    try:
        partial_query = request.GET.get('q', '').strip()
        limit = min(int(request.GET.get('limit', 10)), 20)  # Max 20 suggestions
        
        if len(partial_query) < 2:
            return Response({
                'suggestions': [],
                'message': 'Query must be at least 2 characters'
            }, status=status.HTTP_200_OK)
        
        suggestions = search_service.get_suggestions(partial_query, limit)
        
        return Response({
            'suggestions': suggestions,
            'partial_query': partial_query,
            'count': len(suggestions)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Suggestions API error: {e}")
        return Response({
            'error': 'Suggestions failed',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def search_status(request):
    """
    Check search system status
    
    GET /api/search/status/
    """
    try:
        # Test Elasticsearch connection
        es_connected = search_service.test_connection()
        
        # Get basic stats
        status_info = {
            'elasticsearch_connected': es_connected,
            'search_service_ready': es_connected,
            'index_name': search_service.index_name if search_service.es_client else None,
        }
        
        if es_connected:
            try:
                # Get index stats
                stats = search_service.es_client.indices.stats(index=search_service.index_name)
                status_info['document_count'] = stats['_all']['total']['docs']['count']
                status_info['index_size'] = stats['_all']['total']['store']['size_in_bytes']
            except:
                status_info['document_count'] = 'Unknown'
                status_info['index_size'] = 'Unknown'
        
        http_status = status.HTTP_200_OK if es_connected else status.HTTP_503_SERVICE_UNAVAILABLE
        
        return Response(status_info, status=http_status)
        
    except Exception as e:
        logger.error(f"Status API error: {e}")
        return Response({
            'error': 'Status check failed',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_index(request):
    """
    Create Elasticsearch index
    
    POST /api/search/create-index/
    """
    try:
        success = search_service.create_index()
        
        if success:
            return Response({
                'message': 'Index created successfully',
                'index_name': search_service.index_name
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'error': 'Failed to create index',
                'detail': 'Check Elasticsearch connection'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Create index API error: {e}")
        return Response({
            'error': 'Index creation failed',
            'detail': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def file_search(request):
    """
    File-focused search endpoint - DTSearch-like file operations
    
    GET /api/search/files/?q=python&file_type=pdf&min_size=100000
    POST /api/search/files/ with JSON: {"query": "django", "filters": {"file_type": "docx"}}
    """
    try:
        # Get query and parameters
        if request.method == 'GET':
            query = request.GET.get('q', '').strip()
            filters = {}
            
            # File-specific filters
            if request.GET.get('file_type'):
                filters['file_type'] = request.GET.get('file_type')
                
            if request.GET.get('filename'):
                filters['filename'] = request.GET.get('filename')
                
            if request.GET.get('min_size'):
                try:
                    filters['min_file_size'] = int(request.GET.get('min_size'))
                except ValueError:
                    pass
                    
            if request.GET.get('max_size'):
                try:
                    filters['max_file_size'] = int(request.GET.get('max_size'))
                except ValueError:
                    pass
                    
            if request.GET.get('date_from'):
                filters['date_from'] = request.GET.get('date_from')
                
            if request.GET.get('date_to'):
                filters['date_to'] = request.GET.get('date_to')
                
        else:  # POST
            data = request.data
            query = data.get('query', '').strip()
            filters = data.get('filters', {})
        
        if not query:
            return Response({
                'error': 'Query is required',
                'examples': [
                    'GET /api/search/files/?q=python&file_type=pdf',
                    'GET /api/search/files/?q=django&min_size=50000',
                    'POST /api/search/files/ {"query": "react", "filters": {"file_type": "docx"}}'
                ]
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get pagination parameters
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 20))
        
        # Perform search with file focus
        search_service = SearchService()
        results = search_service.search_documents(query, filters, page, size)
        
        # Add file-specific metadata to response
        results['search_info'] = {
            'query': query,
            'filters_applied': filters,
            'search_type': 'file_search',
            'file_types_found': list(set([hit.get('file_type', '') for hit in results.get('hits', []) if hit.get('file_type')])),
            'size_range': {
                'min_size_mb': min([hit.get('file_size_mb', 0) for hit in results.get('hits', []) if hit.get('file_size_mb', 0) > 0], default=0),
                'max_size_mb': max([hit.get('file_size_mb', 0) for hit in results.get('hits', [])], default=0)
            } if results.get('hits') else {},
            'search_time_ms': results.get('took', 0)
        }
        
        return Response(results, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"File search failed: {e}")
        return Response({
            'error': 'File search failed',
            'details': str(e) if settings.DEBUG else 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def search_help(request):
    """
    API documentation and examples
    
    GET /api/search/help/
    """
    help_info = {
        'endpoints': {
            'main_search': {
                'url': '/api/search/',
                'method': 'GET',
                'description': 'Main search functionality with filters',
                'parameters': {
                    'q': 'Search query (required)',
                    'skills': 'Comma-separated skills filter',
                    'file_type': 'File type filter (pdf, doc, docx, txt)',
                    'date_from': 'Date filter from (YYYY-MM-DD)',
                    'date_to': 'Date filter to (YYYY-MM-DD)',
                    'page': 'Page number (default: 1)',
                    'size': 'Results per page (default: 20, max: 100)'
                },
                'examples': [
                    '/api/search/?q=python+developer',
                    '/api/search/?q=machine+learning&skills=python,tensorflow',
                    '/api/search/?q=senior&file_type=pdf&page=2'
                ]
            },
            'boolean_search': {
                'url': '/api/search/boolean/',
                'method': 'GET',
                'description': 'Boolean search with AND, OR, NOT operators',
                'parameters': {
                    'q': 'Boolean query (required)'
                },
                'examples': [
                    '/api/search/boolean/?q=Python+AND+Django',
                    '/api/search/boolean/?q=Manager+OR+Lead',
                    '/api/search/boolean/?q=Java+NOT+JavaScript'
                ]
            },
            'suggestions': {
                'url': '/api/search/suggest/',
                'method': 'GET',
                'description': 'Auto-complete suggestions',
                'parameters': {
                    'q': 'Partial query (min 2 chars)',
                    'limit': 'Max suggestions (default: 10, max: 20)'
                },
                'examples': [
                    '/api/search/suggest/?q=pyth',
                    '/api/search/suggest/?q=mach&limit=5'
                ]
            },
            'status': {
                'url': '/api/search/status/',
                'method': 'GET',
                'description': 'Check system status'
            },
            'create_index': {
                'url': '/api/search/create-index/',
                'method': 'POST',
                'description': 'Create Elasticsearch index'
            }
        },
        'search_tips': [
            'Use quotes for exact phrases: "senior developer"',
            'Use wildcards: develop* (finds developer, development, etc.)',
            'Combine terms: python django (finds documents with both)',
            'Use boolean operators: Python AND (Django OR Flask)',
            'Filter by file type: add &file_type=pdf',
            'Filter by skills: add &skills=python,django'
        ]
    }
    
    return Response(help_info, status=status.HTTP_200_OK)
