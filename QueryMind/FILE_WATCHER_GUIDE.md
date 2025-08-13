# QueryMind File Watcher - Automatic Resume Detection

## 🎯 Overview

The QueryMind File Watcher automatically monitors specified folders for new resume files and processes them in real-time. When a new file is detected, it:

1. **Detects** new files immediately using watchdog
2. **Classifies** them as CV/resume or not using AI
3. **Sends** detected CVs to your resume parser automatically
4. **Tracks** statistics in real-time

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install watchdog
```

### 2. Start File Watcher
```bash
# Test mode (monitors DROPPED PROJECTS folder)
python file_watcher.py --test

# Production mode (monitors configured server folders)
python file_watcher.py

# Custom folders
python file_watcher.py --folders "C:\path\to\folder1" "C:\path\to\folder2"
```

### 3. Test the Watcher
```bash
# In another terminal, run the test
python test_watcher.py
```

## 📁 Configuration

Edit `watcher_config.py` to configure your server folders:

```python
WATCH_FOLDERS = [
    r"\\server\MSL-DATA\PROJECTS\INCOMING",
    r"\\server\MSL-DATA\SHARED\NEW_DOCUMENTS", 
    r"\\server\MSL-DATA\HR\APPLICATIONS",
]
```

## 🎛️ Usage Options

### Production Mode
```bash
python file_watcher.py
```
- Monitors all configured server folders
- Processes files automatically
- Runs continuously until stopped

### Test Mode
```bash
python file_watcher.py --test
```
- Monitors only the DROPPED PROJECTS folder
- Good for testing and development

### Custom Folders
```bash
python file_watcher.py --folders "C:\HR\CVs" "C:\Applications"
```
- Monitor specific folders
- Useful for one-time setups

## 🔍 How It Works

### File Detection
- **Real-time monitoring** using Python watchdog
- **Multiple event types**: file creation, moves, modifications
- **Smart filtering**: Only processes supported file types
- **Debouncing**: Waits for files to finish being written

### Processing Pipeline
1. **File Validation**: Checks extension, size, and accessibility
2. **AI Classification**: Uses your existing QueryMind logic
3. **Resume Detection**: Identifies CVs vs other documents
4. **Integration**: Sends CVs to resume parser API
5. **Logging**: Tracks all activities and statistics

### Supported File Types
- **PDF** (with OCR fallback)
- **Microsoft Word** (.doc, .docx)
- **Rich Text Format** (.rtf)

## 📊 Real-time Output

When running, you'll see:

```
🎯 QueryMind Automatic Resume Detection Service
==================================================
👀 Watching folder: \\server\MSL-DATA\PROJECTS\INCOMING

📄 New file detected (created): John_Smith_CV.pdf
🔍 Analyzing: John_Smith_CV.pdf
✅ CV detected: John_Smith_CV.pdf
🎯 CV sent to resume parser successfully

📊 Live Statistics:
   📄 Files detected: 5
   📄 CVs found: 3
   🎯 CVs sent to parser: 3
   📈 Success rate: 100.0%
```

## 🛠️ Server Deployment

### Option 1: Run as Service (Windows)
```batch
# Create a batch file: start_watcher.bat
@echo off
cd "D:\Office work\Resume Parser\openai+gemini+unstructured+querymind\QueryMind"
python file_watcher.py
pause
```

### Option 2: Task Scheduler
1. Create task in Windows Task Scheduler
2. Set to run at startup
3. Command: `python file_watcher.py`
4. Working directory: Your QueryMind folder

### Option 3: Background Process
```bash
# Run in background (Linux/Unix)
nohup python file_watcher.py > watcher.log 2>&1 &
```

## 🔧 Advanced Configuration

### Processing Settings
```python
PROCESS_INTERVAL = 5  # seconds between processing batches
FILE_SIZE_THRESHOLD = 1024  # minimum file size in bytes
```

### Integration Settings
```python
INTEGRATION_ENABLED = True
RESUME_PARSER_URL = "http://localhost:8000"
RESUME_PARSER_ENDPOINT = "/api/resumes/upload/"
```

## 📈 Monitoring and Logs

### Real-time Statistics
- Files detected and processed
- CVs found vs non-CVs
- Integration success rate
- Error tracking

### Log Files
- **Console output**: Real-time processing status
- **processed_files.json**: Maintains list of processed files
- **Resume_Classification.xlsx**: Updated with new classifications

## 🎯 Benefits

### Automation
- **Zero manual intervention** required
- **Instant processing** of new files
- **Continuous monitoring** 24/7

### Reliability
- **Error handling**: Continues processing even if individual files fail
- **File validation**: Skips invalid or temporary files
- **Resume on restart**: Remembers processed files

### Integration
- **Seamless workflow**: CVs automatically flow to resume parser
- **Real-time feedback**: Know immediately when CVs are detected
- **Statistics tracking**: Monitor system performance

## 🛡️ Error Handling

### Common Scenarios
- **File in use**: Waits and retries
- **Network issues**: Continues monitoring, logs errors
- **API failures**: Continues processing other files
- **Invalid files**: Skips and continues

### Recovery
- **State persistence**: Remembers processed files across restarts
- **Graceful degradation**: System continues even with component failures
- **Error logging**: Comprehensive error reporting

## 🔄 Testing

### Manual Testing
1. Start the file watcher
2. Copy a resume file to the watched folder
3. Observe real-time processing
4. Check resume parser for received file

### Automated Testing
```bash
python test_watcher.py
```
- Copies test files automatically
- Demonstrates real-time detection
- Shows complete workflow

## 💡 Tips

### Performance
- **Monitor resource usage** during peak times
- **Adjust PROCESS_INTERVAL** based on file volume
- **Use SSD storage** for watched folders when possible

### Troubleshooting
- **Check folder permissions** if files aren't detected
- **Verify network connectivity** for server folders
- **Monitor API quotas** for OpenAI usage
- **Check resume parser status** if integration fails

### Best Practices
- **Test with small batches** before production deployment
- **Monitor disk space** in watched folders
- **Set up log rotation** for long-term running
- **Create backup procedures** for processed file logs

## 🎉 Your Automatic Resume Processing Pipeline is Ready!

The file watcher creates a complete automated workflow:
**New File** → **Auto-Detection** → **AI Classification** → **Resume Parser Integration** → **Database Storage**

Perfect for your office environment where new files arrive continuously! 🚀
