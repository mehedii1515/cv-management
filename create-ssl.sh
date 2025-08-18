#!/bin/bash

# Create SSL certificates for HTTPS (optional for office use)
mkdir -p ssl/certs ssl/private

echo "Creating self-signed SSL certificate for office use..."

# Generate private key
openssl genrsa -out ssl/private/server.key 2048

# Generate certificate signing request
openssl req -new -key ssl/private/server.key -out ssl/server.csr -subj "/C=BD/ST=Dhaka/L=Dhaka/O=Office/OU=IT/CN=ResumeParser"

# Generate self-signed certificate
openssl x509 -req -days 365 -in ssl/server.csr -signkey ssl/private/server.key -out ssl/certs/server.crt

# Clean up
rm ssl/server.csr

echo "SSL certificates created successfully!"
echo "Certificate: ssl/certs/server.crt"
echo "Private Key: ssl/private/server.key"
