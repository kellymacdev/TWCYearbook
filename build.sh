#!/usr/bin/env bash
set -o errexit  # stop if any command fails

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run migrations
echo "Applying migrations..."
python manage.py migrate

# Import the CSV data
echo "Importing csv data"
python manage.py import_google_sheet

echo "Build complete!"