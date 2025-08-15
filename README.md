venv\Scripts\activate

pip freeze > requirements.txt

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

django-admin startproject config .

python manage.py startapp

python manage.py createsuperuser

python manage.py runserver