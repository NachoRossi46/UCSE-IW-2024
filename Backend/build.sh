# exit on error
set -o errexit

pip install -r requirements.txt

# cd $(dirname $(find . | grep manage.py$))
python manage.py collectstatic --no-input
python manage.py migrate
python initialize_db.py
echo "from django.contrib.auth import get_user_model; User = get_user_model(); Rol = User.rol.field.remote_field.model; admin_rol = Rol.objects.get(rol='Administrador'); User.objects.create_superuser(email='nachorossi121@gmail.com', nombre='Admin', apellido='User', password='12345678', rol=admin_rol) if not User.objects.filter(email='nachorossi121@gmail.com').exists() else None" | python manage.py shell
mkdir -p /opt/render/project/src/whoosh_index
python manage.py rebuild_index --noinput
# python manage.py createsuperuser --username admin --email "nachorossi121@gmail.com" --noinput || true