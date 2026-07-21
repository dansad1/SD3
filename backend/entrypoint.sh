#!/bin/sh

set -e

echo "Waiting for database and applying migrations..."

python manage.py migrate --noinput

echo "Checking whether the system is initialized..."

if ! python manage.py shell -c "
from backend.project.users.models import User

raise SystemExit(
    0 if User.objects.exists() else 1
)
"; then
    echo "Database is empty. Running setup_system..."
    python manage.py setup_system
else
    echo "Database already contains users. Setup skipped."
fi

exec "$@"