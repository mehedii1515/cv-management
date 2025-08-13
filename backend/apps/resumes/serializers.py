from rest_framework import serializers
from .models import Resume
import json


class ResumeSerializer(serializers.ModelSerializer):
    """
    Serializer for Resume model
    """
    full_name = serializers.ReadOnlyField()
    experience_level = serializers.ReadOnlyField()
    experience_display = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    total_experience_years = serializers.ReadOnlyField()
    
    # Custom fields to handle JSON serialization
    expertise_areas = serializers.SerializerMethodField()
    expertise_details = serializers.SerializerMethodField()
    sectors = serializers.SerializerMethodField()
    skill_keywords = serializers.SerializerMethodField()
    languages_spoken = serializers.SerializerMethodField()
    professional_certifications = serializers.SerializerMethodField()
    professional_associations = serializers.SerializerMethodField()
    publications = serializers.SerializerMethodField()
    
    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ('id', 'timestamp', 'cv_hash', 'full_name', 'experience_level', 'experience_display', 'age', 'total_experience_years')
    
    def get_expertise_areas(self, obj):
        """Convert expertise_areas JSON string to array"""
        return obj.get_expertise_areas()
    
    def get_expertise_details(self, obj):
        """Convert expertise_details JSON string to dict"""
        return obj.get_expertise_details()
    
    def get_sectors(self, obj):
        """Convert sectors JSON string to array"""
        return obj.get_sectors()
    
    def get_skill_keywords(self, obj):
        """Convert skill_keywords JSON string to array"""
        return obj.get_skill_keywords()
    
    def get_languages_spoken(self, obj):
        """Convert languages_spoken JSON string to array"""
        return obj.get_languages_spoken()
    
    def get_professional_certifications(self, obj):
        """Convert professional_certifications JSON string to array"""
        return obj.get_professional_certifications()
    
    def get_professional_associations(self, obj):
        """Convert professional_associations JSON string to array"""
        return obj.get_professional_associations()
    
    def get_publications(self, obj):
        """Convert publications JSON string to array"""
        return obj.get_publications()


class ResumeUploadSerializer(serializers.Serializer):
    """
    Serializer for resume file upload
    """
    file = serializers.FileField()
    parse_immediately = serializers.BooleanField(default=True)
    
    def validate_file(self, value):
        """
        Validate uploaded file
        """
        # Check file size (10MB limit)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 10MB")
        
        # Check file extension
        allowed_extensions = ['pdf', 'docx', 'doc', 'txt', 'rtf']
        file_extension = value.name.split('.')[-1].lower()
        
        if file_extension not in allowed_extensions:
            raise serializers.ValidationError(
                f"File type '{file_extension}' not supported. "
                f"Allowed types: {', '.join(allowed_extensions)}"
            )
        
        return value


class BatchResumeUploadSerializer(serializers.Serializer):
    """
    Serializer for batch resume file upload
    """
    files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False,
        max_length=50  # Maximum 50 files per batch
    )
    parse_immediately = serializers.BooleanField(default=True)
    
    def validate_files(self, value):
        """
        Validate uploaded files
        """
        if len(value) > 50:
            raise serializers.ValidationError("Maximum 50 files allowed per batch")
        
        if len(value) == 0:
            raise serializers.ValidationError("At least one file is required")
        
        allowed_extensions = ['pdf', 'docx', 'doc', 'txt', 'rtf']
        total_size = 0
        
        for file in value:
            # Check individual file size (10MB limit)
            if file.size > 10 * 1024 * 1024:
                raise serializers.ValidationError(f"File '{file.name}' exceeds 10MB limit")
            
            # Check file extension
            file_extension = file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise serializers.ValidationError(
                    f"File '{file.name}' has unsupported type '{file_extension}'. "
                    f"Allowed types: {', '.join(allowed_extensions)}"
                )
            
            total_size += file.size
        
        # Check total batch size (200MB limit)
        if total_size > 200 * 1024 * 1024:
            raise serializers.ValidationError("Total batch size cannot exceed 200MB")
        
        return value


class BatchUploadResultSerializer(serializers.Serializer):
    """
    Serializer for batch upload results
    """
    filename = serializers.CharField()
    status = serializers.ChoiceField(choices=['success', 'duplicate', 'error'])
    resume_id = serializers.UUIDField(required=False, allow_null=True)
    message = serializers.CharField()
    error_details = serializers.CharField(required=False, allow_null=True)
    resume_data = ResumeSerializer(required=False, allow_null=True) 