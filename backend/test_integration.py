#!/usr/bin/env python
"""
Simple test of the QueryMind-Search integration
"""
import os
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_parser.settings')
django.setup()

from apps.resumes.models import Resume
from apps.search.services import SearchService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_integration():
    """Test the integration between Resume model and Search system"""
    
    logger.info("=== TESTING QUERYMIND-SEARCH INTEGRATION ===")
    
    # 1. Check database
    total_resumes = Resume.objects.count()
    processed_resumes = Resume.objects.filter(is_processed=True).count()
    
    logger.info(f"Database: {total_resumes} total CVs, {processed_resumes} processed")
    
    # 2. Check search index
    service = SearchService()
    
    # Test search for all CVs
    all_search = service.search_documents('')  # Empty query should return all
    if all_search['total_hits'] == 0:
        # Try different approach
        from elasticsearch import Elasticsearch
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        count_result = es.count(index='cv_documents')
        indexed_count = count_result['count']
        logger.info(f"Search Index: {indexed_count} documents indexed (direct ES count)")
    else:
        indexed_count = all_search['total_hits']
        logger.info(f"Search Index: {indexed_count} documents indexed")
    
    # 3. Check sync status
    # indexed_count is set above
    
    if indexed_count == processed_resumes:
        logger.info("✅ Database and search index are in sync!")
    else:
        logger.warning(f"⚠️  Sync issue: DB has {processed_resumes} processed CVs, index has {indexed_count}")
    
    # 4. Test search functionality
    test_searches = ['Ahmed', 'project management', 'development', 'engineer']
    
    for query in test_searches:
        result = service.search_documents(query)
        logger.info(f"Search '{query}': {result['total_hits']} results")
    
    # 5. Test recent CVs
    from django.utils import timezone
    from datetime import timedelta
    
    recent_cvs = Resume.objects.filter(
        timestamp__gte=timezone.now() - timedelta(hours=24),
        is_processed=True
    )
    
    logger.info(f"Recent CVs (24h): {recent_cvs.count()} new processed CVs")
    
    logger.info("=== INTEGRATION TEST COMPLETE ===")

if __name__ == "__main__":
    test_integration()
