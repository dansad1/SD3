#!/bin/sh

set -e

echo "Waiting for database and applying migrations..."

python manage.py migrate --noinput

echo "Checking whether the system is initialized..."

if ! python manage.py shell -c "
from backend.project.users.models import UserRole

raise SystemExit(
    0 if UserRole.objects.filter(code='admin').exists() else 1
)
"; then
    echo "System is empty. Running setup_system..."
    python manage.py setup_system
else
    echo "System is already initialized. Setup skipped."
fi

echo "Checking administrator..."

python manage.py create_admin

exec "$@"