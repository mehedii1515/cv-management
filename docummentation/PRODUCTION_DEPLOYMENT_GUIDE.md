# Resume Parser - Windows Production Deployment Guide
# Waitress + Caddy Setup for Office Environment

## Overview

This setup provides a production-ready deployment for your Resume Parser application optimized for a Windows office environment with multiple users. The configuration uses:

- **Waitress**: Production WSGI server optimized for Windows
- **Caddy**: Reverse proxy with automatic compression and security headers
- **Optimized Django settings**: For multi-user office environment

## Prerequisites

### 1. Install Python Dependencies
```bash
pip install -r production_requirements.txt
```

### 2. Install Caddy (Web Server)
1. Download Caddy for Windows from: https://caddyserver.com/download
2. Extract `caddy.exe` to your project directory, or
3. Add Caddy to your system PATH for global access

## Deployment Steps

### Step 1: Prepare the Environment
```bash
# Create necessary directories
mkdir logs
mkdir backend\media\uploads
mkdir backend\staticfiles

# Collect static files
cd backend
python manage.py collectstatic --noinput
cd ..
```

### Step 2: Database Setup
```bash
# Run migrations
cd backend
python manage.py migrate
cd ..
```

### Step 3: Start Production Servers

#### Option A: Automated Start (Recommended)
```bash
# Run as Administrator for best performance
start_production.bat
```

#### Option B: Manual Start
```bash
# Terminal 1: Start Django with Waitress
python production_server.py

# Terminal 2: Start Caddy (in separate terminal)
caddy run --config Caddyfile
```

## Access Information

### For Office Users:
- **Main Application**: http://localhost:8080 (through Caddy)
- **Network Access**: http://[SERVER-IP]:8080

### For Direct Access:
- **Django Server**: http://localhost:8000 (direct to Django)

## Performance Optimizations

### Database Optimizations (SQLite)
- Write-Ahead Logging (WAL) mode for better concurrency
- Increased cache size for faster queries
- Memory-mapped I/O for better performance

### Server Optimizations
- **16 threads** for handling multiple office users
- **1000 connection limit** for high concurrent usage
- **Gzip compression** for faster page loading
- **Static file caching** for improved performance

### For High Usage, Consider PostgreSQL:
1. Install PostgreSQL
2. Update `production_settings.py` to use PostgreSQL
3. Install: `pip install psycopg2-binary`

## Security Features

- **Security headers** (XSS protection, content type sniffing protection)
- **CORS handling** for API requests
- **Request size limits** for file uploads
- **Session management** optimized for office environment

## Monitoring & Logs

### Log Files:
- `logs/django_production.log` - Application logs
- `logs/django_errors.log` - Error logs only  
- `logs/caddy_access.log` - Web server access logs

### Monitor Performance:
- Check log files regularly
- Monitor system resources (RAM, CPU)
- Watch database file size growth

## Network Configuration

### For Office Network Access:
1. Find your server's IP address:
   ```cmd
   ipconfig
   ```

2. Update firewall rules to allow:
   - Port 8000 (Django)
   - Port 8080 (Caddy)

3. Add office IP addresses to `ALLOWED_HOSTS` in `production_settings.py`:
   ```python
   ALLOWED_HOSTS = [
       'localhost',
       '127.0.0.1',
       '192.168.1.100',  # Your server IP
       '10.0.0.50',      # Additional office IPs
   ]
   ```

## Stopping Servers

### Automated Stop:
```bash
stop_production.bat
```

### Manual Stop:
- Press `Ctrl+C` in Django terminal
- Press `Ctrl+C` in Caddy terminal

## Troubleshooting

### Common Issues:

1. **Port Already in Use**:
   - Change ports in `production_server.py` and `Caddyfile`
   - Check what's using the port: `netstat -ano | findstr :8000`

2. **Database Locked**:
   - Stop all servers completely
   - Check for zombie Python processes
   - Restart servers

3. **File Upload Issues**:
   - Check `backend/media/uploads` directory permissions
   - Verify `FILE_UPLOAD_MAX_MEMORY_SIZE` settings

4. **Performance Issues**:
   - Monitor `logs/django_production.log`
   - Consider upgrading to PostgreSQL for high usage
   - Increase server resources (RAM/CPU)

### Performance Tips:

1. **Run as Administrator** for better Windows performance
2. **Disable Windows Defender** real-time scanning for project directory (if security policy allows)
3. **Use SSD storage** for database and media files
4. **Close unnecessary applications** on the server machine

## Maintenance

### Regular Tasks:
- Monitor log file sizes (they auto-rotate)
- Backup database file (`backend/db.sqlite3`)
- Clear old uploaded files from `backend/media/uploads`
- Update dependencies periodically

### Backup Strategy:
```bash
# Backup database
copy backend\db.sqlite3 backups\db_backup_YYYYMMDD.sqlite3

# Backup uploaded files
xcopy backend\media\uploads backups\uploads_YYYYMMDD\ /E /I
```

## Scaling for More Users

If you have many office users (20+), consider:

1. **PostgreSQL Database**:
   - Better concurrent access
   - Improved performance under load
   
2. **Increase Server Resources**:
   - More RAM (8GB+ recommended)
   - Faster CPU
   - SSD storage

3. **Load Balancer** (for very high usage):
   - Multiple Django instances
   - Database connection pooling

## Support

For issues or optimizations:
1. Check log files first
2. Verify network connectivity
3. Test with single user first
4. Monitor system resources

The production setup is optimized for Windows office environments and should handle multiple concurrent users effectively.
