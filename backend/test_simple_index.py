#!/usr/bin/env python
"""
Simple test to add one CV to Elasticsearch
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

def test_simple_indexing():
    """Test adding one CV manually using direct Elasticsearch client"""
    
    # Connect to Elasticsearch
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    
    # Get one resume
    resume = Resume.objects.first()
    if not resume:
        print("No resumes found in database")
        return
    
    # Prepare document
    doc = {
        'id': str(resume.id),
        'name': f"{resume.first_name or ''} {resume.last_name or ''}".strip(),
        'email': resume.email or "",
        'phone': resume.phone_number or "",
        'skills': resume.skill_keywords or "",
        'experience': resume.expertise_details or "",
        'education': "",  # Not directly available in this model
        'location': resume.location or "",
        'current_employer': resume.current_employer or "",
        'years_of_experience': resume.years_of_experience or 0,
    }
    
    print(f"Adding resume: {resume.first_name} {resume.last_name} (ID: {resume.id})")
    print(f"Document: {json.dumps(doc, indent=2)}")
    
    # Index the document
    try:
        response = es.index(
            index='cv_documents',
            id=resume.id,
            body=doc
        )
        print(f"Success! Response: {response}")
        
        # Test search
        search_response = es.search(
            index='cv_documents',
            body={
                "query": {"match_all": {}}
            }
        )
        print(f"Search results: {search_response['hits']['total']}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_simple_indexing()
