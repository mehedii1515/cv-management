# Resume Parser - Office Network Access Guide

## 🏢 **For Office Users**

### **Main Application URL:**
```
http://192.168.1.2:8080
```

**📋 Instructions for Office Employees:**

1. **Open your web browser** (Chrome, Firefox, Edge)
2. **Type this address:** `http://192.168.1.2:8080`
3. **Press Enter** - You should see the Resume Parser application

---

## 🖥️ **For IT Administrator (Server Setup)**

### **Server Requirements:**
- **Server IP:** 192.168.1.2 (configured)
- **Required Ports:** 8000, 3000, 8080
- **Operating System:** Windows

### **Windows Firewall Configuration:**

**Method 1: Windows Defender Firewall (GUI)**
1. Open **Windows Defender Firewall with Advanced Security**
2. Click **Inbound Rules** → **New Rule**
3. Select **Port** → **TCP** → **Specific Local Ports**
4. Enter: `8000,3000,8080`
5. Select **Allow the connection**
6. Apply to **Domain, Private, Public** (or as per office policy)
7. Name: "Resume Parser Application"

**Method 2: Command Line (Run as Administrator)**
```cmd
netsh advfirewall firewall add rule name="Resume Parser - Django" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="Resume Parser - Frontend" dir=in action=allow protocol=TCP localport=3000
netsh advfirewall firewall add rule name="Resume Parser - Caddy" dir=in action=allow protocol=TCP localport=8080
```

### **Starting the Production Server:**
1. **Navigate to project directory**
2. **Right-click** `start_production.bat`
3. **Select:** "Run as Administrator"
4. **Wait** for all servers to start (Django, Next.js, Caddy)

---

## 🔧 **Troubleshooting**

### **If Users Can't Access the Application:**

**1. Check Server Status:**
- Verify all three services are running:
  - Django (port 8000)
  - Next.js (port 3000)
  - Caddy (port 8080)

**2. Test Network Connectivity:**
```cmd
# From office computer, test connectivity:
ping 192.168.1.2
telnet 192.168.1.2 8080
```

**3. Check Firewall:**
- Ensure Windows Firewall allows the required ports
- Check office network firewall/router settings

**4. Verify Server IP:**
```cmd
# On server, confirm IP address:
ipconfig
```

### **Common Issues:**

**❌ "This site can't be reached"**
- Check if server is running
- Verify firewall settings
- Confirm IP address is correct

**❌ "Connection refused"**  
- Server services may not be running
- Wrong port number
- Firewall blocking connection

**❌ Slow performance**
- Multiple users accessing simultaneously (normal)
- Check server resources (CPU, RAM)
- Consider upgrading server hardware for heavy usage

---

## 📊 **Office Usage Guidelines**

### **For Best Performance:**
- **Recommended:** Up to 20 concurrent users
- **File Upload Limit:** 50MB per file
- **Supported Formats:** PDF, DOCX, DOC, TXT

### **Network Requirements:**
- **Minimum:** 100 Mbps local network
- **Recommended:** 1 Gbps for better file transfer speeds

### **Browser Compatibility:**
- ✅ **Chrome** (Recommended)
- ✅ **Firefox**  
- ✅ **Microsoft Edge**
- ⚠️ **Internet Explorer** (Not recommended)

---

## 📞 **Support**

### **For Users:**
1. Try refreshing the page
2. Clear browser cache
3. Try a different browser
4. Contact IT administrator

### **For IT Administrator:**
1. Check server logs in `logs/` directory
2. Monitor server resources
3. Restart services if needed: `stop_production.bat` then `start_production.bat`

---

## 🚀 **Access Summary**

| Service | Local Access | Network Access | Purpose |
|---------|-------------|----------------|---------|
| **Main App** | http://localhost:8080 | **http://192.168.1.2:8080** | **Use This** |
| Frontend | http://localhost:3000 | http://192.168.1.2:3000 | Development |
| Backend | http://localhost:8000 | http://192.168.1.2:8000 | API Only |

**🎯 Office users should use: `http://192.168.1.2:8080`**
