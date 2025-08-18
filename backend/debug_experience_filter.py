#!/usr/bin/env python
"""
Quick test script to debug the experience filter issue
"""
import os
import sys
import django

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_parser.settings')
django.setup()

from apps.resumes.models import Resume
from apps.resumes.views import ResumeFilter

def test_experience_filter():
    print("🧪 Testing Experience Filter Debug")
    print("=" * 50)
    
    # Test basic model query
    total_resumes = Resume.objects.count()
    print(f"📊 Total resumes in database: {total_resumes}")
    
    # Test experience level distribution
    experience_counts = {}
    for resume in Resume.objects.all()[:20]:  # Test first 20
        exp_level = resume.experience_level
        years = resume.years_of_experience
        if exp_level not in experience_counts:
            experience_counts[exp_level] = 0
        experience_counts[exp_level] += 1
        print(f"  📄 {resume.first_name} {resume.last_name}: {years} years → '{exp_level}'")
    
    print(f"\n📈 Experience Level Distribution:")
    for level, count in experience_counts.items():
        print(f"  {level}: {count} resumes")
    
    # Test the filter manually
    print(f"\n🔍 Testing Manual Filter:")
    
    # Test Junior filter
    junior_resumes = Resume.objects.filter(years_of_experience__gt=0, years_of_experience__lt=2)
    print(f"  Junior (0-2 years): {junior_resumes.count()} resumes")
    
    # Test Mid-level filter  
    mid_resumes = Resume.objects.filter(years_of_experience__gte=2, years_of_experience__lt=5)
    print(f"  Mid-level (2-5 years): {mid_resumes.count()} resumes")
    
    # Test Senior filter
    senior_resumes = Resume.objects.filter(years_of_experience__gte=5, years_of_experience__lt=10)
    print(f"  Senior (5-10 years): {senior_resumes.count()} resumes")
    
    # Test Expert filter
    expert_resumes = Resume.objects.filter(years_of_experience__gte=10)
    print(f"  Expert (10+ years): {expert_resumes.count()} resumes")
    
    # Test Not specified filter
    not_specified_resumes = Resume.objects.filter(
        models.Q(years_of_experience__isnull=True) | 
        models.Q(years_of_experience=0)
    )
    print(f"  Not specified (0 or NULL): {not_specified_resumes.count()} resumes")

if __name__ == "__main__":
    from django.db import models
    test_experience_filter()
