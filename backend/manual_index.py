#!/usr/bin/env python
"""
Manual script to index CVs into Elasticsearch
This script bypasses the django-elasticsearch-dsl timeout issues
"""
import os
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_parser.settings')
django.setup()

from apps.resumes.models import Resume
from apps.search.documents import CVDocument
from elasticsearch_dsl import connections
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def index_cvs_manually():
    """Index CVs manually with better error handling and progress tracking"""
    
    # Get all resumes
    resumes = Resume.objects.all()
    total_count = resumes.count()
    
    logger.info(f"Found {total_count} CVs to index")
    
    if total_count == 0:
        logger.info("No CVs found in database")
        return
    
    # Create index if it doesn't exist
    try:
        CVDocument._index.create()
        logger.info("Index created successfully")
    except Exception as e:
        logger.info(f"Index might already exist: {e}")
    
    # Index documents in batches
    batch_size = 10
    indexed_count = 0
    error_count = 0
    
    for i in range(0, total_count, batch_size):
        batch = resumes[i:i + batch_size]
        logger.info(f"Processing batch {i//batch_size + 1}/{(total_count + batch_size - 1)//batch_size}")
        
        for resume in batch:
            try:
                # Create document
                doc = CVDocument()
                doc.meta.id = resume.id
                
                # Set fields
                doc.name = resume.name or ""
                doc.email = resume.email or ""
                doc.phone = resume.phone or ""
                doc.skills = resume.skills or ""
                doc.experience = resume.experience or ""
                doc.education = resume.education or ""
                doc.summary = resume.summary or ""
                
                # Try to extract file content
                try:
                    if resume.cv_file and hasattr(resume.cv_file, 'path'):
                        file_path = Path(resume.cv_file.path)
                        if file_path.exists():
                            doc.file_content = doc.extract_file_content(str(file_path))
                        else:
                            doc.file_content = ""
                    else:
                        doc.file_content = ""
                except Exception as file_error:
                    logger.warning(f"Could not extract content from file for resume {resume.id}: {file_error}")
                    doc.file_content = ""
                
                # Save document
                doc.save()
                indexed_count += 1
                logger.info(f"Indexed CV {resume.id}: {resume.name}")
                
            except Exception as e:
                error_count += 1
                logger.error(f"Error indexing CV {resume.id}: {e}")
                continue
    
    logger.info(f"Indexing complete: {indexed_count} indexed, {error_count} errors")

if __name__ == "__main__":
    index_cvs_manually()
