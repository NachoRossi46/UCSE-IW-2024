# exit on error
set -o errexit

pip install -r requirements.txt

# cd $(dirname $(find . | grep manage.py$))
python manage.py collectstatic --no-input
python manage.py migrate
python initialize_db.py
echo "from django.contrib.auth import get_user_model; User = get_user_model(); Rol = User.rol.field.remote_field.model; admin_rol = Rol.objects.get(rol='Administrador'); User.objects.create_superuser('admin', 'nachorossi121@gmail.com', '12345678', nombre='Admin', apellido='User', rol=admin_rol) if not User.objects.filter(email='nachorossi121@gmail.com').exists() else None" | python manage.py shell

# python manage.py createsuperuser --username admin --email "nachorossi121@gmail.com" --noinput || true