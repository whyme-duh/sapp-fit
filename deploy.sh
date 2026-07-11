#! /bin/bash

echo "Starting deployment process..."

WSGI_FILE="/var/www/sappfit_pythonanywhere_com_wsgi.py"

echo "Navigating to the project directory..."
cd sapp-fit

echo "Pulling latest changes from the repository..."
git pull origin master

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --no-input
ch
echo "Reloading the application server..."
touch $WSGI_FILE

echo "Deployment process completed successfully!"
