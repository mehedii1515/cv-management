"""
Celery tasks for background CV indexing
Automatically index new CVs when they're uploaded or detected by QueryMind
"""
from celery import shared_task
from django.db import transaction
from apps.resumes.models import Resume
from apps.search.services import SearchService
from apps.search.documents import CVDocument
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def index_single_cv(self, resume_id):
    """
    Index a single CV in the background
    
    Args:
        resume_id: UUID of the resume to index
        
    Returns:
        dict: Result of indexing operation
    """
    try:
        resume = Resume.objects.get(id=resume_id)
        
        # Create document
        doc = CVDocument()
        doc.meta.id = resume.id
        
        # Set fields using the same logic as our management command
        doc.name = f"{resume.first_name or ''} {resume.last_name or ''}".strip()
        doc.email = resume.email or ''
        doc.phone = resume.phone_number or ''
        doc.skills = resume.skill_keywords or ''
        doc.experience = resume.expertise_details or ''
        doc.education = ''  # No direct education field in this model
        doc.summary = resume.expertise_areas or ''
        doc.location = resume.location or ''
        doc.current_employer = resume.current_employer or ''
        doc.years_of_experience = resume.years_of_experience or 0
        doc.sectors = resume.sectors or ''
        doc.linkedin_profile = resume.linkedin_profile or ''
        doc.languages_spoken = resume.languages_spoken or ''
        doc.professional_certifications = resume.professional_certifications or ''
        
        # Try to extract file content
        try:
            if resume.file_path:
                from pathlib import Path
                from django.core.files.storage import default_storage
                
                # Get the full file path
                if default_storage.exists(resume.file_path):
                    if hasattr(default_storage, 'path'):
                        # For local storage, get the actual file path
                        file_path = Path(default_storage.path(resume.file_path))
                    else:
                        # For other storage backends, use the file_path as is
                        file_path = Path(resume.file_path)
                    
                    if file_path.exists():
                        doc.file_content = doc.extract_file_content(str(file_path))
                    else:
                        doc.file_content = ""
                else:
                    doc.file_content = ""
            else:
                doc.file_content = ""
        except Exception as file_error:
            logger.warning(f"Could not extract content from file for resume {resume_id}: {file_error}")
            doc.file_content = ""
        
        # Save to Elasticsearch
        doc.save()
        
        logger.info(f"Successfully indexed CV {resume_id}: {resume.first_name} {resume.last_name}")
        
        return {
            'status': 'success',
            'resume_id': str(resume_id),
            'name': f"{resume.first_name} {resume.last_name}"
        }
        
    except Resume.DoesNotExist:
        logger.error(f"Resume {resume_id} does not exist")
        return {
            'status': 'error',
            'resume_id': str(resume_id),
            'error': 'Resume not found'
        }
        
    except Exception as e:
        logger.error(f"Failed to index CV {resume_id}: {e}")
        
        # Retry with exponential backoff
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=60 * (2 ** self.request.retries))
        
        return {
            'status': 'error',
            'resume_id': str(resume_id),
            'error': str(e)
        }


@shared_task
def bulk_index_cvs(resume_ids=None, batch_size=10):
    """
    Index multiple CVs in batches
    
    Args:
        resume_ids: List of resume IDs to index (None = all)
        batch_size: Number of CVs to process in each batch
        
    Returns:
        dict: Summary of indexing results
    """
    if resume_ids is None:
        queryset = Resume.objects.all()
    else:
        queryset = Resume.objects.filter(id__in=resume_ids)
    
    total = queryset.count()
    processed = 0
    errors = 0
    
    logger.info(f"Starting bulk indexing of {total} CVs")
    
    # Process in batches
    for i in range(0, total, batch_size):
        batch = queryset[i:i + batch_size]
        
        for resume in batch:
            try:
                # Call the single CV indexing task
                result = index_single_cv.apply_async(args=[resume.id])
                result.get()  # Wait for completion
                processed += 1
                
            except Exception as e:
                logger.error(f"Error processing resume {resume.id}: {e}")
                errors += 1
    
    result = {
        'status': 'completed',
        'total': total,
        'processed': processed,
        'errors': errors
    }
    
    logger.info(f"Bulk indexing completed: {result}")
    return result


@shared_task
def reindex_cv_on_update(resume_id):
    """
    Reindex a CV when it's updated
    This task is triggered when a CV is modified
    
    Args:
        resume_id: UUID of the updated resume
    """
    logger.info(f"Reindexing updated CV: {resume_id}")
    return index_single_cv.apply_async(args=[resume_id])


@shared_task
def delete_cv_from_index(resume_id):
    """
    Remove a CV from the search index when it's deleted
    
    Args:
        resume_id: UUID of the deleted resume
    """
    try:
        from elasticsearch import Elasticsearch
        
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        
        # Delete from Elasticsearch
        es.delete(index='cv_documents', id=str(resume_id), ignore=[404])
        
        logger.info(f"Removed CV {resume_id} from search index")
        
        return {
            'status': 'success',
            'resume_id': str(resume_id),
            'action': 'deleted'
        }
        
    except Exception as e:
        logger.error(f"Failed to delete CV {resume_id} from index: {e}")
        return {
            'status': 'error',
            'resume_id': str(resume_id),
            'error': str(e)
        }


@shared_task
def refresh_search_index():
    """
    Refresh the Elasticsearch index to make new documents immediately searchable
    This is useful after bulk operations
    """
    try:
        from elasticsearch import Elasticsearch
        
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        es.indices.refresh(index='cv_documents')
        
        logger.info("Search index refreshed")
        return {'status': 'success', 'action': 'index_refreshed'}
        
    except Exception as e:
        logger.error(f"Failed to refresh search index: {e}")
        return {'status': 'error', 'error': str(e)}


@shared_task
def monitor_querymind_integration():
    """
    Monitor QueryMind for new files and trigger indexing
    This task can be run periodically to check for new CVs detected by QueryMind
    """
    try:
        # Get recently added CVs (last 10 minutes)
        from django.utils import timezone
        from datetime import timedelta
        
        ten_minutes_ago = timezone.now() - timedelta(minutes=10)
        new_resumes = Resume.objects.filter(
            timestamp__gte=ten_minutes_ago,
            is_processed=True
        )
        
        indexed_count = 0
        
        for resume in new_resumes:
            # Check if already indexed by trying to search for it
            service = SearchService()
            existing = service.search_documents(f'id:{resume.id}')
            
            if existing['total_hits'] == 0:
                # Not indexed yet, queue for indexing
                index_single_cv.apply_async(args=[resume.id])
                indexed_count += 1
                logger.info(f"Queued new CV for indexing: {resume.id}")
        
        return {
            'status': 'success',
            'new_cvs_found': new_resumes.count(),
            'queued_for_indexing': indexed_count
        }
        
    except Exception as e:
        logger.error(f"QueryMind monitoring failed: {e}")
        return {'status': 'error', 'error': str(e)}
