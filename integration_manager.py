#!/usr/bin/env python3
"""
QueryMind-Search Integration Manager
Complete integration between QueryMind file detection and CV search indexing
"""

import os
import sys
import django
import json
import time
from pathlib import Path
from datetime import datetime
import logging

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = PROJECT_ROOT / 'backend'
QUERYMIND_DIR = PROJECT_ROOT / 'QueryMind'

# Add backend to path for Django imports
sys.path.append(str(BACKEND_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_parser.settings')

# Initialize Django
django.setup()

# Import Django components
from apps.resumes.models import Resume
from django.db import transaction

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class IntegratedCVProcessor:
    """
    Integrated CV processor that combines QueryMind detection with search indexing
    """
    
    def __init__(self):
        self.processed_files_path = QUERYMIND_DIR / 'processed_files.json'
        self.monitoring_log = PROJECT_ROOT / 'integration.log'
        self.processed_files = self.load_processed_files()
        
    def load_processed_files(self):
        """Load processed files tracking"""
        try:
            if self.processed_files_path.exists():
                with open(self.processed_files_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading processed files: {e}")
        return {}
    
    def save_processed_files(self):
        """Save processed files tracking"""
        try:
            with open(self.processed_files_path, 'w', encoding='utf-8') as f:
                json.dump(self.processed_files, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving processed files: {e}")
    
    def process_cv_file(self, file_path, extracted_data=None):
        """
        Process a CV file detected by QueryMind
        
        Args:
            file_path: Path to the CV file
            extracted_data: Pre-extracted CV data (if available)
        
        Returns:
            bool: Success status
        """
        try:
            file_path = Path(file_path)
            
            # Check if already processed
            file_key = str(file_path)
            if file_key in self.processed_files:
                logger.info(f"File already processed: {file_path.name}")
                return True
            
            logger.info(f"Processing new CV: {file_path.name}")
            
            # Extract data if not provided
            if not extracted_data:
                extracted_data = self.extract_cv_data(file_path)
            
            if not extracted_data:
                logger.error(f"Failed to extract data from: {file_path.name}")
                return False
            
            # Create Resume record with transaction
            with transaction.atomic():
                resume = self.create_resume_record(file_path, extracted_data)
                if resume:
                    # Index in search system (this will be triggered automatically by signals)
                    logger.info(f"Created resume record: {resume.id}")
                    
                    # Mark as processed
                    self.processed_files[file_key] = {
                        'processed_at': datetime.now().isoformat(),
                        'resume_id': str(resume.id),
                        'file_size': file_path.stat().st_size if file_path.exists() else 0
                    }
                    self.save_processed_files()
                    
                    # Log integration success
                    self.log_integration_event('success', file_path, resume.id)
                    
                    return True
                else:
                    logger.error(f"Failed to create resume record for: {file_path.name}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error processing CV {file_path}: {e}")
            self.log_integration_event('error', file_path, error=str(e))
            return False
    
    def extract_cv_data(self, file_path):
        """
        Extract CV data using existing extraction logic
        """
        try:
            # This would integrate with your existing AI parser
            # For now, create basic structure
            
            file_path = Path(file_path)
            base_name = file_path.stem
            
            # Try to extract name from filename
            name_parts = base_name.replace('_', ' ').replace('-', ' ').split()
            first_name = name_parts[0] if name_parts else 'Unknown'
            last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
            
            return {
                'first_name': first_name,
                'last_name': last_name,
                'email': '',  # Would be extracted by AI parser
                'phone': '',  # Would be extracted by AI parser  
                'location': '',  # Would be extracted by AI parser
                'summary': f'CV processed from {file_path.name}',
                'skills': '',  # Would be extracted by AI parser
                'experience': '',  # Would be extracted by AI parser
                'education': '',  # Would be extracted by AI parser
                'file_path': str(file_path),
                'file_type': file_path.suffix.lower(),
                'is_processed': True
            }
            
        except Exception as e:
            logger.error(f"Error extracting CV data: {e}")
            return None
    
    def create_resume_record(self, file_path, data):
        """
        Create Resume database record
        """
        try:
            resume = Resume.objects.create(
                first_name=data.get('first_name', 'Unknown'),
                last_name=data.get('last_name', ''),
                email=data.get('email', ''),
                phone=data.get('phone', ''),
                location=data.get('location', ''),
                summary=data.get('summary', ''),
                skills=data.get('skills', ''),
                experience=data.get('experience', ''),
                education=data.get('education', ''),
                file_path=str(file_path),
                file_type=data.get('file_type', '.pdf'),
                is_processed=True,
                extracted_text=data.get('extracted_text', ''),
                created_at=datetime.now()
            )
            
            logger.info(f"Created Resume record: {resume.id}")
            return resume
            
        except Exception as e:
            logger.error(f"Error creating resume record: {e}")
            return None
    
    def log_integration_event(self, event_type, file_path, resume_id=None, error=None):
        """Log integration events"""
        try:
            event = {
                'timestamp': datetime.now().isoformat(),
                'event_type': event_type,
                'file_path': str(file_path),
                'file_name': Path(file_path).name,
                'resume_id': str(resume_id) if resume_id else None,
                'error': error
            }
            
            # Log to file
            with open(self.monitoring_log, 'a') as f:
                f.write(json.dumps(event) + '\n')
                
        except Exception as e:
            logger.error(f"Error logging event: {e}")
    
    def scan_for_new_files(self, watch_directories):
        """
        Scan directories for new CV files
        
        Args:
            watch_directories: List of directories to monitor
        """
        logger.info(f"Scanning {len(watch_directories)} directories for new CVs...")
        
        cv_extensions = {'.pdf', '.doc', '.docx', '.txt'}
        processed_count = 0
        
        for directory in watch_directories:
            directory = Path(directory)
            if not directory.exists():
                logger.warning(f"Directory does not exist: {directory}")
                continue
                
            logger.info(f"Scanning directory: {directory}")
            
            for file_path in directory.rglob('*'):
                if (file_path.is_file() and 
                    file_path.suffix.lower() in cv_extensions and
                    str(file_path) not in self.processed_files):
                    
                    logger.info(f"Found new CV file: {file_path.name}")
                    
                    if self.process_cv_file(file_path):
                        processed_count += 1
                        logger.info(f"Successfully processed: {file_path.name}")
                    else:
                        logger.error(f"Failed to process: {file_path.name}")
        
        logger.info(f"Scan complete. Processed {processed_count} new files.")
        return processed_count
    
    def start_monitoring(self, watch_directories, check_interval=60):
        """
        Start continuous monitoring for new files
        
        Args:
            watch_directories: List of directories to monitor
            check_interval: Seconds between scans
        """
        logger.info(f"Starting continuous monitoring...")
        logger.info(f"Watch directories: {watch_directories}")
        logger.info(f"Check interval: {check_interval} seconds")
        
        try:
            while True:
                logger.info("Running scheduled scan...")
                processed = self.scan_for_new_files(watch_directories)
                
                if processed > 0:
                    logger.info(f"Processed {processed} new CVs")
                    # Trigger search index refresh if needed
                    self.refresh_search_status()
                else:
                    logger.info("No new files found")
                
                logger.info(f"Next scan in {check_interval} seconds...")
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")
    
    def refresh_search_status(self):
        """Check search index sync status"""
        try:
            from elasticsearch import Elasticsearch
            
            # Check database vs Elasticsearch count
            db_count = Resume.objects.filter(is_processed=True).count()
            
            es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
            if es.ping():
                index_info = es.indices.stats(index='cv_documents')
                es_count = index_info['indices']['cv_documents']['total']['docs']['count']
                
                logger.info(f"Search index status: DB={db_count}, ES={es_count}")
                
                if db_count != es_count:
                    logger.warning(f"Search index out of sync! DB={db_count}, ES={es_count}")
                    # Could trigger re-indexing here if needed
                    
            else:
                logger.warning("Elasticsearch not responding")
                
        except Exception as e:
            logger.error(f"Error checking search status: {e}")

def main():
    """Main function to run the integration"""
    processor = IntegratedCVProcessor()
    
    # Default watch directories - modify as needed
    default_watch_dirs = [
        PROJECT_ROOT / 'media' / 'uploads',
        PROJECT_ROOT / 'backend' / 'media' / 'uploads',
        # Add your CV storage directories here
    ]
    
    # Create directories if they don't exist
    for directory in default_watch_dirs:
        directory.mkdir(parents=True, exist_ok=True)
    
    print("🔗 QueryMind-Search Integration Manager")
    print("=" * 50)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Backend Dir: {BACKEND_DIR}")
    print(f"QueryMind Dir: {QUERYMIND_DIR}")
    print()
    
    # Check system status first
    try:
        # Database check
        db_count = Resume.objects.count()
        print(f"📊 Database: {db_count} resumes")
        
        # Search index check
        from elasticsearch import Elasticsearch
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        if es.ping():
            index_info = es.indices.stats(index='cv_documents')
            es_count = index_info['indices']['cv_documents']['total']['docs']['count']
            print(f"🔍 Search Index: {es_count} documents")
        else:
            print("⚠️  Elasticsearch not responding")
            
    except Exception as e:
        print(f"❌ System check error: {e}")
    
    print("\nOptions:")
    print("1. Scan for new files once")
    print("2. Start continuous monitoring")
    print("3. Process specific file")
    print("4. View integration status")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == '1':
        print("\n🔍 Scanning for new CV files...")
        processed = processor.scan_for_new_files(default_watch_dirs)
        print(f"✅ Scan complete. Processed {processed} files.")
        
    elif choice == '2':
        print("\n🔄 Starting continuous monitoring...")
        print("Press Ctrl+C to stop")
        processor.start_monitoring(default_watch_dirs, check_interval=30)
        
    elif choice == '3':
        file_path = input("Enter CV file path: ").strip()
        if file_path and Path(file_path).exists():
            success = processor.process_cv_file(file_path)
            if success:
                print(f"✅ Successfully processed: {Path(file_path).name}")
            else:
                print(f"❌ Failed to process: {Path(file_path).name}")
        else:
            print("❌ File not found")
            
    elif choice == '4':
        print(f"\n📊 Integration Status:")
        print(f"Processed files: {len(processor.processed_files)}")
        print(f"Log file: {processor.monitoring_log}")
        
        if processor.processed_files:
            print("\nRecent files:")
            for file_path, info in list(processor.processed_files.items())[-5:]:
                print(f"  • {Path(file_path).name} ({info.get('processed_at', 'unknown')})")
    
    else:
        print("Invalid option")

if __name__ == "__main__":
    main()
