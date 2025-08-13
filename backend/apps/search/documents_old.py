from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from apps.resumes.models import Resume
import os
import hashlib


# Create Elasticsearch index
cv_index = Index('cv_documents')
cv_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
    analysis={
        'analyzer': {
            'cv_analyzer': {
                'type': 'standard',
                'stopwords': '_english_'
            },
            'skills_analyzer': {
                'type': 'keyword',
                'lowercase': True
            }
        }
    }
)


@registry.register_document
class CVDocument(Document):
    """
    Elasticsearch document for CV/Resume indexing and search
    This provides DTSearch-like functionality for CV content
    """
    
    # Personal Information (from database)
    first_name = fields.TextField(analyzer='cv_analyzer')
    last_name = fields.TextField(analyzer='cv_analyzer')
    full_name = fields.TextField(analyzer='cv_analyzer')
    email = fields.KeywordField()
    phone_number = fields.KeywordField()
    location = fields.TextField(analyzer='cv_analyzer')
    
    # Professional Information (from database)
    current_employer = fields.TextField(analyzer='cv_analyzer')
    years_of_experience = fields.IntegerField()
    total_experience_months = fields.IntegerField()
    availability = fields.TextField(analyzer='cv_analyzer')
    
    # Skills and Expertise (from database JSON fields)
    expertise_areas = fields.TextField(analyzer='skills_analyzer')
    sectors = fields.TextField(analyzer='skills_analyzer')
    skill_keywords = fields.TextField(analyzer='skills_analyzer')
    languages_spoken = fields.TextField(analyzer='skills_analyzer')
    
    # Education and Certifications (from database)
    professional_certifications = fields.TextField(analyzer='cv_analyzer')
    professional_associations = fields.TextField(analyzer='cv_analyzer')
    publications = fields.TextField(analyzer='cv_analyzer')
    
    # File Information (from database)
    original_filename = fields.TextField(analyzer='cv_analyzer')
    file_path = fields.KeywordField()
    file_type = fields.KeywordField()
    
    # File Content (extracted from actual files - DTSearch-like)
    extracted_text = fields.TextField(
        analyzer='cv_analyzer',
        fields={
            'raw': fields.KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )
    
    # Metadata for search optimization
    content_hash = fields.KeywordField()
    file_size = fields.IntegerField()
    indexed_date = fields.DateField()
    processing_status = fields.KeywordField()
    
    # Timestamps
    created_at = fields.DateField()
    updated_at = fields.DateField()
    
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
            'timestamp',
        ]
    
    def prepare_full_name(self, instance):
        """Combine first and last name for easier searching"""
        return f"{instance.first_name} {instance.last_name}".strip()
    
    def prepare_expertise_areas(self, instance):
        """Convert JSON expertise areas to searchable text"""
        try:
            import json
            if instance.expertise_areas:
                areas = json.loads(instance.expertise_areas)
                return ' '.join(areas) if isinstance(areas, list) else str(areas)
        except (json.JSONDecodeError, TypeError):
            pass
        return instance.expertise_areas or ""
    
    def prepare_sectors(self, instance):
        """Convert JSON sectors to searchable text"""
        try:
            import json
            if instance.sectors:
                sectors = json.loads(instance.sectors)
                return ' '.join(sectors) if isinstance(sectors, list) else str(sectors)
        except (json.JSONDecodeError, TypeError):
            pass
        return instance.sectors or ""
    
    def prepare_skill_keywords(self, instance):
        """Convert JSON skill keywords to searchable text"""
        try:
            import json
            if instance.skill_keywords:
                keywords = json.loads(instance.skill_keywords)
                return ' '.join(keywords) if isinstance(keywords, list) else str(keywords)
        except (json.JSONDecodeError, TypeError):
            pass
        return instance.skill_keywords or ""
    
    def prepare_languages_spoken(self, instance):
        """Convert JSON languages to searchable text"""
        try:
            import json
            if instance.languages_spoken:
                languages = json.loads(instance.languages_spoken)
                return ' '.join(languages) if isinstance(languages, list) else str(languages)
        except (json.JSONDecodeError, TypeError):
            pass
        return instance.languages_spoken or ""
    
    def prepare_professional_certifications(self, instance):
        """Convert JSON certifications to searchable text"""
        try:
            import json
            if instance.professional_certifications:
                certs = json.loads(instance.professional_certifications)
                return ' '.join(certs) if isinstance(certs, list) else str(certs)
        except (json.JSONDecodeError, TypeError):
            pass
        return instance.professional_certifications or ""
    
    def prepare_extracted_text(self, instance):
        """
        Extract text from the actual CV file (DTSearch-like functionality)
        This is the core feature that enables searching inside file content
        """
        if not instance.file_path or not os.path.exists(instance.file_path):
            return ""
        
        try:
            return self.extract_file_content(instance.file_path)
        except Exception as e:
            print(f"Error extracting text from {instance.file_path}: {e}")
            return ""
    
    def prepare_content_hash(self, instance):
        """Use existing content hash or generate from file"""
        if instance.content_hash:
            return instance.content_hash
        
        if instance.file_path and os.path.exists(instance.file_path):
            try:
                with open(instance.file_path, 'rb') as f:
                    return hashlib.md5(f.read()).hexdigest()
            except Exception:
                pass
        return ""
    
    def prepare_file_size(self, instance):
        """Get file size in bytes"""
        if instance.file_path and os.path.exists(instance.file_path):
            try:
                return os.path.getsize(instance.file_path)
            except Exception:
                pass
        return 0
    
    def prepare_indexed_date(self, instance):
        """Set current date as indexed date"""
        from datetime import datetime
        return datetime.now().date()
    
    def extract_file_content(self, file_path):
        """
        Extract text content from CV files (DTSearch-like)
        Supports PDF, DOC, DOCX, TXT files
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
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
            print(f"Error extracting {file_extension} content: {e}")
            return ""
    
    def extract_pdf_content(self, file_path):
        """Extract text from PDF files"""
        try:
            from unstructured.partition.pdf import partition_pdf
            elements = partition_pdf(filename=file_path)
            text_content = []
            for element in elements:
                if hasattr(element, 'text') and element.text.strip():
                    text_content.append(element.text.strip())
            return '\n'.join(text_content)
        except Exception as e:
            # Fallback to pypdf if unstructured fails
            try:
                from pypdf import PdfReader
                pdf = PdfReader(file_path)
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                return text
            except Exception:
                return ""
    
    def extract_docx_content(self, file_path):
        """Extract text from DOCX files"""
        try:
            from unstructured.partition.docx import partition_docx
            elements = partition_docx(filename=file_path)
            text_content = []
            for element in elements:
                if hasattr(element, 'text') and element.text.strip():
                    text_content.append(element.text.strip())
            return '\n'.join(text_content)
        except Exception:
            return ""
    
    def extract_doc_content(self, file_path):
        """Extract text from DOC files"""
        try:
            from unstructured.partition.doc import partition_doc
            elements = partition_doc(filename=file_path)
            text_content = []
            for element in elements:
                if hasattr(element, 'text') and element.text.strip():
                    text_content.append(element.text.strip())
            return '\n'.join(text_content)
        except Exception:
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
            except Exception:
                return ""
        except Exception:
            return ""
