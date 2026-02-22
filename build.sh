#!/bin/bash

# 1. Install dependencies
echo "Installing requirements..."
# Using python3.12 explicitly to match vercel.json configuration
python3.12 -m pip install -r requirements.txt

# 2. Run migrations
# This will create your tables in Supabase automatically during deployment
echo "Running database migrations..."
python3.12 manage.py migrate --noinput

# 3. Collect static files for the UI
echo "Collecting static files..."
python3.12 manage.py collectstatic --noinput

echo "Build Completed!"