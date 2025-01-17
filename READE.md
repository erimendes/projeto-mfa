meu_projeto/
    manage.py
    meu_projeto/
        __init__.py
        settings.py
        urls.py
        wsgi.py
        asgi.py
    minha_aplicacao/
        __init__.py
        admin.py
        apps.py
        models.py
        views.py
        urls.py
        migrations/
        templates/
        static/

python manage.py makemigrations minha_aplicacao

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

pip freeze > requirements.txt

python manage.py shell

.tables

SELECT * FROM minha_aplicacao_userprofile;

SELECT * FROM auth_user WHERE id = 1;


