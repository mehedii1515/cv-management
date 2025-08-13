"""
Django signals for automatic CV indexing
Automatically trigger search indexing when CVs are created, updated, or deleted
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.resumes.models import Resume
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Resume)
def index_cv_on_save(sender, instance, created, **kwargs):
    """
    Automatically index CV when it's created or updated
    
    Args:
        sender: Resume model class
        instance: Resume instance that was saved
        created: Boolean indicating if this is a new record
        **kwargs: Additional keyword arguments
    """
    try:
        # Import here to avoid circular imports
        from apps.search.tasks import index_single_cv
        
        # Only index if the CV is processed
        if instance.is_processed:
            if created:
                logger.info(f"New CV created: {instance.id} - queuing for indexing")
                # Delay slightly to ensure the file is fully saved
                index_single_cv.apply_async(args=[instance.id], countdown=5)
            else:
                logger.info(f"CV updated: {instance.id} - queuing for reindexing")
                # Reindex immediately for updates
                index_single_cv.apply_async(args=[instance.id])
        else:
            logger.info(f"CV {instance.id} not yet processed - skipping indexing")
            
    except Exception as e:
        logger.error(f"Failed to queue CV {instance.id} for indexing: {e}")


@receiver(post_delete, sender=Resume)
def remove_cv_from_index(sender, instance, **kwargs):
    """
    Automatically remove CV from search index when deleted
    
    Args:
        sender: Resume model class
        instance: Resume instance that was deleted
        **kwargs: Additional keyword arguments
    """
    try:
        # Import here to avoid circular imports
        from apps.search.tasks import delete_cv_from_index
        
        logger.info(f"CV deleted: {instance.id} - removing from search index")
        delete_cv_from_index.apply_async(args=[instance.id])
        
    except Exception as e:
        logger.error(f"Failed to queue CV {instance.id} for deletion from index: {e}")


# Additional signal for when CV processing is completed
@receiver(post_save, sender=Resume)
def index_on_processing_complete(sender, instance, created, **kwargs):
    """
    Index CV when processing status changes to completed
    This handles cases where CVs are uploaded but processing happens later
    """
    if not created and instance.is_processed:
        # Check if processing status just changed
        try:
            from apps.search.tasks import index_single_cv
            
            # Get the previous state from database
            old_instance = Resume.objects.get(id=instance.id)
            if not old_instance.is_processed and instance.is_processed:
                logger.info(f"CV processing completed: {instance.id} - queuing for indexing")
                index_single_cv.apply_async(args=[instance.id], countdown=2)
                
        except Exception as e:
            logger.error(f"Error checking processing status for CV {instance.id}: {e}")
