#!/usr/bin/env python
"""
Simple script to add one CV document at a time to avoid timeout issues
"""
import os
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_parser.settings')
django.setup()

from apps.resumes.models import Resume
from elasticsearch import Elasticsearch
import json

def add_single_document():
    """Add a single CV document to test indexing"""
    
    # Get the first resume
    try:
        resume = Resume.objects.first()
        if not resume:
            print("No resumes found in database")
            return
        
        print(f"Found resume: {resume.first_name} {resume.last_name}")
        
        # Create Elasticsearch client with increased timeout
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}], timeout=30)
        
        # Prepare document
        doc = {
            'name': f"{resume.first_name or ''} {resume.last_name or ''}".strip(),
            'email': resume.email or '',
            'phone': resume.phone_number or '',
            'skills': resume.skill_keywords or '',
            'experience': resume.expertise_details or '',
            'education': '',  # No direct education field in this model
            'summary': resume.expertise_areas or '',
            'file_content': '',  # We'll skip file content for now to avoid issues
        }
        
        # Index the document
        result = es.index(
            index='cv_documents',
            id=str(resume.id),
            body=doc
        )
        
        print(f"Successfully indexed document: {result}")
        
        # Test search
        search_result = es.search(
            index='cv_documents',
            body={
                "query": {"match_all": {}}
            }
        )
        
        print(f"Search result: {search_result['hits']['total']}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_single_document()
