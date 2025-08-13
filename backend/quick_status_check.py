#!/usr/bin/env python3
"""
Quick status check for the search system integration
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_parser.settings')
django.setup()

def check_database():
    """Check database status"""
    try:
        from apps.resumes.models import Resume
        total_resumes = Resume.objects.count()
        processed_resumes = Resume.objects.filter(is_processed=True).count()
        print(f"📊 Database Status:")
        print(f"   Total Resumes: {total_resumes}")
        print(f"   Processed Resumes: {processed_resumes}")
        return True
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return False

def check_elasticsearch():
    """Check Elasticsearch status"""
    try:
        from elasticsearch import Elasticsearch
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        
        # Quick health check
        if es.ping():
            print(f"✅ Elasticsearch Connected")
        else:
            print(f"❌ Elasticsearch Not Responding")
            return False
            
        # Check index
        index_info = es.indices.stats(index='cv_documents')
        doc_count = index_info['indices']['cv_documents']['total']['docs']['count']
        print(f"📈 Elasticsearch Index: {doc_count} documents")
        return True
        
    except Exception as e:
        print(f"❌ Elasticsearch Error: {e}")
        return False

def check_search_api():
    """Test search API"""
    try:
        from apps.search.services import SearchService
        service = SearchService()
        
        # Test search
        results = service.search_documents('python', page_size=3)
        print(f"🔍 Search Test: Found {results['total_hits']} total results for 'python'")
        
        if results['hits']:
            print(f"   Sample result: {results['hits'][0].get('name', 'Unknown')}")
        
        return True
    except Exception as e:
        print(f"❌ Search API Error: {e}")
        return False

def main():
    print("🚀 Resume Parser Search System - Quick Status Check")
    print("=" * 60)
    
    # Run checks
    db_ok = check_database()
    es_ok = check_elasticsearch()
    api_ok = check_search_api()
    
    print("=" * 60)
    if db_ok and es_ok and api_ok:
        print("✅ All systems operational!")
        print("\n🎯 Next steps:")
        print("   1. Start Celery worker: celery -A resume_parser worker --loglevel=info")
        print("   2. Test QueryMind integration")
        print("   3. Deploy to production")
    else:
        print("❌ Some systems need attention")

if __name__ == "__main__":
    main()
