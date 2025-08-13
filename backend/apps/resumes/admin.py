from django.contrib import admin
from django.utils.html import format_html
import json
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Resume model
    """
    list_display = [
        'full_name', 
        'email', 
        'current_employer', 
        'years_of_experience',
        'location',
        'processing_status',
        'timestamp'
    ]
    
    list_filter = [
        'processing_status',
        'is_processed',
        'location',
        'years_of_experience',
        'timestamp'
    ]
    
    search_fields = [
        'first_name',
        'last_name', 
        'email',
        'current_employer',
        'location'
    ]
    
    readonly_fields = [
        'id',
        'cv_hash',
        'timestamp',
        'full_name',
        'experience_level',
        'expertise_details_pretty'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'id',
                'timestamp',
                'cv_hash',
                ('first_name', 'last_name'),
                'full_name',
                'email',
                'phone_number',
                'location'
            )
        }),
        ('Professional Information', {
            'fields': (
                'current_employer',
                'years_of_experience',
                'experience_level',
                'availability',
                'preferred_contract_type',
                'preferred_work_arrangement'
            )
        }),
        ('Skills & Expertise', {
            'fields': (
                'expertise_areas',
                'sectors',
                'skill_keywords',
                'expertise_details_pretty'
            ),
            'classes': ('collapse',)
        }),
        ('Contact Information', {
            'fields': (
                'linkedin_profile',
                'website_portfolio'
            ),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': (
                'languages_spoken',
                'professional_certifications',
                'professional_associations',
                'publications',
                'references',
                'notes'
            ),
            'classes': ('collapse',)
        }),
        ('File Information', {
            'fields': (
                'original_filename',
                'file_path',
                'file_type'
            ),
            'classes': ('collapse',)
        }),
        ('Processing Status', {
            'fields': (
                'is_processed',
                'processing_status',
                'error_message'
            )
        })
    )
    
    list_per_page = 25
    date_hierarchy = 'timestamp'
    
    def get_queryset(self, request):
        """Optimize queryset for admin list view"""
        return super().get_queryset(request).select_related()
    
    def has_delete_permission(self, request, obj=None):
        """Allow delete permission"""
        return True
    
    def has_change_permission(self, request, obj=None):
        """Allow change permission"""
        return True
    
    def has_add_permission(self, request):
        """Allow add permission"""
        return True
    
    def expertise_details_pretty(self, obj):
        """Return pretty formatted JSON for expertise_details"""
        try:
            details = obj.get_expertise_details()
            pretty_json = json.dumps(details, indent=2, ensure_ascii=False)
            return format_html('<pre style="white-space: pre-wrap; max-height: 500px; overflow: auto;">{}</pre>', pretty_json)
        except Exception:
            return obj.expertise_details or "{}"
    
    expertise_details_pretty.short_description = "Expertise Details"
    expertise_details_pretty.allow_tags = True 