"""
Django management command to index files for search
Usage: python manage.py index_files [directory_path] [options]
"""
import os
import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from apps.search.file_search_service import FileSearchService

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Index files for search functionality'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'directory',
            type=str,
            help='Directory path to index files from'
        )
        
        parser.add_argument(
            '--recursive',
            action='store_true',
            default=True,
            help='Index files recursively (default: True)'
        )
        
        parser.add_argument(
            '--extensions',
            type=str,
            default='.pdf,.docx,.doc,.txt,.rtf',
            help='File extensions to index (comma-separated, default: .pdf,.docx,.doc,.txt,.rtf)'
        )
        
        parser.add_argument(
            '--create-index',
            action='store_true',
            help='Create/recreate the search index before indexing files'
        )
        
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force re-indexing of already indexed files'
        )
    
    def handle(self, *args, **options):
        directory = options['directory']
        recursive = options['recursive']
        extensions = [ext.strip() for ext in options['extensions'].split(',')]
        create_index = options['create_index']
        force = options['force']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting file indexing for: {directory}')
        )
        
        # Validate directory
        if not os.path.exists(directory):
            raise CommandError(f'Directory does not exist: {directory}')
            
        if not os.path.isdir(directory):
            raise CommandError(f'Path is not a directory: {directory}')
        
        # Initialize file search service
        file_service = FileSearchService()
        
        # Create index if requested
        if create_index:
            self.stdout.write('Creating file search index...')
            if file_service.create_file_index():
                self.stdout.write(
                    self.style.SUCCESS('✓ File index created successfully')
                )
            else:
                raise CommandError('Failed to create file index')
        
        # Check system status
        status = file_service.get_system_status()
        if not status.get('elasticsearch_connected'):
            raise CommandError('Elasticsearch is not connected')
            
        if not status.get('file_search_ready'):
            self.stdout.write(
                self.style.WARNING('File search index not ready. Use --create-index to create it.')
            )
            return
        
        # Show indexing parameters
        self.stdout.write(f'Directory: {directory}')
        self.stdout.write(f'Recursive: {recursive}')
        self.stdout.write(f'Extensions: {", ".join(extensions)}')
        self.stdout.write(f'Force re-index: {force}')
        self.stdout.write('---')
        
        # Start indexing
        try:
            if force:
                # For force mode, we might need to delete existing entries
                # This is a simplified approach
                self.stdout.write('Force mode: Will re-index all files')
            
            result = file_service.index_directory(
                directory_path=directory,
                recursive=recursive,
                file_extensions=extensions
            )
            
            # Display results
            self.stdout.write('---')
            self.stdout.write(self.style.SUCCESS('Indexing completed!'))
            self.stdout.write(f'✓ Files indexed: {result["indexed"]}')
            self.stdout.write(f'✗ Files failed: {result["failed"]}')
            self.stdout.write(f'- Files skipped: {result["skipped"]}')
            self.stdout.write(f'Total processed: {result["total_processed"]}')
            
            # Show final status
            final_status = file_service.get_system_status()
            self.stdout.write('---')
            self.stdout.write('Final System Status:')
            self.stdout.write(f'Total indexed files: {final_status.get("total_files", 0)}')
            if final_status.get('index_size_mb'):
                self.stdout.write(f'Index size: {final_status["index_size_mb"]} MB')
            
        except Exception as e:
            raise CommandError(f'Indexing failed: {str(e)}')
