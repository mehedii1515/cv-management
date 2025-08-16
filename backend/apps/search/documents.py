from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from apps.resumes.models import Resume
import os
import hashlib
from datetime import datetime

# Create Elasticsearch index with simple settings
@registry.register_document
class CVDocument(Document):
    """DTSearch-like document for Elasticsearch indexing"""
    
    # File metadata fields
    filename = fields.TextField()
    file_path = fields.KeywordField()
    file_size = fields.IntegerField()
    file_type = fields.KeywordField()
    content_hash = fields.KeywordField()
    
    # CV file content (DTSearch-like full-text search)
    extracted_text = fields.TextField()
    
    # CV structured data from database
    name = fields.TextField()
    email = fields.KeywordField()
    phone = fields.KeywordField()
    skills = fields.TextField()
    experience = fields.TextField()
    education = fields.TextField()
    
    # Search metadata
    indexed_date = fields.DateField()
    
    class Index:
        name = 'cv_documents'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
    
    class Django:
        model = Resume
        fields = [
            'id',
            'timestamp',  # Use the actual field name from Resume model
        ]
    
    def prepare_extracted_text(self, instance):
        """Extract text from uploaded file (DTSearch-like functionality)"""
        if instance.file_path:
            try:
                from django.core.files.storage import default_storage
                if default_storage.exists(instance.file_path):
                    if hasattr(default_storage, 'path'):
                        file_path = default_storage.path(instance.file_path)
                        return self.extract_file_content(file_path)
                    else:
                        return self.extract_file_content(instance.file_path)
            except Exception as e:
                print(f"Error extracting text from {instance.file_path}: {e}")
                return ""
        return ""
    
    def prepare_filename(self, instance):
        """Get filename from file field"""
        if instance.original_filename:
            return instance.original_filename
        elif instance.file_path:
            return os.path.basename(instance.file_path)
        return ""
    
    def prepare_file_path(self, instance):
        """Get full file path"""
        if instance.file_path:
            from django.core.files.storage import default_storage
            if hasattr(default_storage, 'path') and default_storage.exists(instance.file_path):
                return default_storage.path(instance.file_path)
            return instance.file_path
        return ""
    
    def prepare_file_size(self, instance):
        """Get file size"""
        if instance.file_path:
            try:
                from django.core.files.storage import default_storage
                if hasattr(default_storage, 'path') and default_storage.exists(instance.file_path):
                    file_path = default_storage.path(instance.file_path)
                    return os.path.getsize(file_path)
            except:
                pass
        return 0
    
    def prepare_file_type(self, instance):
        """Get file extension"""
        if instance.file_type:
            return instance.file_type.lower()
        elif instance.original_filename:
            return os.path.splitext(instance.original_filename)[1].lower()
        elif instance.file_path:
            return os.path.splitext(instance.file_path)[1].lower()
        return ""
    
    def prepare_content_hash(self, instance):
        """Generate hash for duplicate detection"""
        if instance.file_path:
            try:
                from django.core.files.storage import default_storage
                if hasattr(default_storage, 'path') and default_storage.exists(instance.file_path):
                    file_path = default_storage.path(instance.file_path)
                    with open(file_path, 'rb') as f:
                        return hashlib.md5(f.read()).hexdigest()
            except:
                pass
        return ""
        return ""
    
    def prepare_indexed_date(self, instance):
        """Set indexing timestamp"""
        return datetime.now()
    
    def prepare_name(self, instance):
        """Combine first and last name"""
        first_name = getattr(instance, 'first_name', '') or ''
        last_name = getattr(instance, 'last_name', '') or ''
        return f"{first_name} {last_name}".strip()
    
    def prepare_email(self, instance):
        """Get email address"""
        return getattr(instance, 'email', '') or ''
    
    def prepare_phone(self, instance):
        """Get phone number"""
        return getattr(instance, 'phone_number', '') or ''
    
    def prepare_skills(self, instance):
        """Extract skills from various fields"""
        skills = []
        if hasattr(instance, 'skill_keywords') and instance.skill_keywords:
            try:
                import json
                skills.extend(json.loads(instance.skill_keywords))
            except:
                pass
        if hasattr(instance, 'expertise_areas') and instance.expertise_areas:
            try:
                import json
                skills.extend(json.loads(instance.expertise_areas))
            except:
                pass
        return ' '.join(skills)
    
    def prepare_experience(self, instance):
        """Get experience information"""
        exp_parts = []
        if hasattr(instance, 'current_employer') and instance.current_employer:
            exp_parts.append(instance.current_employer)
        if hasattr(instance, 'years_of_experience') and instance.years_of_experience:
            exp_parts.append(f"{instance.years_of_experience} years experience")
        return ' '.join(exp_parts)
    
    def prepare_education(self, instance):
        """Get education information - for now return empty, can be enhanced later"""
        return ''
    
    def extract_file_content(self, file_path):
        """Extract text content from various file types (DTSearch-like)"""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.pdf':
                return self.extract_pdf_content(file_path)
            elif file_extension == '.docx':
                return self.extract_docx_content(file_path)
            elif file_extension == '.doc':
                return self.extract_doc_content(file_path)
            elif file_extension == '.txt':
                return self.extract_txt_content(file_path)
            else:
                return ""
        except Exception as e:
            print(f"Error extracting content from {file_path}: {e}")
            return ""
    
    def extract_pdf_content(self, file_path):
        """Extract text from PDF files"""
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error extracting PDF content: {e}")
            return ""
    
    def extract_docx_content(self, file_path):
        """Extract text from DOCX files"""
        try:
            from unstructured.partition.docx import partition_docx
            elements = partition_docx(filename=file_path)
            return "\n".join([str(element) for element in elements])
        except Exception as e:
            print(f"Error extracting DOCX content: {e}")
            return ""
    
    def extract_doc_content(self, file_path):
        """Extract text from DOC files"""
        try:
            from unstructured.partition.doc import partition_doc
            elements = partition_doc(filename=file_path)
            return "\n".join([str(element) for element in elements])
        except Exception as e:
            print(f"Error extracting DOC content: {e}")
            return ""
    
    def extract_txt_content(self, file_path):
        """Extract text from TXT files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                print(f"Error extracting TXT content: {e}")
                return ""
        except Exception as e:
            print(f"Error extracting TXT content: {e}")
            return ""
