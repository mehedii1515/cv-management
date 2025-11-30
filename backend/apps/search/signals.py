"""
Django signals for automatic CV indexing
Automatically trigger search indexing when CVs are cre            if not created and instance.is_processed:
                logger.info(f"CV processing completed: {instance.id} - queuing for indexing")
                index_single_cv.apply_async(args=[instance.id])
                
                # Also index the file for file search
                if instance.file_path:
                    logger.info(f"CV file processing completed: {instance.file_path} - queuing for file indexing")
                    index_resume_file.apply_async(args=[instance.id])dated, or deleted
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
    This includes both resume database indexing and file content indexing
    
    Args:
        sender: Resume model class
        instance: Resume instance that was saved
        created: Boolean indicating if this is a new record
        **kwargs: Additional keyword arguments
    """
    try:
        # Debug logging - use print to bypass logging level issues
        print(f"🔥 SIGNAL FIRED: resume {instance.id}, created={created}, is_processed={instance.is_processed}, file_path={instance.file_path}")
        
        # Import here to avoid circular imports
        from apps.search.tasks import index_single_cv, index_resume_file
        
        # Only index if the CV is processed
        if instance.is_processed:
            if created:
                print(f"📝 New CV created: {instance.id} - queuing for indexing")
                # For eager execution, don't use countdown as it may cause issues
                index_single_cv.apply_async(args=[instance.id])
                
                # Also index the file for file search
                if instance.file_path:
                    print(f"📁 New CV file: {instance.file_path} - queuing for file indexing")
                    result = index_resume_file.apply_async(args=[instance.id])
                    print(f"✅ File indexing task result: {result}")
            else:
                print(f"🔄 CV updated: {instance.id} - queuing for reindexing")
                # Reindex immediately for updates
                index_single_cv.apply_async(args=[instance.id])
                
                # Also reindex the file
                if instance.file_path:
                    print(f"📁 CV file updated: {instance.file_path} - queuing for file reindexing")
                    result = index_resume_file.apply_async(args=[instance.id])
                    print(f"✅ File reindexing task result: {result}")
        else:
            print(f"⏳ CV {instance.id} not yet processed - skipping indexing")
            
    except Exception as e:
        logger.error(f"Failed to queue CV {instance.id} for indexing: {e}")


@receiver(post_delete, sender=Resume)
def remove_cv_from_index(sender, instance, **kwargs):
    """
    Automatically remove CV from search index when deleted
    This includes both resume database index and file index
    
    Args:
        sender: Resume model class
        instance: Resume instance that was deleted
        **kwargs: Additional keyword arguments
    """
    try:
        # Import here to avoid circular imports
        from apps.search.tasks import delete_cv_from_index, delete_resume_file_from_index
        
        logger.info(f"CV deleted: {instance.id} - removing from search indexes")
        
        # Remove from CV database index
        delete_cv_from_index.apply_async(args=[instance.id])
        
        # Remove from file index if there was a file
        if instance.file_path:
            logger.info(f"CV file deleted: {instance.file_path} - removing from file index")
            delete_resume_file_from_index.apply_async(args=[instance.file_path])
        
    except Exception as e:
        logger.error(f"Failed to queue CV {instance.id} for deletion from indexes: {e}")


# Additional signal for when CV processing is completed
@receiver(post_save, sender=Resume)
def index_on_processing_complete(sender, instance, created, **kwargs):
    """
    Index CV when processing status changes to completed
    This handles cases where CVs are uploaded but processing happens later
    Includes both resume database indexing and file indexing
    """
    if not created and instance.is_processed:
        # Check if processing status just changed
        try:
            from apps.search.tasks import index_single_cv, index_resume_file
            
            # Get the previous state from database
            old_instance = Resume.objects.get(id=instance.id)
            if not old_instance.is_processed and instance.is_processed:
                logger.info(f"CV processing completed: {instance.id} - queuing for indexing")
                index_single_cv.apply_async(args=[instance.id], countdown=2)
                
                # Also index the file for file search
                if instance.file_path:
                    logger.info(f"CV file processing completed: {instance.file_path} - queuing for file indexing")
                    index_resume_file.apply_async(args=[instance.id], countdown=4)
                
        except Exception as e:
            logger.error(f"Error checking processing status for CV {instance.id}: {e}")
