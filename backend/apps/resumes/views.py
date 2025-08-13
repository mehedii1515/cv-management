import os
import logging
from django.conf import settings
from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.http import FileResponse, Http404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import django_filters
import json
from django.db import models

from .models import Resume
from .serializers import ResumeSerializer, ResumeUploadSerializer, BatchResumeUploadSerializer, BatchUploadResultSerializer
from ..ai_parser.services import ResumeParsingService

logger = logging.getLogger(__name__)


class ResumePagination(PageNumberPagination):
    """Custom pagination for resume results"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class ResumeFilter(django_filters.FilterSet):
    """
    Custom filter for Resume model to handle JSON fields properly
    """
    # Standard filters
    years_of_experience = django_filters.NumberFilter(field_name='years_of_experience')
    years_of_experience__gte = django_filters.NumberFilter(field_name='years_of_experience', lookup_expr='gte')
    years_of_experience__lte = django_filters.NumberFilter(field_name='years_of_experience', lookup_expr='lte')
    processing_status = django_filters.CharFilter(field_name='processing_status', lookup_expr='exact')
    availability = django_filters.CharFilter(field_name='availability', lookup_expr='icontains')
    
    # Custom filters with OR logic support
    location = django_filters.CharFilter(method='filter_location')
    expertise_areas = django_filters.CharFilter(method='filter_expertise_areas')
    sectors = django_filters.CharFilter(method='filter_sectors')
    skills = django_filters.CharFilter(method='filter_skills')
    experience = django_filters.CharFilter(method='filter_experience_level')
    
    class Meta:
        model = Resume
        fields = []  # We define all fields explicitly above
    
    def filter_location(self, queryset, name, value):
        """Filter by location with OR logic for multiple values"""
        if not value:
            return queryset
        
        # Get all location values from the request
        location_values = self.data.getlist('location')
        
        if not location_values:
            return queryset
        
        # Build OR query for multiple locations
        from django.db.models import Q
        location_queries = Q()
        
        for location in location_values:
            if location and location.strip():
                location_queries |= Q(location__icontains=location.strip())
        
        return queryset.filter(location_queries) if location_queries else queryset
    
    def filter_expertise_areas(self, queryset, name, value):
        """Filter by expertise areas with OR logic for multiple values"""
        if not value:
            return queryset
        
        # Get all expertise values from the request
        expertise_values = self.data.getlist('expertise_areas')
        
        if not expertise_values:
            return queryset
        
        # Build OR query for multiple expertise areas
        from django.db.models import Q
        expertise_queries = Q()
        
        for expertise in expertise_values:
            if expertise and expertise.strip():
        # Filter resumes where the expertise_areas JSON field contains the value
                expertise_queries |= Q(expertise_areas__icontains=f'"{expertise.strip()}"')
        
        return queryset.filter(expertise_queries) if expertise_queries else queryset
    
    def filter_sectors(self, queryset, name, value):
        """Filter by sectors with OR logic for multiple values"""
        if not value:
            return queryset
        
        # Get all sector values from the request
        sector_values = self.data.getlist('sectors')
        
        if not sector_values:
            return queryset
        
        # Build OR query for multiple sectors
        from django.db.models import Q
        sector_queries = Q()
        
        for sector in sector_values:
            if sector and sector.strip():
        # Filter resumes where the sectors JSON field contains the value
                sector_queries |= Q(sectors__icontains=f'"{sector.strip()}"')
        
        return queryset.filter(sector_queries) if sector_queries else queryset
    
    def filter_skills(self, queryset, name, value):
        """Filter by skill keywords with OR logic for multiple values"""
        if not value:
            return queryset
        
        # Get all skill values from the request
        skill_values = self.data.getlist('skills')
        
        if not skill_values:
            return queryset
        
        # Build OR query for multiple skills
        from django.db.models import Q
        skill_queries = Q()
        
        for skill in skill_values:
            if skill and skill.strip():
        # Filter resumes where the skill_keywords JSON field contains the value
                skill_queries |= Q(skill_keywords__icontains=f'"{skill.strip()}"')
        
        return queryset.filter(skill_queries) if skill_queries else queryset
    
    def filter_experience_level(self, queryset, name, value):
        """Filter by experience level"""
        if not value:
            return queryset
        
        # Filter by the actual experience_level property value
        # Since experience_level is a property, we need to filter based on years_of_experience
        # Matching the exact logic from Resume.experience_level property
        value = value.strip()
        if value == 'Not specified':
            # years is None or 0 (following the model's "if not years:" logic)
            return queryset.filter(models.Q(years_of_experience__isnull=True) | models.Q(years_of_experience=0))
        elif value == 'Junior':
            # 0 < years < 2
            return queryset.filter(years_of_experience__gt=0, years_of_experience__lt=2)
        elif value == 'Mid-level':
            # 2 <= years < 5
            return queryset.filter(years_of_experience__gte=2, years_of_experience__lt=5)
        elif value == 'Senior':
            # 5 <= years < 10
            return queryset.filter(years_of_experience__gte=5, years_of_experience__lt=10)
        elif value == 'Expert':
            # years >= 10
            return queryset.filter(years_of_experience__gte=10)
        
        return queryset


class ResumeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing resumes
    """
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    parser_classes = [MultiPartParser, JSONParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ResumeFilter
    pagination_class = ResumePagination
    
    # Search fields - covers all available data in the database
    search_fields = [
        # Basic personal information
        'first_name', 'last_name', 'email', 'phone_number', 'location',
        
        # Professional information
        'current_employer', 'availability', 'preferred_contract_type', 
        'preferred_work_arrangement', 'linkedin_profile', 'website_portfolio',
        'references', 'notes',
        
        # JSON fields - skills and expertise
        'expertise_areas', 'skill_keywords', 'sectors', 'languages_spoken',
        
        # JSON fields - certifications and associations
        'professional_certifications', 'professional_associations', 'publications'
    ]
    
    # Ordering fields
    ordering_fields = ['timestamp', 'first_name', 'last_name', 'years_of_experience']
    ordering = ['-timestamp']
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """
        Upload and parse a resume file
        """
        serializer = ResumeUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = serializer.validated_data['file']
        parse_immediately = serializer.validated_data['parse_immediately']
        
        try:
            # Save the uploaded file
            file_path = default_storage.save(
                f'uploads/{uploaded_file.name}',
                uploaded_file
            )
            
            # Parse the resume first to get the email and other data
            if parse_immediately:
                try:
                    # Use AI parsing service to extract data
                    parsing_service = ResumeParsingService()
                    parsed_data = parsing_service.parse_resume(file_path)
                    
                    # Extract resume text for duplicate detection
                    resume_text = parsing_service.extract_text(file_path)
                    
                    # Handle duplicate detection using new system
                    action, existing_resume, message = Resume.handle_duplicate_resume(
                        parsed_data, file_path, resume_text
                    )
                    
                    if action == 'identical':
                        # Delete the uploaded file - identical content exists
                        default_storage.delete(file_path)
                        return Response({
                            'error': 'Identical resume already exists',
                            'detail': message
                        }, status=status.HTTP_400_BAD_REQUEST)
                    
                    elif action == 'older':
                        # Delete the uploaded file - newer resume already exists
                        default_storage.delete(file_path)
                        return Response({
                            'error': 'Newer resume already exists',
                            'detail': message
                        }, status=status.HTTP_400_BAD_REQUEST)
                    
                    elif action == 'replace':
                        # Delete the older resume and its file
                        logger.info(f"Replacing older resume: {message}")
                        existing_resume.delete_file()
                        existing_resume.delete()
                     
                    # Generate content hash and file modification date
                    temp_resume = Resume(
                        first_name=parsed_data.get('first_name', ''),
                        last_name=parsed_data.get('last_name', ''),
                        phone_number=parsed_data.get('phone_number', ''),
                        years_of_experience=parsed_data.get('years_of_experience'),
                        total_experience_months=parsed_data.get('total_experience_months')
                    )
                    content_hash = temp_resume.generate_content_hash(resume_text)
                    file_creation_date = temp_resume.extract_file_modification_date(file_path)
                    
                    # Create resume record with parsed data
                    resume_data = {
                        'original_filename': uploaded_file.name,
                        'file_path': file_path,
                        'file_type': uploaded_file.name.split('.')[-1].lower(),
                        'processing_status': 'completed',
                        'is_processed': True,
                        'content_hash': content_hash,
                        'file_creation_date': file_creation_date,
                        'email': parsed_data.get('email', '')  # No fallback needed
                    }
                    
                    # Add simple fields from parsed data
                    simple_fields = [
                        'first_name', 'last_name', 'phone_number', 'location',
                        'current_employer', 'years_of_experience', 'total_experience_months', 
                        'availability', 'preferred_contract_type', 'preferred_work_arrangement',
                        'linkedin_profile', 'website_portfolio', 'references', 'notes'
                    ]
                    
                    for field in simple_fields:
                        if field in parsed_data and hasattr(Resume, field):
                            resume_data[field] = parsed_data[field]
                    
                    # Handle date_of_birth separately (convert string to date)
                    if 'date_of_birth' in parsed_data and parsed_data['date_of_birth']:
                        try:
                            from datetime import datetime
                            dob = datetime.strptime(parsed_data['date_of_birth'], '%Y-%m-%d').date()
                            resume_data['date_of_birth'] = dob
                        except (ValueError, TypeError):
                            logger.warning(f"Invalid date format for date_of_birth: {parsed_data['date_of_birth']}")
                    
                    # Create the resume instance first
                    resume = Resume.objects.create(**resume_data)
                    
                    # Now set the JSON fields using the model's setter methods
                    if 'expertise_areas' in parsed_data:
                        resume.set_expertise_areas(parsed_data['expertise_areas'])
                    if 'expertise_details' in parsed_data:
                        resume.set_expertise_details(parsed_data['expertise_details'])
                    if 'sectors' in parsed_data:
                        resume.set_sectors(parsed_data['sectors'])
                    if 'skill_keywords' in parsed_data:
                        resume.set_skill_keywords(parsed_data['skill_keywords'])
                    if 'languages_spoken' in parsed_data:
                        resume.set_languages_spoken(parsed_data['languages_spoken'])
                    if 'professional_certifications' in parsed_data:
                        resume.set_professional_certifications(parsed_data['professional_certifications'])
                    if 'professional_associations' in parsed_data:
                        resume.set_professional_associations(parsed_data['professional_associations'])
                    if 'publications' in parsed_data:
                        resume.set_publications(parsed_data['publications'])
                    
                    # Save the resume with JSON fields
                    resume.save()
                    
                    logger.info(f"Successfully uploaded and parsed resume: {resume.id}")
                    
                    return Response({
                        'id': resume.id,
                        'status': resume.processing_status,
                        'message': 'Resume uploaded and parsed successfully',
                        'data': ResumeSerializer(resume).data
                    }, status=status.HTTP_201_CREATED)
                    
                except Exception as e:
                    # If parsing fails, delete the uploaded file and return error
                    logger.error(f"Failed to parse resume: {str(e)}")
                    
                    # Clean up the uploaded file
                    if default_storage.exists(file_path):
                        default_storage.delete(file_path)
                    
                    return Response({
                        'error': 'Resume parsing failed',
                        'detail': f'Unable to process the resume file: {str(e)}. Please check the file format and content.',
                        'filename': uploaded_file.name
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Just upload without parsing
                resume = Resume.objects.create(
                    original_filename=uploaded_file.name,
                    file_path=file_path,
                    file_type=uploaded_file.name.split('.')[-1].lower(),
                    processing_status='pending',
                    email=''  # No email needed
                )
                
                return Response({
                    'id': resume.id,
                    'status': resume.processing_status,
                    'message': 'Resume uploaded successfully. Parse it later to extract details.'
                }, status=status.HTTP_201_CREATED)
            
        except IntegrityError as e:
            logger.error(f"Database integrity error: {str(e)}")
            return Response({
                'error': 'Database constraint violation',
                'detail': 'This resume might already exist in the database. Please check for duplicates.'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Failed to upload resume: {str(e)}")
            return Response({
                'error': 'Failed to upload resume',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def batch_upload(self, request):
        """
        Upload and parse multiple resume files
        """
        serializer = BatchResumeUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_files = serializer.validated_data['files']
        parse_immediately = serializer.validated_data['parse_immediately']
        
        results = []
        successful_uploads = 0
        duplicate_count = 0
        error_count = 0
        
        for uploaded_file in uploaded_files:
            result = self._process_single_file(uploaded_file, parse_immediately)
            results.append(result)
            
            if result['status'] == 'success':
                successful_uploads += 1
            elif result['status'] == 'duplicate':
                duplicate_count += 1
            else:
                error_count += 1
        
        # Create summary
        summary = {
            'total_files': len(uploaded_files),
            'successful': successful_uploads,
            'duplicates': duplicate_count,
            'errors': error_count,
            'results': results
        }
        
        # Determine overall status code
        if successful_uploads > 0:
            status_code = status.HTTP_201_CREATED if error_count == 0 else status.HTTP_207_MULTI_STATUS
        else:
            status_code = status.HTTP_400_BAD_REQUEST
        
        return Response(summary, status=status_code)
    
    def _process_single_file(self, uploaded_file, parse_immediately):
        """
        Process a single file and return the result
        """
        try:
            # Save the uploaded file
            file_path = default_storage.save(
                f'uploads/{uploaded_file.name}',
                uploaded_file
            )
            
            if parse_immediately:
                try:
                    # Use AI parsing service to extract data
                    parsing_service = ResumeParsingService()
                    parsed_data = parsing_service.parse_resume(file_path)
                    
                    # Extract resume text for duplicate detection
                    resume_text = parsing_service.extract_text(file_path)
                    
                    # Handle duplicate detection using new system
                    action, existing_resume, message = Resume.handle_duplicate_resume(
                        parsed_data, file_path, resume_text
                    )
                    
                    if action == 'identical':
                        # Delete the uploaded file - identical content exists
                        default_storage.delete(file_path)
                        return {
                            'filename': uploaded_file.name,
                            'status': 'duplicate',
                            'resume_id': None,
                            'message': f'Identical file: {message}',
                            'error_details': None,
                            'resume_data': None
                        }
                    
                    elif action == 'older':
                        # Delete the uploaded file - newer resume already exists
                        default_storage.delete(file_path)
                        return {
                            'filename': uploaded_file.name,
                            'status': 'duplicate',
                            'resume_id': None,
                            'message': f'Older resume: {message}',
                            'error_details': None,
                            'resume_data': None
                        }
                    
                    elif action == 'replace':
                        # Delete the older resume and its file
                        logger.info(f"Replacing older resume: {message}")
                        existing_resume.delete_file()
                        existing_resume.delete()
                     
                    # Generate content hash and file modification date
                    temp_resume = Resume(
                        first_name=parsed_data.get('first_name', ''),
                        last_name=parsed_data.get('last_name', ''),
                        phone_number=parsed_data.get('phone_number', ''),
                        years_of_experience=parsed_data.get('years_of_experience'),
                        total_experience_months=parsed_data.get('total_experience_months')
                    )
                    content_hash = temp_resume.generate_content_hash(resume_text)
                    file_creation_date = temp_resume.extract_file_modification_date(file_path)
                    
                    # Create resume record with parsed data
                    resume_data = {
                        'original_filename': uploaded_file.name,
                        'file_path': file_path,
                        'file_type': uploaded_file.name.split('.')[-1].lower(),
                        'processing_status': 'completed',
                        'is_processed': True,
                        'content_hash': content_hash,
                        'file_creation_date': file_creation_date,
                        'email': parsed_data.get('email', '')
                    }
                    
                    # Add simple fields from parsed data
                    simple_fields = [
                        'first_name', 'last_name', 'phone_number', 'location',
                        'current_employer', 'years_of_experience', 'total_experience_months', 
                        'availability', 'preferred_contract_type', 'preferred_work_arrangement',
                        'linkedin_profile', 'website_portfolio', 'references', 'notes'
                    ]
                    
                    for field in simple_fields:
                        if field in parsed_data and hasattr(Resume, field):
                            resume_data[field] = parsed_data[field]
                    
                    # Handle date_of_birth
                    if 'date_of_birth' in parsed_data and parsed_data['date_of_birth']:
                        try:
                            from datetime import datetime
                            dob = datetime.strptime(parsed_data['date_of_birth'], '%Y-%m-%d').date()
                            resume_data['date_of_birth'] = dob
                        except (ValueError, TypeError):
                            logger.warning(f"Invalid date format for date_of_birth: {parsed_data['date_of_birth']}")
                    
                    # Create the resume instance
                    resume = Resume.objects.create(**resume_data)
                    
                    # Set JSON fields
                    if 'expertise_areas' in parsed_data:
                        resume.set_expertise_areas(parsed_data['expertise_areas'])
                    if 'expertise_details' in parsed_data:
                        resume.set_expertise_details(parsed_data['expertise_details'])
                    if 'sectors' in parsed_data:
                        resume.set_sectors(parsed_data['sectors'])
                    if 'skill_keywords' in parsed_data:
                        resume.set_skill_keywords(parsed_data['skill_keywords'])
                    if 'languages_spoken' in parsed_data:
                        resume.set_languages_spoken(parsed_data['languages_spoken'])
                    if 'professional_certifications' in parsed_data:
                        resume.set_professional_certifications(parsed_data['professional_certifications'])
                    if 'professional_associations' in parsed_data:
                        resume.set_professional_associations(parsed_data['professional_associations'])
                    if 'publications' in parsed_data:
                        resume.set_publications(parsed_data['publications'])
                    
                    resume.save()
                    
                    logger.info(f"Successfully processed resume in batch: {resume.id}")
                    
                    return {
                        'filename': uploaded_file.name,
                        'status': 'success',
                        'resume_id': resume.id,
                        'message': "Resume uploaded and parsed successfully",
                        'error_details': None,
                        'resume_data': ResumeSerializer(resume).data
                    }
                    
                except Exception as e:
                    # Delete the file and return error
                    logger.error(f"Error during parsing: {str(e)}. Deleting file.")
                    
                    # Clean up the uploaded file
                    if default_storage.exists(file_path):
                        default_storage.delete(file_path)
                    
                    return {
                        'filename': uploaded_file.name,
                        'status': 'error',
                        'resume_id': None,
                        'message': 'Resume parsing failed',
                        'error_details': str(e),
                        'resume_data': None
                    }
            else:
                # Just upload without parsing
                resume = Resume.objects.create(
                    original_filename=uploaded_file.name,
                    file_path=file_path,
                    file_type=uploaded_file.name.split('.')[-1].lower(),
                    processing_status='pending',
                    email=f'pending_{uploaded_file.name}_{hash(uploaded_file.name)}@temp.com'
                )
                
                return {
                    'filename': uploaded_file.name,
                    'status': 'success',
                    'resume_id': resume.id,
                    'message': 'Resume uploaded successfully. Parse it later to extract details.',
                    'error_details': None,
                    'resume_data': None
                }
            
        except Exception as e:
            logger.error(f"Failed to process file in batch: {uploaded_file.name}, Error: {str(e)}")
            return {
                'filename': uploaded_file.name,
                'status': 'error',
                'resume_id': None,
                'message': 'Failed to upload resume',
                'error_details': str(e),
                'resume_data': None
            }
    
    @action(detail=True, methods=['post'])
    def reparse(self, request, pk=None):
        """
        Re-parse an existing resume
        """
        resume = self.get_object()
        
        if not resume.file_path:
            return Response({
                'error': 'No file associated with this resume'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            resume.processing_status = 'processing'
            resume.error_message = ''
            resume.save()
            
            # Use AI parsing service
            parsing_service = ResumeParsingService()
            parsed_data = parsing_service.parse_resume(resume.file_path)
            
            # Update resume with simple fields from parsed data
            simple_fields = [
                'first_name', 'last_name', 'phone_number', 'location',
                'current_employer', 'years_of_experience', 'total_experience_months', 
                'availability', 'preferred_contract_type', 'preferred_work_arrangement',
                'linkedin_profile', 'website_portfolio', 'references', 'notes'
            ]
            
            for field in simple_fields:
                if field in parsed_data and hasattr(resume, field):
                    setattr(resume, field, parsed_data[field])
            
            # Handle date_of_birth separately (convert string to date)
            if 'date_of_birth' in parsed_data and parsed_data['date_of_birth']:
                try:
                    from datetime import datetime
                    dob = datetime.strptime(parsed_data['date_of_birth'], '%Y-%m-%d').date()
                    resume.date_of_birth = dob
                except (ValueError, TypeError):
                    logger.warning(f"Invalid date format for date_of_birth: {parsed_data['date_of_birth']}")
            
            # Update JSON fields using the model's setter methods
            if 'expertise_areas' in parsed_data:
                resume.set_expertise_areas(parsed_data['expertise_areas'])
            if 'expertise_details' in parsed_data:
                resume.set_expertise_details(parsed_data['expertise_details'])
            if 'sectors' in parsed_data:
                resume.set_sectors(parsed_data['sectors'])
            if 'skill_keywords' in parsed_data:
                resume.set_skill_keywords(parsed_data['skill_keywords'])
            if 'languages_spoken' in parsed_data:
                resume.set_languages_spoken(parsed_data['languages_spoken'])
            if 'professional_certifications' in parsed_data:
                resume.set_professional_certifications(parsed_data['professional_certifications'])
            if 'professional_associations' in parsed_data:
                resume.set_professional_associations(parsed_data['professional_associations'])
            if 'publications' in parsed_data:
                resume.set_publications(parsed_data['publications'])
            
            resume.processing_status = 'completed'
            resume.is_processed = True
            resume.save()
            
            return Response({
                'message': 'Resume re-parsed successfully',
                'status': resume.processing_status,
                'data': ResumeSerializer(resume).data
            })
            
        except Exception as e:
            # If re-parsing fails, update the resume status
            logger.error(f"Failed to re-parse resume {resume.id}: {str(e)}")
            
            # Update the resume status to indicate failure
            resume.processing_status = 'failed'
            resume.error_message = str(e)[:255]  # Truncate if too long
            resume.save()
            
            return Response({
                'error': 'Failed to re-parse resume',
                'detail': f'Resume parsing failed: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get resume statistics
        """
        total_resumes = Resume.objects.count()
        processed_resumes = Resume.objects.filter(is_processed=True).count()
        pending_resumes = Resume.objects.filter(processing_status='pending').count()
        failed_resumes = Resume.objects.filter(processing_status='failed').count()
        
        # Top expertise areas
        expertise_stats = {}
        for resume in Resume.objects.filter(is_processed=True):
            for expertise in resume.get_expertise_areas():
                expertise_stats[expertise] = expertise_stats.get(expertise, 0) + 1
        
        top_expertise = sorted(expertise_stats.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Top locations
        location_stats = {}
        for resume in Resume.objects.filter(is_processed=True, location__isnull=False).exclude(location=''):
            location_stats[resume.location] = location_stats.get(resume.location, 0) + 1
        
        top_locations = sorted(location_stats.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return Response({
            'total_resumes': total_resumes,
            'processed_resumes': processed_resumes,
            'pending_resumes': pending_resumes,
            'failed_resumes': failed_resumes,
            'top_expertise_areas': top_expertise,
            'top_locations': top_locations
        })

    @action(detail=False, methods=['get'])
    def filter_options(self, request):
        """
        Get all available filter options from the entire database
        """
        try:
            # Get all processed resumes
            processed_resumes = Resume.objects.filter(processing_status='completed')
            
            # Collect unique values for each filter type
            expertise_areas = set()
            locations = set()
            sectors = set()
            skills = set()
            experience_levels = set()
            
            for resume in processed_resumes:
                # Expertise areas
                for area in resume.get_expertise_areas():
                    if area and area.strip():
                        expertise_areas.add(area.strip())
                
                # Locations
                if resume.location and resume.location.strip():
                    locations.add(resume.location.strip())
                
                # Sectors
                for sector in resume.get_sectors():
                    if sector and sector.strip():
                        sectors.add(sector.strip())
                
                # Skills
                for skill in resume.get_skill_keywords():
                    if skill and skill.strip():
                        skills.add(skill.strip())
                
                # Experience levels (use actual model property values)
                if resume.experience_level:
                    experience_levels.add(resume.experience_level)
            
            return Response({
                'expertise': sorted(list(expertise_areas)),
                'locations': sorted(list(locations)),
                'sectors': sorted(list(sectors)),
                'skills': sorted(list(skills)),
                'experienceLevels': sorted(list(experience_levels))
            })
            
        except Exception as e:
            logger.error(f"Error getting filter options: {str(e)}")
            return Response({
                'expertise': [],
                'locations': [],
                'sectors': [],
                'skills': [],
                'experienceLevels': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Download resume file
        """
        try:
            resume = self.get_object()
            
            # Check if file exists
            if not resume.file_path:
                return Response({'error': 'No file associated with this resume'}, 
                              status=status.HTTP_404_NOT_FOUND)
            
            # Construct full file path
            file_path = os.path.join(settings.MEDIA_ROOT, resume.file_path)
            
            if not os.path.exists(file_path):
                return Response({'error': 'File not found on server'}, 
                              status=status.HTTP_404_NOT_FOUND)
            
            # Return file response
            response = FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=resume.original_filename or f"{resume.full_name}_resume.pdf"
            )
            return response
            
        except Resume.DoesNotExist:
            return Response({'error': 'Resume not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

    @action(detail=True, methods=['get'])
    def extract_expertise(self, request, pk=None):
        """
        Extract specific expertise-related information directly from the resume text
        """
        try:
            resume = self.get_object()
            expertise_area = request.query_params.get('expertise_area')
            
            if not expertise_area:
                return Response({
                    'error': 'expertise_area parameter is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if file exists
            if not resume.file_path:
                return Response({
                    'error': 'No file associated with this resume'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Construct full file path
            file_path = os.path.join(settings.MEDIA_ROOT, resume.file_path)
            
            if not os.path.exists(file_path):
                return Response({
                    'error': 'Resume file not found on server'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # First check if expertise details already exist in the resume
            expertise_details = resume.get_expertise_details().get(expertise_area, {})
            
            # If existing details are available and include work_experience, use them
            if expertise_details and ('work_experience' in expertise_details or 'projects' in expertise_details):
                logger.info(f"Using existing expertise details for {expertise_area}")
                return Response({
                    'expertise_area': expertise_area,
                    'candidate_name': resume.full_name,
                    'details': expertise_details
                })
            
            # If no details exist, check if we need to reparse the entire resume
            # since we now get all expertise details in the main parsing
            from apps.ai_parser.services import ResumeParsingService
            parsing_service = ResumeParsingService()
            
            # Parse the entire resume to get all expertise details
            parsed_data = parsing_service.parse_resume(file_path)
            
            # Check if expertise details were extracted in the parsing
            if 'expertise_details' in parsed_data and expertise_area in parsed_data['expertise_details']:
                expertise_details = parsed_data['expertise_details'][expertise_area]
                
                # Save all expertise details to the resume model
                resume.set_expertise_details(parsed_data['expertise_details'])
                resume.save()
                
                logger.info(f"Extracted and saved expertise details for {expertise_area} from main parsing")
                
                return Response({
                    'expertise_area': expertise_area,
                    'candidate_name': resume.full_name,
                    'details': expertise_details
                })
            else:
                # If expertise area not found in parsed data
                return Response({
                    'expertise_area': expertise_area,
                    'candidate_name': resume.full_name,
                    'details': {
                        'message': f"No specific information found for {expertise_area} in this resume."
                    }
                })
            
        except Resume.DoesNotExist:
            return Response({
                'error': 'Resume not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            return Response({
                'error': f'Failed to parse AI response as JSON: {str(e)}',
                'detail': 'The AI service returned an invalid response. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Error extracting expertise: {str(e)}")
            return Response({
                'error': f'Failed to extract expertise details: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

    @action(detail=True, methods=['post'])
    def enrich_expertise_details(self, request, pk=None):
        """
        Enrich all expertise details for a resume by processing each expertise area
        """
        try:
            resume = self.get_object()
            
            # Check if file exists
            if not resume.file_path:
                return Response({
                    'error': 'No file associated with this resume'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Construct full file path
            file_path = os.path.join(settings.MEDIA_ROOT, resume.file_path)
            
            if not os.path.exists(file_path):
                return Response({
                    'error': 'Resume file not found on server'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Get the list of expertise areas
            expertise_areas = resume.get_expertise_areas()
            
            if not expertise_areas:
                return Response({
                    'error': 'No expertise areas found for this resume'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Use AI parsing service to parse the entire resume with all expertise details
            from apps.ai_parser.services import ResumeParsingService
            parsing_service = ResumeParsingService()
            
            # Parse the entire resume to get all expertise details at once
            parsed_data = parsing_service.parse_resume(file_path)
            
            if 'expertise_details' in parsed_data and parsed_data['expertise_details']:
                # Save the expertise details to the resume
                resume.set_expertise_details(parsed_data['expertise_details'])
                resume.save()
                
                # Generate results for each expertise area
                results = []
                for area in expertise_areas:
                    if area in parsed_data['expertise_details']:
                        results.append({
                            'area': area,
                            'status': 'success',
                            'details_found': True
                        })
                    else:
                        results.append({
                            'area': area,
                            'status': 'not_found',
                            'details_found': False
                        })
                
                return Response({
                    'resume_id': resume.id,
                    'candidate_name': resume.full_name,
                    'processed_areas': len(results),
                    'results': results
                })
            else:
                return Response({
                    'error': 'No expertise details found in the parsed resume data'
                }, status=status.HTTP_404_NOT_FOUND)
            
        except Resume.DoesNotExist:
            return Response({
                'error': 'Resume not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error enriching expertise details: {str(e)}")
            return Response({
                'error': f'Failed to enrich expertise details: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)