from django.db import models
from django.utils import timezone
import hashlib
import uuid
import json
import os
import re
from datetime import date
from django.core.files.storage import default_storage


class Resume(models.Model):
    """
    Resume model storing parsed candidate information
    """
    # Metadata
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(default=timezone.now)
    cv_hash = models.CharField(max_length=64, unique=True, blank=True)
    
    # Duplicate Detection Fields
    content_hash = models.CharField(max_length=64, blank=True, db_index=True, help_text="Hash of resume content to detect identical files")
    person_soft_id = models.CharField(max_length=64, blank=True, db_index=True, help_text="Soft identifier for person (name+details based)")
    file_creation_date = models.DateTimeField(null=True, blank=True, help_text="File modification date from metadata (when file was last changed)")
    
    # Personal Information
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)  # Removed unique constraint
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)  # Country
    date_of_birth = models.DateField(null=True, blank=True)  # New field for age calculation
    
    # Professional Information
    current_employer = models.CharField(max_length=200, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    total_experience_months = models.IntegerField(null=True, blank=True)  # More precise experience tracking
    availability = models.CharField(max_length=100, blank=True)
    preferred_contract_type = models.CharField(max_length=100, blank=True)
    preferred_work_arrangement = models.CharField(max_length=100, blank=True)
    
    # Skills and Expertise (stored as JSON text fields)
    expertise_areas = models.TextField(blank=True, help_text="JSON array of expertise areas")
    expertise_details = models.TextField(blank=True, help_text="JSON object mapping expertise areas to detailed information from resume")
    sectors = models.TextField(blank=True, help_text="JSON array of industry sectors")
    skill_keywords = models.TextField(blank=True, help_text="JSON array of skill keywords")
    
    # Contact Information
    linkedin_profile = models.URLField(blank=True)
    website_portfolio = models.URLField(blank=True)
    
    # Additional Information
    languages_spoken = models.TextField(blank=True, help_text="JSON array of languages")
    references = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Education and Certifications
    professional_certifications = models.TextField(blank=True, help_text="JSON array of certifications")
    professional_associations = models.TextField(blank=True, help_text="JSON array of associations")
    publications = models.TextField(blank=True, help_text="JSON array of publications")
    
    # File Information
    original_filename = models.CharField(max_length=255, blank=True)
    file_path = models.CharField(max_length=500, blank=True)
    file_type = models.CharField(max_length=10, blank=True)
    
    # Processing Status
    is_processed = models.BooleanField(default=False)
    processing_status = models.CharField(max_length=50, default='pending')  # pending, processing, completed, failed
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['content_hash']),
            models.Index(fields=['person_soft_id']),
            models.Index(fields=['email']),
            models.Index(fields=['cv_hash']),
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['years_of_experience']),
            models.Index(fields=['location']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['processing_status']),
            models.Index(fields=['date_of_birth']),
            models.Index(fields=['file_creation_date']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    def save(self, *args, **kwargs):
        """
        Override save to generate hashes and person soft ID
        """
        # Generate person soft ID for duplicate person detection
        if not self.person_soft_id:
            self.person_soft_id = self.generate_person_soft_id()
            
        # Generate CV hash based on person soft ID and timestamp (not email)
        if not self.cv_hash:
            # Use person soft ID + timestamp for uniqueness
            hash_input = f"{self.person_soft_id}{self.timestamp.isoformat()}{self.first_name}{self.last_name}".lower()
            self.cv_hash = hashlib.sha256(hash_input.encode()).hexdigest()
            
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        """Return full name"""
        first = self.first_name or ""
        last = self.last_name or ""
        return f"{first} {last}".strip()
    
    @property
    def age(self):
        """Calculate age from date of birth"""
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    @property
    def total_experience_years(self):
        """Return total experience in years (more precise if months available)"""
        if self.total_experience_months:
            return round(self.total_experience_months / 12, 1)
        return self.years_of_experience
    
    @property
    def experience_display(self):
        """Return experience in 'X years Y months' format"""
        if self.total_experience_months:
            total_months = self.total_experience_months
            years = total_months // 12
            months = total_months % 12
            
            if years == 0 and months == 0:
                return "Less than 1 month"
            elif years == 0:
                return f"{months} month{'s' if months != 1 else ''}"
            elif months == 0:
                return f"{years} year{'s' if years != 1 else ''}"
            else:
                return f"{years} year{'s' if years != 1 else ''} {months} month{'s' if months != 1 else ''}"
        elif self.years_of_experience:
            years = self.years_of_experience
            return f"{years} year{'s' if years != 1 else ''}"
        else:
            return "Not specified"
    
    @property
    def experience_level(self):
        """Return experience level based on years"""
        years = self.total_experience_years or self.years_of_experience
        if not years:
            return "Not specified"
        elif years < 2:
            return "Junior"
        elif years < 5:
            return "Mid-level"
        elif years < 10:
            return "Senior"
        else:
            return "Expert"
    
    # JSON field helpers
    def get_expertise_areas(self):
        """Get expertise areas as Python list"""
        if not self.expertise_areas:
            return []
        try:
            return json.loads(self.expertise_areas)
        except json.JSONDecodeError:
            return []
    
    def set_expertise_areas(self, areas_list):
        """Set expertise areas from Python list"""
        self.expertise_areas = json.dumps(areas_list) if areas_list else ""
    
    def get_sectors(self):
        """Get sectors as Python list"""
        if not self.sectors:
            return []
        try:
            return json.loads(self.sectors)
        except json.JSONDecodeError:
            return []
    
    def set_sectors(self, sectors_list):
        """Set sectors from Python list"""
        self.sectors = json.dumps(sectors_list) if sectors_list else ""
    
    def get_skill_keywords(self):
        """Get skill keywords as Python list"""
        if not self.skill_keywords:
            return []
        try:
            return json.loads(self.skill_keywords)
        except json.JSONDecodeError:
            return []
    
    def set_skill_keywords(self, keywords_list):
        """Set skill keywords from Python list"""
        self.skill_keywords = json.dumps(keywords_list) if keywords_list else ""
    
    def get_languages_spoken(self):
        """Get languages as Python list"""
        if not self.languages_spoken:
            return []
        try:
            return json.loads(self.languages_spoken)
        except json.JSONDecodeError:
            return []
    
    def set_languages_spoken(self, languages_list):
        """Set languages from Python list"""
        self.languages_spoken = json.dumps(languages_list) if languages_list else ""
    
    def get_professional_certifications(self):
        """Get certifications as Python list"""
        if not self.professional_certifications:
            return []
        try:
            return json.loads(self.professional_certifications)
        except json.JSONDecodeError:
            return []
    
    def set_professional_certifications(self, certs_list):
        """Set certifications from Python list"""
        self.professional_certifications = json.dumps(certs_list) if certs_list else ""
    
    def get_professional_associations(self):
        """Get associations as Python list"""
        if not self.professional_associations:
            return []
        try:
            return json.loads(self.professional_associations)
        except json.JSONDecodeError:
            return []
    
    def set_professional_associations(self, associations_list):
        """Set associations from Python list"""
        self.professional_associations = json.dumps(associations_list) if associations_list else ""
    
    def get_publications(self):
        """Get publications as Python list"""
        if not self.publications:
            return []
        try:
            return json.loads(self.publications)
        except json.JSONDecodeError:
            return []
    
    def set_publications(self, publications_list):
        """Set publications from Python list"""
        self.publications = json.dumps(publications_list) if publications_list else ""
    
    def get_expertise_details(self):
        """Get expertise details as Python dict"""
        if not self.expertise_details:
            return {}
        try:
            return json.loads(self.expertise_details)
        except json.JSONDecodeError:
            return {}
    
    def set_expertise_details(self, details_dict):
        """Set expertise details from Python dict"""
        self.expertise_details = json.dumps(details_dict) if details_dict else ""
    
    # === DUPLICATE DETECTION METHODS ===
    
    def generate_person_soft_id(self):
        """
        Generate a soft identifier for this person based on name and phone only.
        This creates a fuzzy match to identify the same person across different resumes.
        Phone numbers are ignored to handle cases where same person has multiple phones.
        """
        identity_parts = []
        
        # Normalize and add name components only
        if self.first_name:
            # Remove extra spaces, convert to lowercase, remove common prefixes
            clean_first = re.sub(r'\s+', '', self.first_name.lower().strip())
            clean_first = re.sub(r'^(mr|ms|mrs|dr|prof)\.?', '', clean_first)
            identity_parts.append(clean_first)
            
        if self.last_name:
            clean_last = re.sub(r'\s+', '', self.last_name.lower().strip())
            clean_last = re.sub(r'^(mr|ms|mrs|dr|prof)\.?', '', clean_last)
            identity_parts.append(clean_last)
        
        # Add phone for differentiation, but use a normalized approach
        if self.phone_number:
            clean_phone = ''.join(filter(str.isdigit, self.phone_number))
            if len(clean_phone) >= 7:
                # Use last 7 digits, but also include area code pattern for better differentiation
                area_code = clean_phone[-10:-7] if len(clean_phone) >= 10 else ''
                last_digits = clean_phone[-7:]
                identity_parts.append(f"{area_code}{last_digits}")
        
        # Create base identifier from name+phone
        identity_string = ''.join(identity_parts)
        if identity_string:
            return hashlib.sha256(identity_string.encode()).hexdigest()[:16]
        else:
            return hashlib.sha256(f"unknown_{uuid.uuid4()}".encode()).hexdigest()[:16]
    
    def generate_content_hash(self, resume_text):
        """
        Generate hash from resume content to detect identical files.
        This normalizes the text to catch minor formatting differences.
        """
        if not resume_text or not resume_text.strip():
            return ""
        
        # Normalize text for comparison
        clean_text = resume_text.lower()
        # Remove extra whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text)
        # Remove common formatting characters
        clean_text = re.sub(r'[^\w\s@.-]', '', clean_text)
        # Remove dates that might change (like "Generated on 2023-12-01")
        clean_text = re.sub(r'\b\d{4}-\d{2}-\d{2}\b', '', clean_text)
        clean_text = re.sub(r'\b\d{2}/\d{2}/\d{4}\b', '', clean_text)
        
        return hashlib.sha256(clean_text.strip().encode()).hexdigest()
    
    def extract_file_modification_date(self, file_path):
        """
        Extract file modification date from file metadata if available.
        Returns timezone-aware datetime or None if not available or accessible.
        """
        try:
            if default_storage.exists(file_path):
                # For local files, get modification time
                if hasattr(default_storage, 'path'):
                    try:
                        full_path = default_storage.path(file_path)
                        stat = os.stat(full_path)
                        # Use modification time (when file was last changed)
                        from datetime import datetime
                        from django.utils import timezone
                        modification_time = stat.st_mtime
                        # Create timezone-aware datetime
                        naive_dt = datetime.fromtimestamp(modification_time)
                        return timezone.make_aware(naive_dt)
                    except (AttributeError, OSError):
                        pass
        except Exception:
            pass
        return None
    
    def delete_file(self):
        """
        Delete the associated resume file from storage.
        """
        if self.file_path and default_storage.exists(self.file_path):
            try:
                default_storage.delete(self.file_path)
                return True
            except Exception as e:
                print(f"Error deleting file {self.file_path}: {str(e)}")
                return False
        return False
    
    def get_resume_freshness_score(self):
        """
        Calculate a "freshness" score to determine which resume is more recent.
        Higher score = more recent/fresh resume.
        """
        score = 0
        
        # File creation date gets highest priority (if available)
        if self.file_creation_date:
            # More recent files get higher scores
            from datetime import datetime, timezone
            now = datetime.now(timezone.utc)
            days_old = (now - self.file_creation_date.replace(tzinfo=timezone.utc)).days
            score += max(0, 10000 - days_old)  # Up to 10000 points for very recent files
        
        # Upload timestamp as secondary factor
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        upload_days_old = (now - self.timestamp).days
        score += max(0, 5000 - upload_days_old)  # Up to 5000 points for recent uploads
        
        # Years of experience as tie-breaker (more experience might indicate more recent resume)
        if self.years_of_experience:
            score += min(self.years_of_experience * 10, 1000)  # Up to 1000 points for experience
        
        # Total experience months for finer granularity
        if self.total_experience_months:
            score += min(self.total_experience_months, 500)  # Up to 500 points
        
        return score
    
    @classmethod
    def find_identical_content(cls, content_hash):
        """
        Find resume with identical content.
        """
        if not content_hash:
            return None
        return cls.objects.filter(content_hash=content_hash).first()
    
    @classmethod
    def are_phones_similar(cls, phone1, phone2):
        """
        Check if two phone numbers might belong to the same person.
        Returns True if phones are similar enough to be the same person.
        """
        if not phone1 or not phone2:
            return False
            
        # Normalize both phones
        clean1 = ''.join(filter(str.isdigit, phone1))
        clean2 = ''.join(filter(str.isdigit, phone2))
        
        if len(clean1) < 7 or len(clean2) < 7:
            return False
        
        # Same phone number
        if clean1 == clean2:
            return True
            
        # Same last 7 digits (local number same, area code different)
        if clean1[-7:] == clean2[-7:]:
            return True
            
        # Same last 4 digits + similar length (might be work vs personal)
        if len(clean1) >= 10 and len(clean2) >= 10:
            if clean1[-4:] == clean2[-4:] and abs(len(clean1) - len(clean2)) <= 1:
                return True
        
        return False

    @classmethod
    def find_same_person(cls, person_soft_id):
        """
        Find all resumes for the same person, ordered by freshness (most recent first).
        """
        if not person_soft_id:
            return cls.objects.none()
        
        resumes = cls.objects.filter(person_soft_id=person_soft_id).order_by('-timestamp')
        
        # Sort by freshness score if we have multiple resumes
        if resumes.count() > 1:
            resumes_list = list(resumes)
            resumes_list.sort(key=lambda r: r.get_resume_freshness_score(), reverse=True)
            return resumes_list
        
        return list(resumes)

    @classmethod
    def find_similar_person_by_name_and_phone(cls, first_name, last_name, phone_number):
        """
        Find existing resumes for people with same name and similar phone numbers.
        This helps catch same person using different phones (work/personal).
        """
        if not first_name or not last_name:
            return []
            
        # Normalize names for comparison
        clean_first = re.sub(r'\s+', '', first_name.lower().strip()) if first_name else ''
        clean_first = re.sub(r'^(mr|ms|mrs|dr|prof)\.?', '', clean_first)
        clean_last = re.sub(r'\s+', '', last_name.lower().strip()) if last_name else ''
        clean_last = re.sub(r'^(mr|ms|mrs|dr|prof)\.?', '', clean_last)
        
        # Find all resumes with matching names
        name_matches = cls.objects.filter(
            first_name__icontains=clean_first,
            last_name__icontains=clean_last
        )
        
        similar_resumes = []
        for resume in name_matches:
            if cls.are_phones_similar(phone_number, resume.phone_number):
                similar_resumes.append(resume)
        
        return similar_resumes
    
    @classmethod
    def handle_duplicate_resume(cls, parsed_data, file_path, resume_text):
        """
        Main method to handle duplicate detection and return the action to take.
        
        Returns:
        - 'identical': Identical file already exists
        - 'replace': Same person, replace older resume
        - 'keep': No duplicates, keep this resume
        
        Also returns: (action, existing_resume, message)
        """
        # Create temporary resume to generate hashes (without location)
        temp_resume = cls(
            first_name=parsed_data.get('first_name', ''),
            last_name=parsed_data.get('last_name', ''),
            phone_number=parsed_data.get('phone_number', ''),
            years_of_experience=parsed_data.get('years_of_experience'),
            total_experience_months=parsed_data.get('total_experience_months')
        )
        
        # Extract file modification date
        file_modification_date = temp_resume.extract_file_modification_date(file_path)
        if file_modification_date:
            temp_resume.file_creation_date = file_modification_date
        
        # Generate content hash
        content_hash = temp_resume.generate_content_hash(resume_text)
        
        # Check for identical content first
        if content_hash:
            identical_resume = cls.find_identical_content(content_hash)
            if identical_resume:
                return 'identical', identical_resume, f'Identical file already exists for {identical_resume.full_name}'
        
        # Check for same person (exact match first)
        person_soft_id = temp_resume.generate_person_soft_id()
        existing_resumes = cls.find_same_person(person_soft_id)
        
        # If no exact match, check for similar person (same name + similar phone)
        if not existing_resumes:
            existing_resumes = cls.find_similar_person_by_name_and_phone(
                parsed_data.get('first_name', ''),
                parsed_data.get('last_name', ''),
                parsed_data.get('phone_number', '')
            )
        
        if existing_resumes:
            # Compare freshness scores
            temp_resume.content_hash = content_hash
            new_score = temp_resume.get_resume_freshness_score()
            existing_resume = existing_resumes[0]  # Most recent existing resume
            existing_score = existing_resume.get_resume_freshness_score()
            
            if new_score > existing_score:
                return 'replace', existing_resume, f'Replacing older resume for {existing_resume.full_name}'
            else:
                return 'older', existing_resume, f'Newer resume already exists for {existing_resume.full_name}'
        
        return 'keep', None, 'No duplicates found' 