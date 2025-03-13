#!/bin/bash
set -e

# Wait for database to be available
until nc -z -v -w30 $DATABASE_HOST 3306; do
  echo "Waiting for database connection..."
  sleep 2
done

# Create database if it doesn't exist
echo "Creating database if it doesn't exist..."
python -c "
import MySQLdb
conn = MySQLdb.connect(
    host='$DATABASE_HOST',
    user='$DATABASE_USER',
    password='$DATABASE_PASSWORD'
)
cursor = conn.cursor()
try:
    cursor.execute('CREATE DATABASE IF NOT EXISTS $DATABASE_NAME')
    print('Database created or already exists')
except:
    print('Failed to create database')
conn.close()
"

# Run migrations
echo "Making migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

# Add any other startup commands here
# python manage.py collectstatic --noinput

# Start Django server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000