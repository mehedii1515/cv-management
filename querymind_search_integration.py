"""
Integration script to connect QueryMind file detection with CV search indexing
This script bridges QueryMind's file monitoring with our Elasticsearch search system
"""
import os
import sys
import django
from pathlib import Path
import json
import hashlib
import time
from datetime import datetime

# Setup Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_parser.settings')
django.setup()

from apps.resumes.models import Resume
from apps.search.tasks import index_single_cv, refresh_search_index
import logging

logger = logging.getLogger(__name__)


class QueryMindSearchIntegration:
    """
    Integration class to connect QueryMind with the search system
    """
    
    def __init__(self, querymind_config_path=None):
        self.querymind_dir = BASE_DIR / 'QueryMind'
        self.processed_files_path = self.querymind_dir / 'processed_files.json'
        self.config_path = querymind_config_path or self.querymind_dir / 'watcher_config.py'
        
        # Load processed files tracking
        self.processed_files = self.load_processed_files()
        
    def load_processed_files(self):
        """Load the list of files already processed by QueryMind"""
        try:
            if self.processed_files_path.exists():
                with open(self.processed_files_path, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading processed files: {e}")
            return {}
    
    def save_processed_files(self):
        """Save the processed files tracking"""
        try:
            with open(self.processed_files_path, 'w') as f:
                json.dump(self.processed_files, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving processed files: {e}")
    
    def get_file_hash(self, file_path):
        """Generate a hash for a file to track changes"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Error hashing file {file_path}: {e}")
            return None
    
    def scan_for_new_cvs(self):
        """
        Scan for new CV files and trigger indexing
        This method should be called periodically
        """
        new_files = []
        updated_files = []
        
        # Check QueryMind's DROPPED PROJECTS folder
        dropped_folder = self.querymind_dir / 'DROPPED PROJECTS'
        
        if dropped_folder.exists():
            for file_path in dropped_folder.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.doc', '.docx', '.txt']:
                    file_key = str(file_path.relative_to(self.querymind_dir))
                    current_hash = self.get_file_hash(file_path)
                    
                    if current_hash:
                        if file_key not in self.processed_files:
                            # New file
                            new_files.append(file_path)
                            self.processed_files[file_key] = {
                                'hash': current_hash,
                                'processed_date': datetime.now().isoformat(),
                                'status': 'detected'
                            }
                        elif self.processed_files[file_key]['hash'] != current_hash:
                            # File was updated
                            updated_files.append(file_path)
                            self.processed_files[file_key]['hash'] = current_hash
                            self.processed_files[file_key]['last_updated'] = datetime.now().isoformat()
        
        logger.info(f"Scan complete: {len(new_files)} new files, {len(updated_files)} updated files")
        
        return new_files, updated_files
    
    def trigger_cv_processing(self, file_paths):
        """
        Trigger CV processing for new files
        This simulates what QueryMind would do when it detects new files
        """
        for file_path in file_paths:
            try:
                logger.info(f"Processing CV: {file_path}")
                
                # Here you would typically call your existing CV processing pipeline
                # For now, we'll just check if a Resume record exists for this file
                
                # Try to find existing resume by filename
                filename = file_path.name
                existing_resume = Resume.objects.filter(
                    original_filename__icontains=filename
                ).first()
                
                if existing_resume and existing_resume.is_processed:
                    # Resume exists and is processed, trigger indexing
                    logger.info(f"Found existing processed resume {existing_resume.id}, triggering indexing")
                    
                    # Use Celery if available, otherwise direct indexing
                    try:
                        index_single_cv.apply_async(args=[existing_resume.id])
                        logger.info(f"Queued CV {existing_resume.id} for background indexing")
                    except Exception as e:
                        logger.warning(f"Celery not available, attempting direct indexing: {e}")
                        # Direct indexing fallback
                        from apps.search.services import SearchService
                        service = SearchService()
                        # Implementation would go here
                        
                else:
                    logger.info(f"No processed resume found for {filename}")
                    
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
    
    def sync_with_database(self):
        """
        Sync processed CVs with the search index
        Ensure all processed CVs in the database are indexed
        """
        try:
            # Get all processed resumes that might not be indexed
            processed_resumes = Resume.objects.filter(is_processed=True)
            
            logger.info(f"Checking {processed_resumes.count()} processed resumes for indexing")
            
            # Check each resume against the search index
            from apps.search.services import SearchService
            service = SearchService()
            
            needs_indexing = []
            
            for resume in processed_resumes:
                # Quick check if resume is in search index
                search_result = service.search_documents(f'id:{resume.id}')
                
                if search_result['total_hits'] == 0:
                    needs_indexing.append(resume.id)
            
            if needs_indexing:
                logger.info(f"Found {len(needs_indexing)} resumes that need indexing")
                
                # Trigger background indexing
                for resume_id in needs_indexing[:10]:  # Limit to 10 at a time
                    try:
                        index_single_cv.apply_async(args=[resume_id])
                        logger.info(f"Queued resume {resume_id} for indexing")
                    except Exception as e:
                        logger.error(f"Failed to queue resume {resume_id}: {e}")
            else:
                logger.info("All processed resumes are indexed")
                
        except Exception as e:
            logger.error(f"Error during database sync: {e}")
    
    def run_integration_cycle(self):
        """
        Run a complete integration cycle
        1. Scan for new files
        2. Process new CVs
        3. Sync with database
        4. Update tracking
        """
        logger.info("Starting QueryMind-Search integration cycle")
        
        try:
            # 1. Scan for new files
            new_files, updated_files = self.scan_for_new_cvs()
            
            # 2. Process new files
            if new_files:
                self.trigger_cv_processing(new_files)
            
            # 3. Process updated files
            if updated_files:
                self.trigger_cv_processing(updated_files)
            
            # 4. Sync database with search index
            self.sync_with_database()
            
            # 5. Save tracking information
            self.save_processed_files()
            
            # 6. Refresh search index
            try:
                refresh_search_index.apply_async()
                logger.info("Triggered search index refresh")
            except Exception as e:
                logger.warning(f"Could not trigger index refresh: {e}")
            
            logger.info("Integration cycle completed successfully")
            
        except Exception as e:
            logger.error(f"Integration cycle failed: {e}")


def main():
    """Main function to run the integration"""
    integration = QueryMindSearchIntegration()
    integration.run_integration_cycle()


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    main()
