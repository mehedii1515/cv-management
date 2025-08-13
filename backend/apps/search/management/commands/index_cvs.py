"""
Django management command to index CVs into Elasticsearch
Handles timeout issues by processing in batches with retries
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.resumes.models import Resume
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionTimeout, RequestError
import time
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Index CV documents into Elasticsearch with timeout handling'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=5,
            help='Number of documents to process in each batch (default: 5)'
        )
        parser.add_argument(
            '--start-id',
            type=str,
            help='Resume ID to start from (for resuming interrupted indexing)'
        )
        parser.add_argument(
            '--max-retries',
            type=int,
            default=3,
            help='Maximum number of retries for failed operations (default: 3)'
        )
        parser.add_argument(
            '--delay',
            type=int,
            default=2,
            help='Delay in seconds between batches (default: 2)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be indexed without actually doing it'
        )

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        start_id = options['start_id']
        max_retries = options['max_retries']
        delay = options['delay']
        dry_run = options['dry_run']

        self.stdout.write(
            self.style.SUCCESS(f'Starting CV indexing with batch size: {batch_size}')
        )

        # Setup Elasticsearch client
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}], 
                          timeout=30, max_retries=2, retry_on_timeout=True)

        # Test connection
        try:
            es.ping()
            self.stdout.write(self.style.SUCCESS('✅ Elasticsearch connection OK'))
        except Exception as e:
            raise CommandError(f'❌ Elasticsearch connection failed: {e}')

        # Get resumes to process
        queryset = Resume.objects.all().order_by('id')
        if start_id:
            queryset = queryset.filter(id__gte=start_id)

        total_count = queryset.count()
        self.stdout.write(f'Found {total_count} resumes to process')

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No actual indexing will be performed'))

        processed = 0
        errors = 0
        skipped = 0

        # Process in batches
        for offset in range(0, total_count, batch_size):
            batch = list(queryset[offset:offset + batch_size])
            batch_num = (offset // batch_size) + 1
            total_batches = (total_count + batch_size - 1) // batch_size

            self.stdout.write(
                f'\nProcessing batch {batch_num}/{total_batches} '
                f'(resumes {offset + 1}-{min(offset + batch_size, total_count)})'
            )

            for resume in batch:
                if dry_run:
                    self.stdout.write(f'  Would index: {resume.first_name} {resume.last_name} (ID: {resume.id})')
                    processed += 1
                    continue

                success = self.index_resume(es, resume, max_retries)
                if success:
                    processed += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✅ Indexed: {resume.first_name} {resume.last_name}')
                    )
                else:
                    errors += 1
                    self.stdout.write(
                        self.style.ERROR(f'  ❌ Failed: {resume.first_name} {resume.last_name}')
                    )

            # Delay between batches
            if batch_num < total_batches and not dry_run:
                self.stdout.write(f'  Waiting {delay} seconds...')
                time.sleep(delay)

        # Summary
        self.stdout.write(f'\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Indexing completed!'))
        self.stdout.write(f'Processed: {processed}')
        self.stdout.write(f'Errors: {errors}')
        self.stdout.write(f'Skipped: {skipped}')

        if not dry_run:
            # Verify index
            try:
                doc_count = es.count(index='cv_documents')['count']
                self.stdout.write(f'Total documents in index: {doc_count}')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Could not verify index: {e}'))

    def index_resume(self, es, resume, max_retries):
        """Index a single resume with retry logic"""
        for attempt in range(max_retries):
            try:
                # Prepare document
                doc = {
                    'name': f"{resume.first_name or ''} {resume.last_name or ''}".strip(),
                    'email': resume.email or '',
                    'phone': resume.phone_number or '',
                    'skills': resume.skill_keywords or '',
                    'experience': resume.expertise_details or '',
                    'education': '',  # No direct education field in this model
                    'summary': resume.expertise_areas or '',
                    'file_content': '',  # Skip file content for now
                    'location': resume.location or '',
                    'current_employer': resume.current_employer or '',
                    'years_of_experience': resume.years_of_experience or 0,
                    'sectors': resume.sectors or '',
                    'linkedin_profile': resume.linkedin_profile or '',
                    'languages_spoken': resume.languages_spoken or '',
                    'professional_certifications': resume.professional_certifications or '',
                }

                # Index document
                result = es.index(
                    index='cv_documents',
                    id=str(resume.id),
                    document=doc,  # Using 'document' instead of 'body' for newer ES versions
                    timeout='30s'
                )
                
                return True

            except ConnectionTimeout:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2  # Exponential backoff
                    self.stdout.write(f'    Timeout, retrying in {wait_time}s...')
                    time.sleep(wait_time)
                else:
                    self.stdout.write(f'    Max retries exceeded due to timeout')
                    return False

            except RequestError as e:
                self.stdout.write(f'    Request error: {e}')
                return False

            except Exception as e:
                if attempt < max_retries - 1:
                    self.stdout.write(f'    Error: {e}, retrying...')
                    time.sleep(1)
                else:
                    self.stdout.write(f'    Failed after {max_retries} attempts: {e}')
                    return False

        return False
