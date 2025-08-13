import os
import logging
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.docx import partition_docx
from unstructured.partition.doc import partition_doc
from unstructured.partition.text import partition_text
from unstructured.partition.rtf import partition_rtf

logger = logging.getLogger(__name__)

class UnstructuredService:
    """
    Service for extracting text from PDF, DOCX, DOC, TXT, and RTF files using the unstructured library.
    Supports only these five file formats.
    """
    
    SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.txt', '.rtf'}
    
    def __init__(self):
        """Initialize the UnstructuredService."""
        logger.info("UnstructuredService initialized for PDF, DOCX, DOC, TXT, and RTF files")
    
    @property
    def supported_formats(self):
        """
        Property to get list of supported file formats.
        
        Returns:
            list: List of supported file extensions
        """
        return list(self.SUPPORTED_EXTENSIONS)
    
    def extract_text(self, file_path):
        """
        Extract text from a file using the appropriate unstructured partition function.
        
        Args:
            file_path (str): Path to the file to extract text from (can be relative or absolute)
            
        Returns:
            str: Extracted text content
            
        Raises:
            ValueError: If file format is not supported
            Exception: If extraction fails
        """
        try:
            # Get file extension
            file_extension = os.path.splitext(file_path)[1].lower()
            
            # Check if file format is supported
            if file_extension not in self.SUPPORTED_EXTENSIONS:
                raise ValueError(f"Unsupported file format: {file_extension}. Supported formats: {', '.join(self.SUPPORTED_EXTENSIONS)}")
            
            # Convert relative path to absolute path using Django's storage system
            if not os.path.isabs(file_path):
                try:
                    # Try to get absolute path from Django storage
                    absolute_path = default_storage.path(file_path)
                    logger.info(f"Converted relative path '{file_path}' to absolute path '{absolute_path}'")
                    file_path = absolute_path
                except (NotImplementedError, AttributeError):
                    # Fallback: construct path manually
                    from django.conf import settings
                    media_root = getattr(settings, 'MEDIA_ROOT', '')
                    if media_root:
                        absolute_path = os.path.join(media_root, file_path)
                        logger.info(f"Constructed absolute path '{absolute_path}' from relative path '{file_path}'")
                        file_path = absolute_path
            
            # Verify file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            logger.info(f"Processing file: {file_path}")
            
            # Extract text based on file type
            elements = []
            
            if file_extension == '.pdf':
                logger.info(f"Extracting text from PDF: {file_path}")
                elements = partition_pdf(filename=file_path)
                
            elif file_extension == '.docx':
                logger.info(f"Extracting text from DOCX: {file_path}")
                elements = partition_docx(filename=file_path)
                
            elif file_extension == '.doc':
                logger.info(f"Extracting text from DOC: {file_path}")
                elements = partition_doc(filename=file_path)
                
            elif file_extension == '.txt':
                logger.info(f"Extracting text from TXT: {file_path}")
                elements = partition_text(filename=file_path)
                
            elif file_extension == '.rtf':
                logger.info(f"Extracting text from RTF: {file_path}")
                elements = partition_rtf(filename=file_path)
            
            # Combine all text elements
            text_content = []
            for element in elements:
                if hasattr(element, 'text') and element.text.strip():
                    text_content.append(element.text.strip())
            
            extracted_text = '\n'.join(text_content)
            
            if not extracted_text.strip():
                logger.warning(f"No text extracted from file: {file_path}")
                return ""
            
            logger.info(f"Successfully extracted {len(extracted_text)} characters from {file_path}")
            return extracted_text
            
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            raise Exception(f"Failed to extract text: {str(e)}")
    
    def extract_from_uploaded_file(self, uploaded_file):
        """
        Extract text from a Django uploaded file.
        
        Args:
            uploaded_file: Django UploadedFile instance
            
        Returns:
            str: Extracted text content
            
        Raises:
            ValueError: If file format is not supported
            Exception: If extraction fails
        """
        try:
            # Get file extension from uploaded file name
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            # Check if file format is supported
            if file_extension not in self.SUPPORTED_EXTENSIONS:
                raise ValueError(f"Unsupported file format: {file_extension}. Supported formats: {', '.join(self.SUPPORTED_EXTENSIONS)}")
            
            # Save uploaded file temporarily
            temp_path = default_storage.save(f'temp/{uploaded_file.name}', ContentFile(uploaded_file.read()))
            
            try:
                # Get the full file path
                full_temp_path = default_storage.path(temp_path)
                
                # Extract text
                extracted_text = self.extract_text(full_temp_path)
                
                return extracted_text
                
            finally:
                # Clean up temporary file
                if default_storage.exists(temp_path):
                    default_storage.delete(temp_path)
                    
        except Exception as e:
            logger.error(f"Error extracting text from uploaded file {uploaded_file.name}: {str(e)}")
            raise Exception(f"Failed to extract text from uploaded file: {str(e)}")
    
    def is_supported_format(self, file_path_or_name):
        """
        Check if a file format is supported.
        
        Args:
            file_path_or_name (str): File path or filename
            
        Returns:
            bool: True if format is supported, False otherwise
        """
        file_extension = os.path.splitext(file_path_or_name)[1].lower()
        return file_extension in self.SUPPORTED_EXTENSIONS
    
    def get_supported_formats(self):
        """
        Get list of supported file formats.
        
        Returns:
            list: List of supported file extensions
        """
        return list(self.SUPPORTED_EXTENSIONS)


# Global instance for easy import
unstructured_service = UnstructuredService()
