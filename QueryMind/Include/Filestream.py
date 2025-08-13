from spire.doc import *
from spire.doc.common import *
from pypdf import PdfReader
import shutil
import os
import yaml
from striprtf.striprtf import rtf_to_text

# OCR-related modules
from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np

def Extract_Text_From_DOCX(FileName: str, max_tokens=500) -> str: 
    try:
        doc = Document()
        doc.LoadFromFile(FileName)
        doc_text = doc.GetText()
        doc.Close()
    except Exception as ex:
        print("{0} error occurred. Arguments: {1}".format(type(ex).__name__, ex.args))
        doc_text = ""
    return doc_text

def Extract_Text_From_DOC(FileName: str, max_tokens=500) -> str: 
    """Extract text from .doc files using Spire.doc library"""
    try:
        doc = Document()
        doc.LoadFromFile(FileName)
        doc_text = doc.GetText()
        doc.Close()
    except Exception as ex:
        print("{0} error occurred. Arguments: {1}".format(type(ex).__name__, ex.args))
        doc_text = ""
    return doc_text

def Extract_Text_From_pdf(FileName: str) -> str:
    pdf_text = ""
    try:
        pdf = PdfReader(FileName)
        for page_number, page in enumerate(pdf.pages):
            pdf_text += f"page: {page_number}" + page.extract_text()
    except Exception as ex:
        print("{0} error occurred. Arguments: {1}".format(type(ex).__name__, ex.args))
    return pdf_text

def Extract_Text_From_RTF(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            rtf_data = f.read()
        text = rtf_to_text(rtf_data)
        return text
    except Exception as ex:
        print(f"Error extracting RTF from {file_path}: {ex}")
        return ""

def Extract_Text_From_TXT(file_path: str) -> str:
    """Extract text from .txt files"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return text
    except UnicodeDecodeError:
        # Try with different encodings if utf-8 fails
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                text = f.read()
            return text
        except Exception as ex:
            print(f"Error extracting text from {file_path}: {ex}")
            return ""
    except Exception as ex:
        print(f"Error extracting text from {file_path}: {ex}")
        return ""

def Write_Text_To_File(Data: str, Filename: str) -> None:
    try:
        with open(Filename, 'w', encoding='utf-8') as file:
            file.write(Data)
    except Exception as ex:
        print("{0} error occurred. Arguments: {1}".format(type(ex).__name__, ex.args))

def Extract_Text_From_PDF_OCR(file_path: str, dpi: int = 300) -> str:
    """
    Extract text from a PDF using OCR as a fallback.
    Converts PDF pages to images in memory and uses pytesseract to extract text.
    Does not save any image files.
    """
    text = ""
    try:
        pages = convert_from_path(file_path, dpi=dpi)
        for page in pages:
            open_cv_image = np.array(page)
            open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
            page_text = pytesseract.image_to_string(gray)
            text += page_text + "\n"
    except Exception as ex:
        print(f"OCR extraction error for {file_path}: {ex}")
    return text
