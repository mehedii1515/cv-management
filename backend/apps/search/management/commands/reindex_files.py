"""
Management command to reindex files that exist but are not in the file index
"""
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from apps.resumes.models import Resume
from apps.search.tasks import index_resume_file
from apps.search.file_search_service import FileSearchService
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Reindex files that exist but are missing from file search index'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Just show what would be indexed without actually doing it'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limit number of files to process'
        )
    
    def handle(self, *args, **options):
        self.stdout.write('🔍 Analyzing file indexing status...')
        
        # Get current index status
        file_service = FileSearchService()
        try:
            response = file_service.es_client.count(index=file_service.index_name)
            current_indexed = response.get('count', 0)
        except:
            current_indexed = 0
            
        self.stdout.write(f'📊 Current file index count: {current_indexed}')
        
        # Find all processed resumes with existing files
        indexable_files = []
        missing_files = []
        
        for resume in Resume.objects.filter(is_processed=True):
            if not resume.file_path:
                continue
                
            if default_storage.exists(resume.file_path):
                indexable_files.append(resume)
            else:
                missing_files.append(resume)
        
        self.stdout.write(f'✅ Files that exist and should be indexed: {len(indexable_files)}')
        self.stdout.write(f'❌ Files missing from disk: {len(missing_files)}')
        self.stdout.write(f'🔢 Potential missing from index: {len(indexable_files) - current_indexed}')
        
        if options['dry_run']:
            self.stdout.write('🔍 DRY RUN - Showing first 10 files that would be indexed:')
            for i, resume in enumerate(indexable_files[:10]):
                self.stdout.write(f'  {i+1}. {resume.original_filename}')
                self.stdout.write(f'     Path: {resume.file_path}')
            return
        
        # Actually index the files
        limit = options.get('limit', len(indexable_files))
        indexed_count = 0
        error_count = 0
        
        self.stdout.write(f'🚀 Starting to index {min(limit, len(indexable_files))} files...')
        
        for i, resume in enumerate(indexable_files[:limit]):
            if i % 10 == 0:
                self.stdout.write(f'Progress: {i}/{min(limit, len(indexable_files))}')
            
            try:
                result = index_resume_file(resume.id)
                if result and result.get('status') == 'success':
                    indexed_count += 1
                else:
                    error_count += 1
                    self.stdout.write(f'⚠️  Failed to index: {resume.original_filename}')
            except Exception as e:
                error_count += 1
                self.stdout.write(f'❌ Error indexing {resume.original_filename}: {e}')
        
        # Check final count
        try:
            response = file_service.es_client.count(index=file_service.index_name)
            final_indexed = response.get('count', 0)
        except:
            final_indexed = current_indexed
            
        self.stdout.write('✅ Indexing completed!')
        self.stdout.write(f'📊 Results:')
        self.stdout.write(f'   - Successfully indexed: {indexed_count}')
        self.stdout.write(f'   - Errors: {error_count}')
        self.stdout.write(f'   - Initial index count: {current_indexed}')
        self.stdout.write(f'   - Final index count: {final_indexed}')
        self.stdout.write(f'   - Net increase: +{final_indexed - current_indexed}')
