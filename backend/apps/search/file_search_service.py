"""
Pure File Search Service
Handles searching through indexed files directly (not database records)
"""
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from django.core.cache import cache
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from .file_documents import FileDocument

logger = logging.getLogger(__name__)

class FileSearchService:
    """Service for searching indexed files directly"""
    
    def __init__(self):
        self.es_client = self._get_es_client()
        self.index_name = 'file_index'
    
    def _get_es_client(self):
        """Get Elasticsearch client"""
        try:
            es_host = getattr(settings, 'ELASTICSEARCH_HOST', 'localhost')
            es_port = getattr(settings, 'ELASTICSEARCH_PORT', 9200)
            
            client = Elasticsearch([f'{es_host}:{es_port}'])
            if client.ping():
                return client
            else:
                logger.error("Cannot connect to Elasticsearch")
                return None
        except Exception as e:
            logger.error(f"Elasticsearch connection error: {e}")
            return None
    
    def index_file(self, file_path: str, base_directory: str = None) -> bool:
        """Index a single file"""
        try:
            if not self.es_client:
                return False
                
            doc = FileDocument.create_from_file(file_path, base_directory)
            if doc:
                doc.save(using=self.es_client, index=self.index_name)
                logger.info(f"Indexed file: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error indexing file {file_path}: {e}")
            return False
    
    def index_directory(self, directory_path: str, recursive: bool = True, 
                       file_extensions: List[str] = None) -> Dict[str, Any]:
        """Index all files in a directory"""
        if file_extensions is None:
            file_extensions = ['.pdf', '.docx', '.doc', '.txt', '.rtf']
            
        indexed_count = 0
        failed_count = 0
        skipped_count = 0
        
        try:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = os.path.splitext(file)[1].lower()
                    
                    if file_ext in file_extensions:
                        # Check if file already indexed (by hash)
                        if self.is_file_indexed(file_path):
                            skipped_count += 1
                            continue
                            
                        if self.index_file(file_path, directory_path):
                            indexed_count += 1
                        else:
                            failed_count += 1
                    
                if not recursive:
                    break
                    
        except Exception as e:
            logger.error(f"Error indexing directory {directory_path}: {e}")
            
        return {
            'indexed': indexed_count,
            'failed': failed_count,
            'skipped': skipped_count,
            'total_processed': indexed_count + failed_count + skipped_count
        }
    
    def search_files(self, query: str, filters: Dict = None, 
                    page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """Search indexed files"""
        if not self.es_client or not query.strip():
            return self._empty_result()
            
        # Check cache
        cache_key = self._generate_cache_key(query, filters, page, page_size)
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
            
        try:
            search = Search(using=self.es_client, index=self.index_name)
            
            # Build query - search in file content and filename
            search = search.query(
                'multi_match',
                query=query,
                fields=[
                    'content^3.0',           # File content (highest priority)
                    'filename^2.0',          # Filename
                    'relative_path^1.0'      # File path
                ],
                type='best_fields',
                minimum_should_match='75%'
            )
            
            # Apply filters
            if filters:
                search = self._apply_file_filters(search, filters)
            
            # Add highlighting
            search = search.highlight(
                'content',
                'filename', 
                'relative_path',
                fragment_size=200,
                number_of_fragments=3,
                pre_tags=['<mark>'],
                post_tags=['</mark>']
            )
            
            # Pagination
            start = (page - 1) * page_size
            search = search[start:start + page_size]
            
            # Execute search
            response = search.execute()
            
            # Format results
            result = self._format_file_results(response, query)
            
            # Cache results
            cache.set(cache_key, result, 300)  # 5 minutes
            
            return result
            
        except Exception as e:
            logger.error(f"File search failed for query '{query}': {e}")
            return self._empty_result()
    
    def boolean_search_files(self, query: str, filters: Dict = None,
                           page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """Boolean search in files with AND/OR/NOT operators"""
        if not self.es_client or not query.strip():
            return self._empty_result()
            
        try:
            search = Search(using=self.es_client, index=self.index_name)
            
            # Build boolean query
            search = search.query(
                'query_string',
                query=query,
                fields=['content^3.0', 'filename^2.0', 'relative_path^1.0'],
                default_operator='AND'
            )
            
            # Apply filters
            if filters:
                search = self._apply_file_filters(search, filters)
                
            # Add highlighting
            search = search.highlight(
                'content',
                'filename',
                'relative_path',
                fragment_size=200,
                number_of_fragments=3,
                pre_tags=['<mark>'],
                post_tags=['</mark>']
            )
            
            # Pagination
            start = (page - 1) * page_size
            search = search[start:start + page_size]
            
            # Execute search
            response = search.execute()
            
            return self._format_file_results(response, query, search_type='boolean')
            
        except Exception as e:
            logger.error(f"Boolean file search failed for query '{query}': {e}")
            return self._empty_result()
    
    def _apply_file_filters(self, search: Search, filters: Dict) -> Search:
        """Apply filters specific to files"""
        if filters.get('file_extension'):
            search = search.filter('term', file_extension=filters['file_extension'])
            

            
        if filters.get('min_size'):
            search = search.filter('range', file_size={'gte': filters['min_size']})
            
        if filters.get('max_size'):
            search = search.filter('range', file_size={'lte': filters['max_size']})
            
        if filters.get('directory'):
            search = search.filter('term', directory_path=filters['directory'])
            
        if filters.get('date_from'):
            search = search.filter('range', modified_date={'gte': filters['date_from']})
            
        if filters.get('date_to'):
            search = search.filter('range', modified_date={'lte': filters['date_to']})
            

            
        return search
    
    def _format_file_results(self, response, query: str, search_type: str = 'basic') -> Dict[str, Any]:
        """Format file search results"""
        files = []
        
        for hit in response:
            file_data = {
                'file_id': hit.meta.id,
                'score': hit.meta.score,
                'filename': getattr(hit, 'filename', ''),
                'file_path': getattr(hit, 'file_path', ''),
                'relative_path': getattr(hit, 'relative_path', ''),
                'file_extension': getattr(hit, 'file_extension', ''),
                'file_size': getattr(hit, 'file_size', 0),
                'file_size_formatted': self._format_file_size(getattr(hit, 'file_size', 0)),
                'created_date': getattr(hit, 'created_date', ''),
                'modified_date': getattr(hit, 'modified_date', ''),
                'indexed_date': getattr(hit, 'indexed_date', ''),
                'page_count': getattr(hit, 'page_count', 1),
                'word_count': getattr(hit, 'word_count', 0),
                'language': getattr(hit, 'language', ''),
                'directory': getattr(hit, 'directory_path', ''),
                'content_preview': self._get_content_preview(getattr(hit, 'content', ''), query),
                'highlights': {}
            }
            
            # Add highlights
            if hasattr(hit.meta, 'highlight'):
                file_data['highlights'] = hit.meta.highlight.to_dict()
                
            files.append(file_data)
        
        return {
            'files': files,
            'total_files': response.hits.total.value if hasattr(response.hits.total, 'value') else len(files),
            'max_score': response.hits.max_score,
            'took': response.took,
            'search_info': {
                'query': query,
                'search_type': search_type,
                'index_name': self.index_name,
                'total_indexed_files': self.get_total_indexed_files(),
                'file_extensions_found': list(set([f.get('file_extension', '') for f in files if f.get('file_extension')])),
                'categories_found': list(set([f.get('file_category', '') for f in files if f.get('file_category')])),
                'search_time_ms': response.took
            }
        }
    
    def get_file_suggestions(self, partial_query: str, limit: int = 10) -> List[str]:
        """Get file search suggestions"""
        if not self.es_client or len(partial_query) < 2:
            return []
            
        try:
            search = Search(using=self.es_client, index=self.index_name)
            
            # Search in filenames and content for suggestions
            search = search.query(
                'match_phrase_prefix',
                content=partial_query
            )
            
            search = search.source(['filename', 'content'])[:limit]
            response = search.execute()
            
            suggestions = set()
            for hit in response:
                # Extract relevant phrases from content
                content = getattr(hit, 'content', '')
                words = content.lower().split()
                
                # Find phrases starting with partial query
                query_lower = partial_query.lower()
                for i, word in enumerate(words):
                    if word.startswith(query_lower):
                        phrase = ' '.join(words[i:i+3])  # 3-word phrases
                        if len(phrase) > len(partial_query):
                            suggestions.add(phrase)
                            
                if len(suggestions) >= limit:
                    break
                    
            return list(suggestions)[:limit]
            
        except Exception as e:
            logger.error(f"File suggestions failed: {e}")
            return []
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get file search system status"""
        try:
            if not self.es_client:
                return {
                    'elasticsearch_connected': False,
                    'file_search_ready': False,
                    'index_name': self.index_name
                }
                
            # Check index exists
            index_exists = self.es_client.indices.exists(index=self.index_name)
            
            status = {
                'elasticsearch_connected': True,
                'file_search_ready': index_exists,
                'index_name': self.index_name,
                'total_files': self.get_total_indexed_files() if index_exists else 0
            }
            
            if index_exists:
                index_stats = self.es_client.indices.stats(index=self.index_name)
                status.update({
                    'index_size_bytes': index_stats['indices'][self.index_name]['total']['store']['size_in_bytes'],
                    'index_size_mb': round(index_stats['indices'][self.index_name]['total']['store']['size_in_bytes'] / 1048576, 2)
                })
                
            return status
            
        except Exception as e:
            logger.error(f"Status check failed: {e}")
            return {
                'elasticsearch_connected': False,
                'file_search_ready': False,
                'error': str(e)
            }
    
    def get_total_indexed_files(self) -> int:
        """Get total number of indexed files"""
        try:
            if not self.es_client:
                return 0
            search = Search(using=self.es_client, index=self.index_name)
            return search.count()
        except:
            return 0
    
    def is_file_indexed(self, file_path: str) -> bool:
        """Check if a file is already indexed"""
        try:
            file_hash = FileDocument.generate_file_hash(file_path)
            if not file_hash:
                return False
                
            search = Search(using=self.es_client, index=self.index_name)
            search = search.filter('term', file_hash=file_hash)
            return search.count() > 0
        except:
            return False
    
    def delete_file_from_index(self, file_path: str) -> bool:
        """Remove a file from the index"""
        try:
            file_hash = FileDocument.generate_file_hash(file_path)
            if file_hash:
                self.es_client.delete(index=self.index_name, id=file_hash)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file from index: {e}")
            return False
    
    def create_file_index(self) -> bool:
        """Create the file index"""
        try:
            FileDocument._index.delete(using=self.es_client, ignore=404)
            FileDocument.init(using=self.es_client)
            return True
        except Exception as e:
            logger.error(f"Failed to create file index: {e}")
            return False
    
    def _get_content_preview(self, content: str, query: str, max_length: int = 300) -> str:
        """Get content preview around query terms"""
        if not content:
            return ""
            
        query_lower = query.lower()
        content_lower = content.lower()
        
        # Find first occurrence of query
        index = content_lower.find(query_lower)
        if index == -1:
            # Return beginning of content if query not found
            return content[:max_length] + ('...' if len(content) > max_length else '')
        
        # Get text around the query
        start = max(0, index - 100)
        end = min(len(content), index + max_length - 100)
        
        preview = content[start:end]
        if start > 0:
            preview = '...' + preview
        if end < len(content):
            preview = preview + '...'
            
        return preview
    
    def _format_file_size(self, bytes_size: int) -> str:
        """Format file size in human readable format"""
        if bytes_size == 0:
            return "0 B"
        
        sizes = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while bytes_size >= 1024 and i < len(sizes) - 1:
            bytes_size /= 1024.0
            i += 1
        
        return f"{bytes_size:.1f} {sizes[i]}"
    
    def _generate_cache_key(self, query: str, filters: Dict, page: int, page_size: int) -> str:
        """Generate cache key for search results"""
        import hashlib
        key_data = f"file_search:{query}:{str(filters)}:{page}:{page_size}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _empty_result(self) -> Dict[str, Any]:
        """Return empty search result"""
        return {
            'files': [],
            'total_files': 0,
            'max_score': 0,
            'took': 0,
            'search_info': {
                'query': '',
                'search_type': 'empty',
                'index_name': self.index_name,
                'total_indexed_files': 0,
                'file_extensions_found': [],
                'categories_found': [],
                'search_time_ms': 0
            }
        }
