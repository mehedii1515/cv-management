# Quick Setup Guide for Production Deployment

## File Organization (Correct Setup)

```
your-project/                          (Root directory)
├── Caddyfile                         (Web server config)
├── production_server.py              (Production startup script)
├── start_production.bat              (Windows startup script)
├── stop_production.bat               (Windows stop script)
├── PRODUCTION_DEPLOYMENT_GUIDE.md    (Full documentation)
├── logs/                             (Will be created automatically)
└── backend/                          (Django project)
    ├── venv/                         (Your virtual environment)
    ├── media/                        (Your media files - uploads, etc.)
    ├── staticfiles/                  (Collected static files)
    ├── production_requirements.txt   (Production packages)
    ├── production_settings.py        (Production Django settings)
    ├── manage.py                     (Django management)
    ├── requirements.txt              (Your existing requirements)
    └── resume_parser/                (Django project settings)
```

## Installation Steps

### 1. Install Production Dependencies
```bash
# Navigate to backend directory
cd backend

# Activate your virtual environment
venv\Scripts\activate

# Install production requirements
pip install -r production_requirements.txt
```

### 2. Download Caddy (Web Server)
- Download from: https://caddyserver.com/download
- Place `caddy.exe` in your **root project directory** (not in backend)

### 3. Start Production Servers
```bash
# Go back to root directory
cd ..

# Run the startup script (as Administrator for best performance)
start_production.bat
```

## Access Your Application
- **Office Users**: http://localhost:8080 (through Caddy)
- **Your Server IP**: http://[YOUR-SERVER-IP]:8080 (for network access)
- **Direct Django**: http://localhost:8000

## What Each File Does

- **Caddyfile**: Web server that handles requests, compression, security
- **production_server.py**: Runs Django with Waitress (production WSGI server)
- **start_production.bat**: Activates venv and starts both servers
- **backend/production_requirements.txt**: Only the extra packages needed for production
- **backend/production_settings.py**: Optimized Django settings for office use

## Troubleshooting

If you get import errors:
1. Make sure you're in the backend directory when installing requirements
2. Make sure venv is activated before installing
3. Check that waitress installed properly: `pip list | grep waitress`

The setup is now properly organized for your backend venv structure!
