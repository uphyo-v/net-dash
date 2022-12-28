"# net-dash" 

Steps:
- Create Virtual Env (optional)
- Activate Virtual Env (optional)
- Install dependencies
	- pip install -r requirements.txt
- Create superuser
	- python manage.py createsuperuser
- Migrate database
	- python manage.py migrate
- Enable the application
	- python manage.py runserver
