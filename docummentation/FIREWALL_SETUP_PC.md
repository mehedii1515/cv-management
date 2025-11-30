# Windows Firewall Configuration for Your PC (192.168.1.152)

## To enable network access to your PC, run these commands as Administrator:

# Open Command Prompt as Administrator and run:

netsh advfirewall firewall add rule name="Resume Parser - Django (PC)" dir=in action=allow protocol=TCP localport=8000 remoteip=192.168.1.0/24

netsh advfirewall firewall add rule name="Resume Parser - Frontend (PC)" dir=in action=allow protocol=TCP localport=3000 remoteip=192.168.1.0/24

netsh advfirewall firewall add rule name="Resume Parser - Caddy (PC)" dir=in action=allow protocol=TCP localport=8080 remoteip=192.168.1.0/24

# Alternative: Allow from any IP on the network (less secure)
# netsh advfirewall firewall add rule name="Resume Parser - Django (PC)" dir=in action=allow protocol=TCP localport=8000
# netsh advfirewall firewall add rule name="Resume Parser - Frontend (PC)" dir=in action=allow protocol=TCP localport=3000
# netsh advfirewall firewall add rule name="Resume Parser - Caddy (PC)" dir=in action=allow protocol=TCP localport=8080

## To remove these rules later:
# netsh advfirewall firewall delete rule name="Resume Parser - Django (PC)"
# netsh advfirewall firewall delete rule name="Resume Parser - Frontend (PC)"
# netsh advfirewall firewall delete rule name="Resume Parser - Caddy (PC)"

## Testing access:
# From another computer on the network:
# ping 192.168.1.152
# Open browser: http://192.168.1.152:8080
