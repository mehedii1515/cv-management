"""
Django management command to trigger background CV indexing
"""
from django.core.management.base import BaseCommand, CommandError
from apps.search.tasks import bulk_index_cvs, index_single_cv, refresh_search_index
from apps.resumes.models import Resume
import time


class Command(BaseCommand):
    help = 'Index CVs using Celery background tasks'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=10,
            help='Number of documents to process in each batch (default: 10)'
        )
        parser.add_argument(
            '--resume-id',
            type=str,
            help='Index a specific resume by ID'
        )
        parser.add_argument(
            '--async',
            action='store_true',
            help='Run tasks asynchronously (default: wait for completion)'
        )
        parser.add_argument(
            '--refresh',
            action='store_true',
            help='Refresh the search index after completion'
        )

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        resume_id = options['resume_id']
        run_async = options['async']
        refresh = options['refresh']

        self.stdout.write(
            self.style.SUCCESS(f'Starting background CV indexing...')
        )

        if resume_id:
            # Index single CV
            try:
                resume = Resume.objects.get(id=resume_id)
                self.stdout.write(f'Indexing CV: {resume.first_name} {resume.last_name} (ID: {resume_id})')
                
                task = index_single_cv.apply_async(args=[resume_id])
                
                if not run_async:
                    result = task.get()
                    if result['status'] == 'success':
                        self.stdout.write(self.style.SUCCESS(f'✅ Successfully indexed CV'))
                    else:
                        self.stdout.write(self.style.ERROR(f'❌ Failed to index CV: {result.get("error", "Unknown error")}'))
                else:
                    self.stdout.write(f'Task queued with ID: {task.id}')
                    
            except Resume.DoesNotExist:
                raise CommandError(f'Resume with ID {resume_id} does not exist')
                
        else:
            # Bulk index all CVs
            total_count = Resume.objects.filter(is_processed=True).count()
            self.stdout.write(f'Found {total_count} processed CVs to index')
            
            task = bulk_index_cvs.apply_async(kwargs={'batch_size': batch_size})
            
            if not run_async:
                self.stdout.write('Waiting for bulk indexing to complete...')
                self.stdout.write('(This may take several minutes)')
                
                # Show progress
                start_time = time.time()
                while not task.ready():
                    elapsed = int(time.time() - start_time)
                    self.stdout.write(f'\rElapsed time: {elapsed}s', ending='')
                    time.sleep(2)
                
                result = task.get()
                
                self.stdout.write('\n' + '='*50)
                self.stdout.write(self.style.SUCCESS(f'Bulk indexing completed!'))
                self.stdout.write(f'Total: {result["total"]}')
                self.stdout.write(f'Processed: {result["processed"]}')
                self.stdout.write(f'Errors: {result["errors"]}')
                
            else:
                self.stdout.write(f'Bulk indexing task queued with ID: {task.id}')
        
        # Refresh index if requested
        if refresh:
            self.stdout.write('Refreshing search index...')
            refresh_task = refresh_search_index.apply_async()
            
            if not run_async:
                refresh_result = refresh_task.get()
                if refresh_result['status'] == 'success':
                    self.stdout.write(self.style.SUCCESS('✅ Index refreshed'))
                else:
                    self.stdout.write(self.style.ERROR(f'❌ Failed to refresh index: {refresh_result.get("error")}'))
            else:
                self.stdout.write(f'Index refresh task queued with ID: {refresh_task.id}')
        
        self.stdout.write(self.style.SUCCESS('Background indexing operations completed!'))
