from typing import Tuple
import openai, os, json, re, concurrent.futures
import pandas as pd
import tiktoken
import requests
from datetime import datetime

from Include import Config
import Include.Filestream as fs

# Configurations and constants
OUTPUT_FILE = Config.OUTPUT_FOLDER + "tokens.json"
OUTPUT_EXCEL = "Resume_Classification.xlsx"

# SOURCE_FOLDER = r"\\server\MSL-DATA\PROJECTS\DEAD PROJECTS"
# DESTINATION_FOLDER = r"\\server\MSL-DATA\QueryMind CVs"

SOURCE_FOLDER = ".\\DROPPED PROJECTS\\"
DESTINATION_FOLDER = ".\\CVs\\"

LOG_FILE = "processed_files.json"
BATCH_SIZE = 1000

# Resume Parser Integration Settings
RESUME_PARSER_URL = "http://localhost:8000"  # Your Django backend URL
RESUME_PARSER_ENDPOINT = "/api/resumes/upload/"  # Correct upload endpoint
INTEGRATION_ENABLED = True  # Set to True to enable integration

tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

def load_processed_files():
    """Load the set of processed file paths from the JSON log."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set()
    return set()

def save_processed_files(processed_files):
    """Save the set of processed file paths to the JSON log."""
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(list(processed_files), f, ensure_ascii=False, indent=2)

def Tokenize_Data(data: str, max_tokens: int = 500):
    tokens = tokenizer.encode(data)
    truncated_tokens = tokens[:max_tokens]
    return tokenizer.decode(truncated_tokens)

def AI_Extract_Data(prompt: str) -> str:
    openai.api_key = Config.InitialiseAPI()
    response = openai.chat.completions.create(
        model=Config.GPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in document classification. "
                    "Your task is to determine if the given document is a resume (CV). "
                    "If it contains clear resume features like (name, contact, work history, employer, position, "
                    "education, qualifications date of birth, country of citizenship, employment record), respond 'Yes'. "
                    "If unsure, respond 'No'. "
                    "Only answer 'Yes' or 'No', nothing else."
                )
            },
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# UPDATED: Removed confidence-based logic. Now, both branches simply check if the answer is "yes".
def IsResume_With_Confidence(data: str, ocr: bool = False) -> bool:
    """
    Returns True if the document is classified as a resume, False otherwise.
    
    - If OCR is used, the prompt notes that OCR was applied and instructs:
         "Respond with 'Yes' or 'No' only. If unsure, respond 'Yes'."
    - If OCR is not used, a simpler prompt is used that expects exactly "Yes" or "No".
    """
    if not data.strip():
        return False
    if ocr:
        prompt = (
            f"Identify whether this is a Resume of a person. Note: The text was extracted using OCR. "
            f"Respond with 'Yes' or 'No' only. If unsure, respond 'Yes'.\n\n{data}"
        )
    else:
        prompt = (
            "You are an expert in document classification. "
            "Your task is to determine if the given document is a resume (CV). "
            "If it contains clear resume features like (name, contact, work history, employer, position, "
            "education, qualifications date of birth, country of citizenship, employment record), respond 'Yes'. "
            "If unsure, respond 'No'. "
            "Only answer 'Yes' or 'No', nothing else.\n\n" + data
        )
    response = AI_Extract_Data(prompt)
    response_clean = response.strip("```").removeprefix("json").strip().lower()
    return (response_clean == "yes")

def send_cv_to_resume_parser(file_path: str, file_name: str) -> bool:
    """Send detected CV to the resume parser API."""
    if not INTEGRATION_ENABLED:
        print(f"🔗 Integration disabled - would send {file_name} to resume parser")
        return True
    
    try:
        file_extension = file_name.split('.')[-1].lower()
        
        # For .doc files, extract text first and send as .txt to avoid LibreOffice dependency
        if file_extension == 'doc':
            print(f"🔄 Converting .doc to text for resume parser: {file_name}")
            
            # Extract text using QueryMind's Spire.doc
            doc_text = fs.Extract_Text_From_DOC(file_path)
            
            if not doc_text.strip():
                print(f"⚠️ No text extracted from {file_name}")
                return False
            
            # Create a temporary text file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(doc_text)
                temp_file_path = temp_file.name
            
            try:
                # Send the text file instead
                with open(temp_file_path, 'rb') as f:
                    txt_filename = file_name.replace('.doc', '.txt')
                    files = {'file': (txt_filename, f)}
                    data = {
                        'parse_immediately': True,
                        'source': 'QueryMind_AutoDetect_DOC_Converted',
                        'auto_detected': True,
                        'original_filename': file_name,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    response = requests.post(
                        f"{RESUME_PARSER_URL}{RESUME_PARSER_ENDPOINT}",
                        files=files,
                        data=data,
                        timeout=120
                    )
                    
                    if response.status_code in [200, 201]:
                        print(f"✅ CV sent to resume parser (converted to text): {file_name}")
                        return True
                    else:
                        print(f"⚠️ Resume parser API error for {file_name}: {response.status_code}")
                        print(f"   Response: {response.text}")
                        return False
            finally:
                # Clean up temporary file
                import os
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
        
        else:
            # For other file types, send the original file
            with open(file_path, 'rb') as f:
                files = {'file': (file_name, f)}
                data = {
                    'parse_immediately': True,
                    'source': 'QueryMind_AutoDetect',
                    'auto_detected': True,
                    'timestamp': datetime.now().isoformat()
                }
                
                response = requests.post(
                    f"{RESUME_PARSER_URL}{RESUME_PARSER_ENDPOINT}",
                    files=files,
                    data=data,
                    timeout=120
                )
                
                if response.status_code in [200, 201]:
                    print(f"✅ CV sent to resume parser: {file_name}")
                    return True
                else:
                    print(f"⚠️ Resume parser API error for {file_name}: {response.status_code}")
                    print(f"   Response: {response.text}")
                    return False
                
    except Exception as e:
        print(f"❌ Failed to send {file_name} to resume parser: {e}")
        return False

def save_results_to_excel(results: list):
    """Save classification results to an Excel file."""
    # Excel now has three columns: File Name, Is Resume, and OCR indicator.
    df = pd.DataFrame(results, columns=["File Name", "Is Resume", "OCR"])
    df.to_excel(OUTPUT_EXCEL, index=False, engine="openpyxl")
    print(f"\nResults saved to '{OUTPUT_EXCEL}'.")

def word_in_filename(word: str, file_lower: str) -> bool:
    # Treat underscores as delimiters using regex boundaries.
    pattern = r'(?<![A-Za-z0-9])' + re.escape(word) + r'(?![A-Za-z0-9])'
    return re.search(pattern, file_lower) is not None

def process_file(FileLocation: str) -> Tuple[str, str, str]:
    """
    Process an individual file and return a tuple (file name, classification result, OCR indicator).
    The classification result is either "YES" or "NO".
    If OCR fallback was used, the OCR indicator is "OCR"; otherwise, it is blank.
    """
    file = os.path.basename(FileLocation)
    file_lower = file.lower()
    result = None
    ocr_indicator = ""

    # Define keywords and patterns
    yes_words = ["cv", "resume", "curriculum vitae"]
    no_words = [
        "proposal", "cover letter", "rfp", "notice", "tor", "pds", "agreement",
        "contract", "memorandum", "invoice", "report", "hot", "head_of_terms",
        "statement", "questionnaire", "association", "pid",
        "declaration of availability", "letter of consent", "letter of commitment", 
        "eoi", "expression of interest", "certificate", "acknowledgement", 
        "terms of reference", "consent letter", "list", "declaration", "certification", 
        "project description", "tors", "letter of submission", "project document", 
        "affidavit", "power of attorney", "schedule", "roi", "loi", "letter of intent", 
        "bidding", "amendment", "addendum", "call for proposals", "call for expression", 
        "call for bids", "appendix", "appendices", "schedule", "policies", "mou", 
        "memorandum of understanding", "memorandum", "moa", "sla", "bill", 
        "bill of quantities", "boq", "receipt", "voucher", "claim", "chalan",
        "timesheet", "invoice", "feasibility", "methodology", "technical proposal", 
        "financial proposal", "concept note", "scope of work", "sow", 
        "technical specification", "presentation", "agenda", "guideline", "manual", 
        "sop", "brochure", "datasheet", "data sheet", "exhibit", "appendix", "minutes",
        "abstract", "cover sheet", "cover page", "title page", "capability statement",
        "table of contents", "availability letter", "letter to"
    ]
    skip_starts = ["~$", "~", "._"]
    allowed_extensions = [".pdf", ".doc", ".docx", ".txt", ".rtf"]

    if any(file_lower.startswith(prefix) for prefix in skip_starts) or not any(file_lower.endswith(ext) for ext in allowed_extensions):
        result = "Invalid File"
        return file, result, ""

    if any(word in file_lower for word in yes_words):
        result = "YES (FOR SURE)"
        return file, result, ""
    elif any(word_in_filename(word, file_lower) for word in no_words):
        result = "NO (FOR SURE)"
        return file, result, ""

    data = ""
    used_ocr = False
    if file_lower.endswith(".pdf"):
        data = fs.Extract_Text_From_pdf(FileLocation)
        if len(data.strip()) < 50:
            print(f"Standard PDF extraction produced little text for {file}, trying OCR fallback...")
            data = fs.Extract_Text_From_PDF_OCR(FileLocation)
            used_ocr = True
    elif file_lower.endswith(".docx"):
        data = fs.Extract_Text_From_DOCX(FileLocation)
    elif file_lower.endswith(".doc"):
        data = fs.Extract_Text_From_DOC(FileLocation)
    elif file_lower.endswith(".rtf"):
        data = fs.Extract_Text_From_RTF(FileLocation)
    elif file_lower.endswith(".txt"):
        data = fs.Extract_Text_From_TXT(FileLocation)

    tokenized_data = Tokenize_Data(data)
    is_resume = IsResume_With_Confidence(tokenized_data, ocr=used_ocr)
    result = "YES" if is_resume else "NO"
    if used_ocr:
        ocr_indicator = "OCR"
    # print(f"File '{file}' processed with result: {result} {ocr_indicator}")
    return file, result, ocr_indicator

def PerformForFilesInFolders(Folder: str, DestinationFolder: str):
    results = []  # For storing classification results for Excel
    processed_log = load_processed_files()

    total_all_files = []
    for root, _, files in os.walk(Folder, topdown=True):
        for file in files:
            total_all_files.append(os.path.join(root, file))
    total_files_count = len(total_all_files)

    new_files = [file_path for file_path in total_all_files if file_path not in processed_log]
    total_new_files = len(new_files)
    print(f"Total files in folder: {total_files_count}")
    print(f"New files detected: {total_new_files}")
    if total_new_files == 0:
        print("No new files found in the folder.")
        return

    files_to_process = new_files[:BATCH_SIZE]

    # Initialize OCR counters and integration counters
    ocr_counter = 0
    ocr_yes = 0
    ocr_no = 0
    cvs_found = 0
    cvs_sent_to_parser = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=14) as executor:
        future_to_file = {executor.submit(process_file, file_path): file_path for file_path in files_to_process}
        batch_count = 0
        for future in concurrent.futures.as_completed(future_to_file):
            try:
                file_name, result, ocr_flag = future.result()
                results.append([file_name, result, ocr_flag])
                file_path = future_to_file[future]
                processed_log.add(file_path)
                batch_count += 1
                
                # OCR tracking
                if ocr_flag == "OCR":
                    ocr_counter += 1
                    if result.startswith("YES"):
                        ocr_yes += 1
                    elif result == "NO":
                        ocr_no += 1
                
                # Integration: Send CVs to resume parser
                if result.startswith("YES"):
                    cvs_found += 1
                    if send_cv_to_resume_parser(file_path, file_name):
                        cvs_sent_to_parser += 1
                
                print(f"Batch Progress: {batch_count}/{len(files_to_process)} files processed.")
            except Exception as exc:
                print(f"Error processing file: {future_to_file[future]}. Exception: {exc}")

    save_processed_files(processed_log)
    print(f"\nBatch complete: Processed {batch_count} files in this run.")
    print(f"Total files in folder (to be eventually processed): {total_files_count}")
    print(f"\nTotal times OCR was used: {ocr_counter}")
    print(f"Total times OCR was used and result was YES: {ocr_yes}")
    print(f"Total times OCR was used and result was NO: {ocr_no}")
    
    # Integration statistics
    print(f"\n📊 Integration Statistics:")
    print(f"CVs found: {cvs_found}")
    print(f"CVs sent to resume parser: {cvs_sent_to_parser}")
    if cvs_found > 0:
        success_rate = (cvs_sent_to_parser / cvs_found) * 100
        print(f"Integration success rate: {success_rate:.1f}%")
    
    if INTEGRATION_ENABLED:
        print("🔗 Integration with resume parser is ENABLED")
    else:
        print("🔗 Integration with resume parser is DISABLED")
        print("   Set INTEGRATION_ENABLED = True to enable automatic CV sending")
    
    print("\nSummary of files processed in this batch:")
    # for file, result, ocr_flag in results:
    #     print(f"{file} ---- {result} {ocr_flag}")

    save_results_to_excel(results)
    print(f"\nResults saved to '{OUTPUT_EXCEL}'.")

def main():
    PerformForFilesInFolders(SOURCE_FOLDER, DESTINATION_FOLDER)

if __name__ == "__main__":
    main()
