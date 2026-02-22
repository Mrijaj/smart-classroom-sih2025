#!/bin/bash

echo "Creating Virtual Environment..."
# Create a virtual environment named 'venv' specifically for the build phase
python3.9 -m venv venv

# Activate the virtual environment
source venv/bin/activate

echo "Installing requirements..."
# Install all dependencies directly into this isolated environment
pip install -r requirements.txt

echo "Running database migrations..."
# Run migrations from the cloud to bypass your HPE office firewall restrictions
python manage.py migrate --noinput

echo "Collecting static files..."
# Collect static files using the isolated Python interpreter
python manage.py collectstatic --noinput --clear

echo "Build Completed!"