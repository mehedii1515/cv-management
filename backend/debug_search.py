#!/usr/bin/env python
"""
Debug script to test search functionality
"""
import os
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_parser.settings')
django.setup()

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

def debug_search():
    """Debug search functionality"""
    
    # Test direct Elasticsearch connection
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    
    print("=== DEBUGGING SEARCH ===")
    
    # 1. Test connection
    print(f"1. ES Connection: {es.ping()}")
    
    # 2. Check index exists
    index_exists = es.indices.exists(index='cv_documents')
    print(f"2. Index exists: {index_exists}")
    
    # 3. Get document count
    if index_exists:
        doc_count = es.count(index='cv_documents')
        print(f"3. Document count: {doc_count['count']}")
        
        # 4. Get sample document
        search_all = es.search(index='cv_documents', body={"query": {"match_all": {}}, "size": 1})
        if search_all['hits']['hits']:
            sample_doc = search_all['hits']['hits'][0]['_source']
            print(f"4. Sample document fields: {list(sample_doc.keys())}")
            print(f"   Name field: '{sample_doc.get('name', 'MISSING')}'")
        
        # 5. Test direct search for "Ahmed"
        search_ahmed = es.search(index='cv_documents', body={
            "query": {
                "multi_match": {
                    "query": "Ahmed",
                    "fields": ["name", "file_content", "skills", "experience"]
                }
            }
        })
        print(f"5. Direct ES search for 'Ahmed': {search_ahmed['hits']['total']['value']} results")
        
        # 6. Test django-elasticsearch-dsl Search
        from elasticsearch_dsl import Search
        search = Search(using=es, index='cv_documents')
        search = search.query('multi_match', query='Ahmed', fields=['name', 'file_content', 'skills', 'experience'])
        response = search.execute()
        print(f"6. DSL search for 'Ahmed': {response.hits.total.value} results")
        
        # 7. Test our SearchService
        from apps.search.services import SearchService
        service = SearchService()
        results = service.search_documents('Ahmed')
        print(f"7. SearchService search for 'Ahmed': {results['total_hits']} results")
        
        # 8. Check if cache is interfering
        from django.core.cache import cache
        cache.clear()
        print("8. Cleared cache")
        
        # 9. Test again after cache clear
        results2 = service.search_documents('Ahmed')
        print(f"9. SearchService search after cache clear: {results2['total_hits']} results")
    
    print("=== DEBUG COMPLETE ===")

if __name__ == "__main__":
    debug_search()
