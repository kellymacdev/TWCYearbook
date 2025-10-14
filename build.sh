#!/usr/bin/env bash
set -o errexit  # stop if any command fails

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Import the CSV data
python manage.py import_google_sheet
