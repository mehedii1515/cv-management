# QueryMind

# QueryMind Resume Parser Integration

## Simple Integration Setup

Your existing QueryMind system has been enhanced with simple integration capabilities to automatically send detected CVs to your resume parser.

### 📋 What's Been Added

1. **Integration Toggle**: `INTEGRATION_ENABLED` setting in `main.py`
2. **Automatic CV Sending**: Detected CVs are automatically sent to your resume parser
3. **Integration Statistics**: Track how many CVs were sent successfully
4. **Error Handling**: Graceful handling of connection issues

### 🚀 Quick Start

1. **Start your resume parser backend**:
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Enable integration**:
   ```bash
   python integration_manager.py --enable
   ```

3. **Run QueryMind**:
   ```bash
   python main.py
   ```

### 🔧 Configuration

Edit the settings in `main.py`:

```python
# Resume Parser Integration Settings
RESUME_PARSER_URL = "http://localhost:8000"  # Your Django backend URL
RESUME_PARSER_ENDPOINT = "/api/upload-resume/"  # Your upload endpoint
INTEGRATION_ENABLED = True  # Set to True to enable integration
```

### 📊 Usage Options

#### Option 1: Enable Integration
```bash
python integration_manager.py --enable
python main.py
```

#### Option 2: Disable Integration (Testing Mode)
```bash
python integration_manager.py --disable
python main.py
```

#### Option 3: Interactive Manager
```bash
python integration_manager.py
```

### 🎯 How It Works

1. **QueryMind runs normally** - processes files and detects CVs
2. **For each detected CV** - automatically sends it to your resume parser API
3. **Integration statistics** - shows how many CVs were sent successfully
4. **Error handling** - continues processing even if the resume parser is down

### 📈 Integration Output

When running with integration enabled, you'll see:

```
Batch Progress: 5/10 files processed.
✅ CV sent to resume parser: John_Smith_CV.pdf
⚠️ Resume parser API error for Jane_Doe_Resume.doc: 500

📊 Integration Statistics:
CVs found: 3
CVs sent to resume parser: 2
Integration success rate: 66.7%

🔗 Integration with resume parser is ENABLED
```

### 🛠️ Troubleshooting

1. **"Resume parser API error"**
   - Make sure your Django backend is running on port 8000
   - Check that the API endpoint `/api/upload-resume/` exists

2. **"Integration disabled"**
   - Run `python integration_manager.py --enable` to enable it

3. **Connection timeout**
   - The system will continue processing files even if the resume parser is down
   - Check your Django backend logs for any errors

### 🔗 Resume Parser API Format

The integration sends files to your resume parser with this format:

```python
files = {'resume': (filename, file_content)}
data = {
    'source': 'QueryMind_AutoDetect',
    'auto_detected': True,
    'timestamp': '2025-08-03T10:30:00'
}
```

Make sure your Django backend can handle this format in your upload endpoint.

### 🎛️ Server Deployment

For your office server setup:

1. **Configure server folders** in `main.py`:
   ```python
   SOURCE_FOLDER = r"\server\MSL-DATA\PROJECTS\INCOMING"
   ```

2. **Run as scheduled task** (Windows Task Scheduler):
   - Run `python main.py` every 30 minutes
   - Set working directory to your QueryMind folder

3. **Monitor logs**:
   - Check console output for integration statistics
   - Monitor `Resume_Classification.xlsx` for results

### 🎯 Integration Benefits

- **Automated Workflow**: CVs are automatically sent to your resume parser
- **No Manual Intervention**: Process runs completely automatically
- **Error Resilience**: Continues working even if resume parser is down
- **Statistics Tracking**: Know exactly how many CVs were processed and sent
- **Easy Toggle**: Can enable/disable integration anytime

Your existing QueryMind workflow remains exactly the same, with the added benefit of automatic integration with your resume parser system!