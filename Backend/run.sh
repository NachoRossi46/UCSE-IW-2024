# exit on error
set -o errexit

gunicorn proyectoPrincipal.wsgi:application