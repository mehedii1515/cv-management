#!/usr/bin/env python3
"""
QueryMind-Search Integration Monitor
Run this to check the integration status
"""

import os, sys, django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_parser.settings')
django.setup()

from apps.resumes.models import Resume
from elasticsearch import Elasticsearch
from datetime import datetime

def monitor_integration():
    print(f"=== Integration Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    # Database status
    db_total = Resume.objects.count()
    db_processed = Resume.objects.filter(is_processed=True).count()
    print(f"📊 Database: {db_total} total, {db_processed} processed")
    
    # Elasticsearch status
    try:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        index_info = es.indices.stats(index='cv_documents')
        es_count = index_info['indices']['cv_documents']['total']['docs']['count']
        print(f"🔍 Search Index: {es_count} documents")
        
        # Check sync
        if db_processed == es_count:
            print("✅ Database and search index are in sync")
        else:
            print(f"⚠️  Sync issue: DB has {db_processed}, index has {es_count}")
            
    except Exception as e:
        print(f"❌ Elasticsearch error: {e}")
    
    print()

if __name__ == "__main__":
    monitor_integration()
