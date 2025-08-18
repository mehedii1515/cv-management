"""
DOC to DOCX Converter Service
Converts legacy .doc files to modern .docx format for consistent processing
"""
import os
import logging
import subprocess
import tempfile
from pathlib import Path
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

logger = logging.getLogger(__name__)

class DocToDocxConverter:
    """
    Service to convert .doc files to .docx format using LibreOffice
    """
    
    def __init__(self):
        """Initialize the converter"""
        self.libreoffice_cmd = self._find_libreoffice()
        if not self.libreoffice_cmd:
            logger.warning("LibreOffice not found. DOC to DOCX conversion will not work.")
    
    def _find_libreoffice(self):
        """
        Find LibreOffice executable on the system
        
        Returns:
            str: Path to LibreOffice executable or None if not found
        """
        possible_paths = [
            'libreoffice',  # Linux/Mac with PATH
            '/usr/bin/libreoffice',  # Linux
            '/Applications/LibreOffice.app/Contents/MacOS/soffice',  # macOS
            r'C:\Program Files\LibreOffice\program\soffice.exe',  # Windows
            r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',  # Windows 32-bit
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, '--version'], 
                                      capture_output=True, 
                                      timeout=10)
                if result.returncode == 0:
                    logger.info(f"Found LibreOffice at: {path}")
                    return path
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                continue
        
        return None
    
    def convert_doc_to_docx(self, doc_file_path: str) -> str:
        """
        Convert a .doc file to .docx format
        
        Args:
            doc_file_path: Path to the .doc file
            
        Returns:
            str: Path to the converted .docx file
            
        Raises:
            Exception: If conversion fails
        """
        if not self.libreoffice_cmd:
            raise Exception("LibreOffice not available for DOC to DOCX conversion")
        
        try:
            # Ensure we have absolute path
            if not os.path.isabs(doc_file_path):
                doc_file_path = default_storage.path(doc_file_path)
            
            if not os.path.exists(doc_file_path):
                raise FileNotFoundError(f"DOC file not found: {doc_file_path}")
            
            # Create output directory
            doc_dir = os.path.dirname(doc_file_path)
            doc_name = os.path.splitext(os.path.basename(doc_file_path))[0]
            
            logger.info(f"Converting DOC to DOCX: {doc_file_path}")
            
            # LibreOffice command to convert DOC to DOCX
            cmd = [
                self.libreoffice_cmd,
                '--headless',  # Run without GUI
                '--convert-to', 'docx',  # Convert to DOCX format
                '--outdir', doc_dir,  # Output directory
                doc_file_path  # Input file
            ]
            
            # Run conversion
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,  # 60 second timeout
                cwd=doc_dir
            )
            
            if result.returncode != 0:
                error_msg = f"LibreOffice conversion failed: {result.stderr}"
                logger.error(error_msg)
                raise Exception(error_msg)
            
            # Check if DOCX file was created
            docx_file_path = os.path.join(doc_dir, f"{doc_name}.docx")
            
            if not os.path.exists(docx_file_path):
                raise Exception(f"DOCX file was not created: {docx_file_path}")
            
            logger.info(f"Successfully converted DOC to DOCX: {docx_file_path}")
            return docx_file_path
            
        except subprocess.TimeoutExpired:
            raise Exception("DOC to DOCX conversion timed out")
        except Exception as e:
            logger.error(f"Error converting DOC to DOCX: {str(e)}")
            raise
    
    def convert_and_replace(self, doc_file_path: str) -> str:
        """
        Convert DOC to DOCX and replace the original file in storage
        
        Args:
            doc_file_path: Relative path to the DOC file in storage
            
        Returns:
            str: New relative path to the DOCX file
        """
        try:
            # Get absolute path
            absolute_doc_path = default_storage.path(doc_file_path)
            
            # Convert to DOCX
            absolute_docx_path = self.convert_doc_to_docx(absolute_doc_path)
            
            # Create new storage path
            doc_dir = os.path.dirname(doc_file_path)
            doc_name = os.path.splitext(os.path.basename(doc_file_path))[0]
            new_docx_path = os.path.join(doc_dir, f"{doc_name}.docx")
            
            # Read the converted DOCX file
            with open(absolute_docx_path, 'rb') as docx_file:
                docx_content = docx_file.read()
            
            # Save to Django storage
            final_docx_path = default_storage.save(new_docx_path, ContentFile(docx_content))
            
            # Clean up temporary DOCX file
            if os.path.exists(absolute_docx_path):
                os.remove(absolute_docx_path)
            
            # Optionally remove original DOC file
            if default_storage.exists(doc_file_path):
                default_storage.delete(doc_file_path)
                logger.info(f"Removed original DOC file: {doc_file_path}")
            
            logger.info(f"DOC converted and stored as DOCX: {final_docx_path}")
            return final_docx_path
            
        except Exception as e:
            logger.error(f"Error in convert_and_replace: {str(e)}")
            raise
    
    def is_available(self) -> bool:
        """
        Check if DOC to DOCX conversion is available
        
        Returns:
            bool: True if LibreOffice is available for conversion
        """
        return self.libreoffice_cmd is not None


# Global instance
doc_converter = DocToDocxConverter()
