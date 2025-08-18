# Docker Deployment Quick Setup Guide

## 🚀 Quick Start for Office Server

### Prerequisites
1. **Install Docker Desktop** on your Windows server
2. **Get your API keys** (OpenAI or Gemini)
3. **Note your server IP address**

### Step-by-Step Deployment

#### 1. Open Command Prompt as Administrator
```cmd
cd "d:\Office work\Resume Parser\previous+dt search"
```

#### 2. Run the deployment script
```cmd
deploy-office.bat
```

#### 3. Update configuration
- The script will create `.env` file
- Edit `.env` and add your API keys:
```env
OPENAI_API_KEY=your-openai-key-here
GEMINI_API_KEY=your-gemini-key-here
```

#### 4. Restart if needed
```cmd
docker-compose restart
```

### 📱 Access URLs
After deployment, your team can access:
- **Main Application**: `http://YOUR_SERVER_IP`
- **Admin Panel**: `http://YOUR_SERVER_IP/admin`
- **API Documentation**: `http://YOUR_SERVER_IP/docs`

### 🔧 Management Commands
```cmd
# Start services
manage-resume-parser.bat

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Update application
docker-compose pull && docker-compose up -d
```

### 🏥 Health Monitoring
- **Health Check**: `http://YOUR_SERVER_IP/health`
- **Service Status**: `docker-compose ps`

### 🔒 Security Notes
- Change default passwords in `.env`
- Use strong SECRET_KEY for production
- Consider firewall rules for office network

### 🚨 Troubleshooting
- **Port conflicts**: Stop other services on ports 80, 5432, 9200
- **Memory issues**: Increase Docker Desktop memory limit
- **API errors**: Check your API keys in `.env`

### 📞 Common Issues
1. **Docker not found**: Install Docker Desktop
2. **Permission denied**: Run as Administrator
3. **Port 80 busy**: Stop IIS or change port in docker-compose.yml
4. **Database errors**: Check PostgreSQL logs: `docker-compose logs postgres`

## 🎯 Production Checklist
- [ ] Docker installed and running
- [ ] API keys configured
- [ ] Server IP accessible from office network
- [ ] Firewall rules configured
- [ ] Backup strategy planned
- [ ] Team URLs shared
