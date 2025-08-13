-- PostgreSQL Database Setup Script for Resume Parser
-- Run this script as the PostgreSQL superuser (usually postgres)

-- Create database
CREATE DATABASE resume_parser;

-- Create user with password
CREATE USER resume_parser_user WITH PASSWORD 'secure_password_change_me';

-- Grant all privileges on database to user
GRANT ALL PRIVILEGES ON DATABASE resume_parser TO resume_parser_user;

-- Grant additional privileges for Django migrations
ALTER USER resume_parser_user CREATEDB;

-- Connect to the database
\c resume_parser;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO resume_parser_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO resume_parser_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO resume_parser_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO resume_parser_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO resume_parser_user;

-- Show confirmation
SELECT 'Database setup complete!' as status; 