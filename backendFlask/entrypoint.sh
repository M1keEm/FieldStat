#!/bin/bash
set -e

# Wait for postgres to be ready
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.5
done
echo "PostgreSQL started"

# Initialize/migrate database if needed
echo "Initializing database..."
flask db init 2>/dev/null || echo "Database already initialized"
flask db migrate -m "Auto migration" 2>/dev/null || echo "No changes in schema detected"
flask db upgrade

# Start the Flask application
echo "Starting Flask application..."
exec flask run
