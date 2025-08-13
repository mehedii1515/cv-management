# PostgreSQL Setup Guide for Resume Parser

This guide will help you install and configure PostgreSQL for the Resume Parser project.

## 🐧 Linux (Ubuntu/Debian)

### Installation
```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Database Setup
```bash
# Switch to postgres user
sudo -u postgres psql

# Or use the provided script
sudo -u postgres psql -f setup_database.sql
```

## 🪟 Windows

### Installation
1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run the installer and follow the setup wizard
3. Choose a password for the postgres user
4. Default port is 5432 (keep it unless you need to change it)

### Database Setup
```cmd
# Open Command Prompt as Administrator
# Navigate to PostgreSQL bin directory (usually C:\Program Files\PostgreSQL\15\bin)
cd "C:\Program Files\PostgreSQL\15\bin"

# Connect to PostgreSQL
psql -U postgres

# Or use the provided script
psql -U postgres -f setup_database.sql
```

## 🍎 macOS

### Installation (using Homebrew)
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install PostgreSQL
brew install postgresql

# Start PostgreSQL service
brew services start postgresql

# Create a database user
createdb $(whoami)
```

### Database Setup
```bash
# Connect to PostgreSQL
psql postgres

# Or use the provided script
psql postgres -f setup_database.sql
```

## 🛠️ Manual Database Setup

If you prefer to set up the database manually:

```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database
CREATE DATABASE resume_parser;

-- Create user
CREATE USER resume_parser_user WITH PASSWORD 'secure_password_change_me';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE resume_parser TO resume_parser_user;
ALTER USER resume_parser_user CREATEDB;

-- Connect to the database
\c resume_parser;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO resume_parser_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO resume_parser_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO resume_parser_user;

-- Set default privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO resume_parser_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO resume_parser_user;

-- Exit
\q
```

## 🔧 Configuration

### Environment Variables
Update your `.env` file with the database credentials:

```env
# PostgreSQL Database Configuration
DB_NAME=resume_parser
DB_USER=resume_parser_user
DB_PASSWORD=secure_password_change_me
DB_HOST=localhost
DB_PORT=5432
```

### Connection Testing
Test your database connection:

```bash
# Test connection
psql -h localhost -U resume_parser_user -d resume_parser

# If successful, you should see:
# resume_parser=>
```

## 🚀 Running Migrations

After setting up PostgreSQL, run Django migrations:

```bash
cd backend
python manage.py migrate
```

## 🔒 Security Best Practices

1. **Change default passwords**: Never use default passwords in production
2. **Use environment variables**: Store sensitive data in `.env` files
3. **Enable SSL**: Configure SSL for production databases
4. **Regular backups**: Set up automated backups
5. **User privileges**: Create specific users with minimal required privileges

## 📊 Database Administration

### Useful Commands

```bash
# List all databases
\l

# Connect to a database
\c database_name

# List all tables
\dt

# Describe a table
\d table_name

# Show current connections
SELECT * FROM pg_stat_activity;

# Backup database
pg_dump -h localhost -U resume_parser_user resume_parser > backup.sql

# Restore database
psql -h localhost -U resume_parser_user resume_parser < backup.sql
```

## 🐛 Troubleshooting

### Common Issues

1. **Connection refused**: Check if PostgreSQL is running
   ```bash
   sudo systemctl status postgresql  # Linux
   brew services list | grep postgresql  # macOS
   ```

2. **Authentication failed**: Verify username and password
   ```bash
   psql -h localhost -U resume_parser_user -d resume_parser
   ```

3. **Database doesn't exist**: Create the database first
   ```bash
   createdb -h localhost -U postgres resume_parser
   ```

4. **Permission denied**: Check user privileges
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE resume_parser TO resume_parser_user;
   ```

## 🔗 Useful Resources

- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [Django PostgreSQL Documentation](https://docs.djangoproject.com/en/4.2/ref/databases/#postgresql-notes)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

## 🆘 Support

If you encounter issues:
1. Check the PostgreSQL logs
2. Verify your `.env` configuration
3. Ensure PostgreSQL is running
4. Test the database connection separately
5. Check Django's database settings in `settings.py` 