#!/bin/bash
# Force the script to fail immediately if ANY command crashes
set -e

echo "Creating Virtual Environment..."
python3.9 -m venv venv
source venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Preparing static directories..."
# Ensure the folders exist physically. Git sometimes ignores folders, which crashes Django.
mkdir -p static
mkdir -p staticfiles

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build Completed Successfully!"