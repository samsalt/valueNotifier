#!/bin/bash

# Activate virtual environment
if [ -f ~/pweb/bin/activate ]; then
    source ~/pweb/bin/activate
elif [ -f ~/codeRepo/pweb/Scripts/activate ]; then
    source ~/codeRepo/pweb/Scripts/activate
else
    echo "Error: Virtual environment not found in ~/pweb"
    exit 1
fi

echo "Using Virtual environment pweb"

# Verify manage.py exists
if [ ! -f "manage.py" ]; then
    echo "Error: Run this script from your Django project root directory!"
    exit 1
fi

echo "Installing python packages..."
pip install requests django djangorestframework psycopg2

# Run migrations
echo "Creating and applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create admin user
echo "Checking admin user 'syadmin'..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='syadmin').exists():
    User.objects.create_superuser('syadmin', 'admin@gmail.com', '123')
    print('Admin user created')
else:
    print('Admin user already exists')
EOF

# Create normal user
echo "Checking normal user 'user1'..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='user1').exists():
    User.objects.create_user('user1', password='123')
    print('User1 created')
else:
    print('User1 already exists')
EOF

echo "Setup complete!"