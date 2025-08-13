"""
Pure File Document for independent file indexing
This document class handles file indexing without Django model dependencies
"""
from elasticsearch_dsl import Document, Index, Text, Keyword, Integer, Date
from django.conf import settings
import os
import hashlib
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Create the file index
file_index = Index('file_index')
file_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
    analysis={
        'analyzer': {
            'file_analyzer': {
                'type': 'standard',
                'stopwords': '_english_'
            }
        }
    }
)

class FileDocument(Document):
    """
    Pure file-based document for DTSearch-like file indexing
    This indexes actual files directly, independent of database records
    """
    
    # File Identity
    file_path = Keyword()                      # Full path to file
    filename = Text(analyzer='standard')       # Filename with text analysis
    file_extension = Keyword()                 # .pdf, .docx, etc.
    file_hash = Keyword()                      # SHA-256 hash for deduplication
    
    # File Content - The main searchable content
    content = Text(
        analyzer='standard',
        search_analyzer='standard'
    )
    
    # File Physical Properties
    file_size = Integer()                      # File size in bytes
    created_date = Date()                      # File creation date
    modified_date = Date()                     # File modification date
    indexed_date = Date()                      # When file was indexed
    
    # File Metadata

    page_count = Integer()                     # Number of pages (for PDFs)
    word_count = Integer()                     # Estimated word count
    
    # Directory Structure
    directory_path = Keyword()                 # Directory containing file
    relative_path = Keyword()                  # Relative path from base

    class Index:
        name = 'file_index'

    @classmethod
    def create_from_file(cls, file_path: str, base_directory: str = None):
        """
        Create a FileDocument from a physical file
        This is the main method to index files
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return None
            
            # Get file info
            file_stat = os.stat(file_path)
            filename = os.path.basename(file_path)
            file_ext = os.path.splitext(filename)[1].lower()
            
            # Generate file hash
            file_hash = cls.generate_file_hash(file_path)
            if not file_hash:
                return None
                
            # Extract text content
            content = cls.extract_text_from_file(file_path)
            if not content:
                logger.warning(f"No content extracted from: {file_path}")
                content = ""
            
            # Calculate relative path
            if base_directory:
                try:
                    relative_path = os.path.relpath(file_path, base_directory)
                    directory_path = os.path.relpath(os.path.dirname(file_path), base_directory)
                except:
                    relative_path = filename
                    directory_path = os.path.dirname(file_path)
            else:
                relative_path = filename
                directory_path = os.path.dirname(file_path)
            
            # Count words and estimate pages
            word_count = len(content.split()) if content else 0
            page_count = max(1, word_count // 300)  # Rough estimate: 300 words per page
            
            # Create document instance
            doc = cls(
                meta={'id': file_hash},
                file_path=file_path,
                filename=filename,
                file_extension=file_ext,
                file_hash=file_hash,
                content=content,
                file_size=file_stat.st_size,
                created_date=datetime.fromtimestamp(file_stat.st_ctime),
                modified_date=datetime.fromtimestamp(file_stat.st_mtime),
                indexed_date=datetime.now(),
                page_count=page_count,
                word_count=word_count,
                directory_path=directory_path,
                relative_path=relative_path
            )
            
            return doc
            
        except Exception as e:
            logger.error(f"Error creating document from file {file_path}: {e}")
            return None
    
    @staticmethod
    def generate_file_hash(file_path: str) -> str:
        """Generate SHA-256 hash of file content for deduplication"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                # Read file in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"Error generating hash for {file_path}: {e}")
            return None
    
    @staticmethod
    def extract_text_from_file(file_path: str) -> str:
        """Extract text content from various file types"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.pdf':
                return FileDocument.extract_pdf_text(file_path)
            elif file_ext in ['.docx', '.doc']:
                return FileDocument.extract_word_text(file_path)
            elif file_ext in ['.txt', '.rtf']:
                return FileDocument.extract_plain_text(file_path)
            else:
                logger.warning(f"Unsupported file type: {file_ext}")
                return ""
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            return ""
    
    @staticmethod
    def extract_pdf_text(file_path: str) -> str:
        """Extract text from PDF files"""
        try:
            from pypdf import PdfReader
            
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                text_content = []
                
                for page in reader.pages:
                    try:
                        page_text = page.extract_text()
                        if page_text.strip():
                            text_content.append(page_text)
                    except Exception as e:
                        logger.warning(f"Error extracting page from {file_path}: {e}")
                        continue
                
                return '\n'.join(text_content)
                
        except ImportError:
            logger.error("pypdf not installed. Install with: pip install pypdf")
            return ""
        except Exception as e:
            logger.error(f"Error reading PDF {file_path}: {e}")
            return ""
    
    @staticmethod
    def extract_word_text(file_path: str) -> str:
        """Extract text from Word documents"""
        try:
            from unstructured.partition.docx import partition_docx
            from unstructured.partition.doc import partition_doc
            
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.docx':
                elements = partition_docx(filename=file_path)
            else:  # .doc
                elements = partition_doc(filename=file_path)
            
            # Extract text from elements
            text_content = []
            for element in elements:
                if hasattr(element, 'text') and element.text.strip():
                    text_content.append(element.text)
            
            return '\n'.join(text_content)
            
        except ImportError:
            logger.error("unstructured not installed. Install with: pip install unstructured")
            return ""
        except Exception as e:
            logger.error(f"Error reading Word document {file_path}: {e}")
            return ""
    
    @staticmethod
    def extract_plain_text(file_path: str) -> str:
        """Extract text from plain text files"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        return file.read()
                except UnicodeDecodeError:
                    continue
            
            # If all encodings fail, try binary mode and decode with errors
            with open(file_path, 'rb') as file:
                raw_content = file.read()
                return raw_content.decode('utf-8', errors='ignore')
                
        except Exception as e:
            logger.error(f"Error reading text file {file_path}: {e}")
            return ""



# Connect document to index
FileDocument._index = file_index
