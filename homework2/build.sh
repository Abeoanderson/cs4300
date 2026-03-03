#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt 

python manage.py collectstatic --no-input

python manage.py migrate
python manage.py loaddata sample_data
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'yourpassword123')"