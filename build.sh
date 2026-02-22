#!/bin/bash

echo "Creating Virtual Environment..."
# Create a virtual environment specifically for the build phase
python3.9 -m venv venv
source venv/bin/activate

echo "Installing requirements..."
# Install the dependencies inside this isolated environment
pip install -r requirements.txt

echo "Running database migrations..."
# Bypass the office firewall and create your Supabase tables
python manage.py migrate --noinput

echo "Collecting static files..."
# Create the static files Vercel is looking for
python manage.py collectstatic --noinput --clear

echo "Build Completed!"