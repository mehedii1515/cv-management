"""
Search Service for DTSearch-like functionality
Handles all Elasticsearch operations and search logic
"""
import hashlib
import logging
from typing import List, Dict, Any, Optional
from django.core.cache import cache
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from .documents import CVDocument

logger = logging.getLogger(__name__)

class SearchService:
    """
    DTSearch-like search service with advanced capabilities
    """
    
    def __init__(self):
        """Initialize Elasticsearch connection"""
        try:
            self.es_client = Elasticsearch([
                {'host': 'localhost', 'port': 9200}
            ])
            self.index_name = 'cv_documents'
            logger.info("SearchService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize SearchService: {e}")
            self.es_client = None
    
    def test_connection(self) -> bool:
        """Test Elasticsearch connection"""
        try:
            if self.es_client and self.es_client.ping():
                info = self.es_client.info()
                logger.info(f"Elasticsearch connected: {info['version']['number']}")
                return True
            return False
        except Exception as e:
            logger.error(f"Elasticsearch connection failed: {e}")
            return False
    
    def create_index(self) -> bool:
        """Create Elasticsearch index if it doesn't exist"""
        try:
            if not self.es_client:
                return False
                
            if not self.es_client.indices.exists(index=self.index_name):
                # Create index with proper mapping
                CVDocument.init(index=self.index_name)
                logger.info(f"Created Elasticsearch index: {self.index_name}")
                return True
            else:
                logger.info(f"Index {self.index_name} already exists")
                return True
        except Exception as e:
            logger.error(f"Failed to create index: {e}")
            return False
    
    def search_documents(self, query: str, filters: Optional[Dict] = None, 
                        page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """
        Main search function - DTSearch-like functionality
        
        Args:
            query: Search query string
            filters: Dictionary of filters (file_type, date_range, etc.)
            page: Page number for pagination
            page_size: Number of results per page
            
        Returns:
            Dictionary with search results and metadata
        """
        if not self.es_client or not query.strip():
            return self._empty_result()
        
        # Check cache first (5 minutes cache)
        cache_key = self._generate_cache_key(query, filters, page, page_size)
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Returning cached results for query: {query}")
            return cached_result
        
        try:
            # Build Elasticsearch search
            search = Search(using=self.es_client, index=self.index_name)
            
            # Add query
            if query:
                search = self._build_query(search, query)
            
            # Add filters
            if filters:
                search = self._apply_filters(search, filters)
            
            # Add highlighting
            search = self._add_highlighting(search)
            
            # Elasticsearch sorts by _score automatically
            
            # Pagination
            start = (page - 1) * page_size
            search = search[start:start + page_size]
            
            # Execute search
            response = search.execute()
            
            # Format results
            results = self._format_results(response)
            
            # Cache results for 5 minutes
            cache.set(cache_key, results, 300)
            
            logger.info(f"Search completed: {query} -> {results['total_hits']} results")
            return results
            
        except Exception as e:
            logger.error(f"Search failed for query '{query}': {e}")
            return self._empty_result()
    
    def boolean_search(self, query: str) -> Dict[str, Any]:
        """
        Boolean search with AND, OR, NOT operators (DTSearch-style)
        
        Args:
            query: Boolean query string (e.g., "Python AND Django", "Manager OR Lead")
            
        Returns:
            Search results dictionary
        """
        if not self.es_client:
            return self._empty_result()
        
        try:
            search = Search(using=self.es_client, index=self.index_name)
            
            # Parse boolean operators
            if ' AND ' in query.upper():
                terms = [term.strip() for term in query.upper().split(' AND ')]
                bool_query = Q('bool', must=[
                    Q('multi_match', 
                      query=term, 
                      fields=['file_content', 'name', 'skills', 'experience'])
                    for term in terms
                ])
            elif ' OR ' in query.upper():
                terms = [term.strip() for term in query.upper().split(' OR ')]
                bool_query = Q('bool', should=[
                    Q('multi_match', 
                      query=term, 
                      fields=['file_content', 'name', 'skills', 'experience'])
                    for term in terms
                ])
            elif ' NOT ' in query.upper():
                positive_term, negative_term = query.upper().split(' NOT ', 1)
                bool_query = Q('bool', 
                             must=[Q('multi_match', 
                                   query=positive_term.strip(), 
                                   fields=['file_content', 'name', 'skills', 'experience'])],
                             must_not=[Q('multi_match', 
                                       query=negative_term.strip(), 
                                       fields=['file_content', 'name', 'skills', 'experience'])])
            else:
                # Fall back to regular search
                return self.search_documents(query)
            
            search = search.query(bool_query)
            search = self._add_highlighting(search)
            # Elasticsearch sorts by _score automatically
            
            response = search.execute()
            results = self._format_results(response)
            
            logger.info(f"Boolean search completed: {query} -> {results['total_hits']} results")
            return results
            
        except Exception as e:
            logger.error(f"Boolean search failed for query '{query}': {e}")
            return self._empty_result()
    
    def get_suggestions(self, partial_query: str, limit: int = 10) -> List[str]:
        """
        Auto-complete suggestions for search
        
        Args:
            partial_query: Partial search term
            limit: Maximum number of suggestions
            
        Returns:
            List of suggested search terms
        """
        if not self.es_client or len(partial_query) < 2:
            return []
        
        try:
            # Search for terms that start with the partial query
            search = Search(using=self.es_client, index=self.index_name)
            search = search.query(
                'prefix', 
                **{'skills.keyword': partial_query}
            )
            search = search[:limit]
            
            response = search.execute()
            suggestions = []
            
            for hit in response:
                if hasattr(hit, 'skills') and hit.skills:
                    for skill in hit.skills.split(','):
                        skill = skill.strip()
                        if skill.lower().startswith(partial_query.lower()) and skill not in suggestions:
                            suggestions.append(skill)
                            if len(suggestions) >= limit:
                                break
                if len(suggestions) >= limit:
                    break
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Suggestions failed for query '{partial_query}': {e}")
            return []
    
    def _build_query(self, search: Search, query: str) -> Search:
        """Build multi-match query with field boosting including file content"""
        return search.query(
            'multi_match',
            query=query,
            fields=[
                'extracted_text^2.0',     # File content (highest priority - DTSearch-like)
                'name^1.8',               # Person name
                'skills^1.5',             # Skills
                'experience^1.3',         # Experience
                'education^1.0',          # Education
                'filename^1.0',           # Filename search
                'email^0.8',              # Email
                'phone^0.5',              # Phone
            ],
            type='best_fields'
        )
    
    def _apply_filters(self, search: Search, filters: Dict) -> Search:
        """Apply search filters including file-based filters"""        
        if filters.get('skills'):
            for skill in filters['skills']:
                search = search.filter('match', skills=skill)
        
        if filters.get('years_of_experience'):
            search = search.filter('range', years_of_experience={'gte': filters['years_of_experience']})
        
        if filters.get('location'):
            search = search.filter('match', location=filters['location'])
        
        # File-based filters
        if filters.get('file_type'):
            search = search.filter('term', file_type=filters['file_type'])
        
        if filters.get('filename'):
            search = search.filter('match', filename=filters['filename'])
        
        if filters.get('min_file_size'):
            search = search.filter('range', file_size={'gte': filters['min_file_size']})
        
        if filters.get('max_file_size'):
            search = search.filter('range', file_size={'lte': filters['max_file_size']})
        
        if filters.get('date_from'):
            search = search.filter('range', indexed_date={'gte': filters['date_from']})
        
        if filters.get('date_to'):
            search = search.filter('range', indexed_date={'lte': filters['date_to']})
        
        return search
    
    def _add_highlighting(self, search: Search) -> Search:
        """Add search result highlighting for file content and metadata"""
        return search.highlight(
            'extracted_text',          # File content highlighting
            'filename',                # Filename highlighting  
            'name',                    # Name highlighting
            'skills',                  # Skills highlighting
            'experience',              # Experience highlighting
            fragment_size=200,
            number_of_fragments=3,
            pre_tags=['<mark>'],
            post_tags=['</mark>']
        )
    
    def _format_results(self, response) -> Dict[str, Any]:
        """Format Elasticsearch response including file metadata"""
        hits = []
        for hit in response:
            hit_data = {
                'id': hit.meta.id,
                'score': hit.meta.score,
                'name': getattr(hit, 'name', ''),
                'email': getattr(hit, 'email', ''),
                'phone': getattr(hit, 'phone', ''),
                'location': getattr(hit, 'location', ''),
                'current_employer': getattr(hit, 'current_employer', ''),
                'years_of_experience': getattr(hit, 'years_of_experience', 0),
                'skills': getattr(hit, 'skills', ''),
                'experience': getattr(hit, 'experience', '')[:200] + '...' if len(getattr(hit, 'experience', '')) > 200 else getattr(hit, 'experience', ''),
                'summary': getattr(hit, 'summary', ''),
                # File metadata (DTSearch-like features)
                'filename': getattr(hit, 'filename', ''),
                'file_type': getattr(hit, 'file_type', ''),
                'file_size': getattr(hit, 'file_size', 0),
                'file_size_mb': round(getattr(hit, 'file_size', 0) / 1048576, 2) if getattr(hit, 'file_size', 0) > 0 else 0,
                'indexed_date': getattr(hit, 'indexed_date', ''),
                'content_preview': getattr(hit, 'extracted_text', '')[:300] + '...' if len(getattr(hit, 'extracted_text', '')) > 300 else getattr(hit, 'extracted_text', ''),
                'highlights': {}
            }
            
            # Add highlights if available
            if hasattr(hit.meta, 'highlight'):
                hit_data['highlights'] = hit.meta.highlight.to_dict()
            
            hits.append(hit_data)
        
        return {
            'hits': hits,
            'total_hits': response.hits.total.value if hasattr(response.hits.total, 'value') else len(hits),
            'max_score': response.hits.max_score,
            'took': getattr(response, 'took', 0)
        }
    
    def _generate_cache_key(self, query: str, filters: Optional[Dict], 
                           page: int, page_size: int) -> str:
        """Generate cache key for search results"""
        key_data = f"{query}_{filters}_{page}_{page_size}"
        return f"search_cache_{hashlib.md5(key_data.encode()).hexdigest()}"
    
    def _empty_result(self) -> Dict[str, Any]:
        """Return empty search result"""
        return {
            'hits': [],
            'total_hits': 0,
            'max_score': 0,
            'took': 0
        }

# Global instance for easy import
search_service = SearchService()
