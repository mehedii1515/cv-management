# QueryMind File Watcher Configuration

# Folders to monitor for new resume files
WATCH_FOLDERS = [
    # Your actual server folders (update these paths)
    r"\\server\MSL-DATA\PROJECTS\INCOMING",
    r"\\server\MSL-DATA\SHARED\NEW_DOCUMENTS", 
    r"\\server\MSL-DATA\HR\APPLICATIONS",
    
    # Local test folder
    r".\DROPPED PROJECTS\"
]

# File processing settings
PROCESS_INTERVAL = 5  # seconds between processing batches
FILE_SIZE_THRESHOLD = 1024  # minimum file size in bytes
SUPPORTED_EXTENSIONS = ['.pdf', '.doc', '.docx', '.rtf']

# Integration settings
INTEGRATION_ENABLED = True
RESUME_PARSER_URL = "http://localhost:8000"
RESUME_PARSER_ENDPOINT = "/api/resumes/upload/"

# Logging settings
LOG_LEVEL = "INFO"
STATS_DISPLAY_INTERVAL = 10  # seconds between stats updates
