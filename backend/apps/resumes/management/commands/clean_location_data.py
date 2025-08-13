from django.core.management.base import BaseCommand
from django.db import transaction
from apps.resumes.models import Resume
from apps.ai_parser.services import ResumeParsingService


class Command(BaseCommand):
    help = 'Clean location data to contain only country names (remove cities/states)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--preview',
            action='store_true',
            help='Preview changes without modifying the database',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Same as --preview (preview changes without modifying)',
        )

    def handle(self, *args, **options):
        preview_mode = options['preview'] or options['dry_run']
        
        if preview_mode:
            self.preview_changes()
        else:
            self.clean_location_data()

    def preview_changes(self):
        """
        Preview what changes would be made without actually updating the database
        """
        self.stdout.write(self.style.SUCCESS("Previewing location data changes..."))
        
        # Initialize the parsing service
        parsing_service = ResumeParsingService()
        
        # Get all resumes that have location data
        resumes_with_location = Resume.objects.exclude(location__isnull=True).exclude(location__exact='')
        
        total_resumes = resumes_with_location.count()
        self.stdout.write(f"Found {total_resumes} resumes with location data")
        
        changes_needed = 0
        
        for i, resume in enumerate(resumes_with_location, 1):
            original_location = resume.location
            country_only = parsing_service.extract_country_only(original_location)
            
            if country_only != original_location:
                self.stdout.write(
                    self.style.WARNING(
                        f"[{i}/{total_resumes}] WOULD UPDATE: '{original_location}' → '{country_only}'"
                    )
                )
                changes_needed += 1
            else:
                self.stdout.write(f"[{i}/{total_resumes}] No change: '{original_location}'")
        
        self.stdout.write("\n" + self.style.SUCCESS("Preview completed!"))
        self.stdout.write(f"Total resumes: {total_resumes}")
        self.stdout.write(self.style.WARNING(f"Resumes that would be updated: {changes_needed}"))
        self.stdout.write(f"Resumes that would remain unchanged: {total_resumes - changes_needed}")
        
        if changes_needed > 0:
            self.stdout.write(
                "\n" + self.style.NOTICE(
                    "To apply these changes, run: python manage.py clean_location_data"
                )
            )

    def clean_location_data(self):
        """
        Clean location data for all resumes to contain only country names
        """
        self.stdout.write(self.style.SUCCESS("Starting location data cleanup..."))
        
        # Initialize the parsing service to use its country extraction method
        parsing_service = ResumeParsingService()
        
        # Get all resumes that have location data
        resumes_with_location = Resume.objects.exclude(location__isnull=True).exclude(location__exact='')
        
        total_resumes = resumes_with_location.count()
        self.stdout.write(f"Found {total_resumes} resumes with location data")
        
        if total_resumes == 0:
            self.stdout.write(self.style.SUCCESS("No resumes with location data found."))
            return
        
        updated_count = 0
        
        # Use database transaction for better performance and rollback capability
        with transaction.atomic():
            for i, resume in enumerate(resumes_with_location, 1):
                original_location = resume.location
                
                # Extract country only using the parsing service method
                country_only = parsing_service.extract_country_only(original_location)
                
                # Only update if the location changed
                if country_only != original_location:
                    self.stdout.write(
                        self.style.WARNING(
                            f"[{i}/{total_resumes}] Updating: '{original_location}' → '{country_only}'"
                        )
                    )
                    resume.location = country_only
                    resume.save()
                    updated_count += 1
                else:
                    self.stdout.write(f"[{i}/{total_resumes}] No change needed: '{original_location}'")
        
        self.stdout.write("\n" + self.style.SUCCESS("Location cleanup completed!"))
        self.stdout.write(f"Total resumes processed: {total_resumes}")
        self.stdout.write(self.style.SUCCESS(f"Resumes updated: {updated_count}"))
        self.stdout.write(f"Resumes unchanged: {total_resumes - updated_count}")
        
        if updated_count > 0:
            self.stdout.write(
                "\n" + self.style.NOTICE(
                    "Location data has been successfully cleaned. "
                    "All locations now contain only country names."
                )
            ) 