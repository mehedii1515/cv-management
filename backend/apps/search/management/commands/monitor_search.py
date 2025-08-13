"""
Django management command to monitor search system status
"""
from django.core.management.base import BaseCommand
from apps.search.services import SearchService
from apps.resumes.models import Resume
from apps.search.tasks import monitor_querymind_integration
from elasticsearch import Elasticsearch


class Command(BaseCommand):
    help = 'Monitor search system status and health'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check-querymind',
            action='store_true',
            help='Check for new CVs from QueryMind integration'
        )
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Show detailed information'
        )

    def handle(self, *args, **options):
        check_querymind = options['check_querymind']
        detailed = options['detailed']

        self.stdout.write(
            self.style.SUCCESS('=== SEARCH SYSTEM STATUS ===')
        )

        # 1. Elasticsearch connection
        try:
            es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
            es_connected = es.ping()
            
            if es_connected:
                self.stdout.write(self.style.SUCCESS('✅ Elasticsearch: Connected'))
                
                # Index stats
                if es.indices.exists(index='cv_documents'):
                    stats = es.indices.stats(index='cv_documents')
                    doc_count = stats['indices']['cv_documents']['total']['docs']['count']
                    index_size = stats['indices']['cv_documents']['total']['store']['size_in_bytes']
                    
                    self.stdout.write(f'   📊 Documents: {doc_count}')
                    self.stdout.write(f'   💾 Index size: {index_size:,} bytes')
                else:
                    self.stdout.write(self.style.WARNING('⚠️  Index "cv_documents" does not exist'))
            else:
                self.stdout.write(self.style.ERROR('❌ Elasticsearch: Not connected'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Elasticsearch: Connection failed - {e}'))

        # 2. Database stats
        total_resumes = Resume.objects.count()
        processed_resumes = Resume.objects.filter(is_processed=True).count()
        unprocessed_resumes = total_resumes - processed_resumes
        
        self.stdout.write(f'\n📋 Database Status:')
        self.stdout.write(f'   Total CVs: {total_resumes}')
        self.stdout.write(f'   Processed: {processed_resumes}')
        self.stdout.write(f'   Unprocessed: {unprocessed_resumes}')
        
        if unprocessed_resumes > 0:
            self.stdout.write(self.style.WARNING(f'   ⚠️  {unprocessed_resumes} CVs need processing'))

        # 3. Search service test
        try:
            service = SearchService()
            test_result = service.test_connection()
            
            if test_result:
                self.stdout.write(self.style.SUCCESS('✅ Search Service: Ready'))
                
                # Quick search test
                search_test = service.search_documents('test')
                self.stdout.write(f'   🔍 Search test completed in {search_test.get("took", 0)}ms')
            else:
                self.stdout.write(self.style.ERROR('❌ Search Service: Not ready'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Search Service: Failed - {e}'))

        # 4. Check Celery (if available)
        try:
            from celery import current_app
            
            # Check if Celery is configured
            if current_app.conf.broker_url:
                self.stdout.write(f'\n🔄 Celery Configuration:')
                self.stdout.write(f'   Broker: {current_app.conf.broker_url}')
                
                # Try to get active tasks (this requires Celery to be running)
                try:
                    inspect = current_app.control.inspect()
                    active_tasks = inspect.active()
                    
                    if active_tasks:
                        total_active = sum(len(tasks) for tasks in active_tasks.values())
                        self.stdout.write(self.style.SUCCESS(f'✅ Celery: {total_active} active tasks'))
                    else:
                        self.stdout.write(self.style.WARNING('⚠️  Celery: No workers responding'))
                        
                except Exception:
                    self.stdout.write(self.style.WARNING('⚠️  Celery: Workers not accessible (may not be running)'))
            else:
                self.stdout.write(self.style.WARNING('⚠️  Celery: Not configured'))
                
        except ImportError:
            self.stdout.write(self.style.WARNING('⚠️  Celery: Not installed'))

        # 5. QueryMind integration check
        if check_querymind:
            self.stdout.write(f'\n🔍 Checking QueryMind Integration:')
            try:
                task = monitor_querymind_integration.apply_async()
                result = task.get(timeout=30)
                
                if result['status'] == 'success':
                    self.stdout.write(self.style.SUCCESS('✅ QueryMind monitoring successful'))
                    self.stdout.write(f'   New CVs found: {result["new_cvs_found"]}')
                    self.stdout.write(f'   Queued for indexing: {result["queued_for_indexing"]}')
                else:
                    self.stdout.write(self.style.ERROR(f'❌ QueryMind monitoring failed: {result.get("error")}'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ QueryMind monitoring failed: {e}'))

        # 6. Detailed information
        if detailed:
            self.stdout.write(f'\n📊 Detailed Statistics:')
            
            # Recent CVs
            from django.utils import timezone
            from datetime import timedelta
            
            recent_cvs = Resume.objects.filter(
                timestamp__gte=timezone.now() - timedelta(hours=24)
            ).count()
            
            self.stdout.write(f'   CVs added in last 24h: {recent_cvs}')
            
            # Top skills
            try:
                from django.db.models import Count
                top_skills = Resume.objects.values('skill_keywords').annotate(
                    count=Count('skill_keywords')
                ).order_by('-count')[:5]
                
                self.stdout.write(f'   Most common skills:')
                for skill in top_skills:
                    if skill['skill_keywords']:
                        self.stdout.write(f'     - {skill["skill_keywords"][:50]}... ({skill["count"]} CVs)')
                        
            except Exception as e:
                self.stdout.write(f'   Could not retrieve skill statistics: {e}')

        self.stdout.write(f'\n' + '='*40)
        self.stdout.write(self.style.SUCCESS('Status check completed!'))
