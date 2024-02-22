CREATE DATABASE feedbot_dev;
CREATE USER feedbot_user WITH PASSWORD '111';
\c feedbot_dev
GRANT ALL PRIVILEGES ON DATABASE feedbot_dev TO feedbot_user;
GRANT ALL ON SCHEMA public TO feedbot_user;
