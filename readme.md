# Django Blog Application

### Preview of Website 

#### http://beablogger.pythonanywhere.com/
## for installing follow below steps
1. create virtual environment
```bash
virtualenv env
```
2. install all required packages using below command
```bash
pip install -r requirements.txt
```

4. run this command for making migrations
```bash
python manage.py makemigrations
```
5. run migrate command for store database changes

```bash
python manage.py migrate
```
6. run this command to start the server
```bash
python manage.py runserver
```

## for creating admin user

```bash
python manage.py createsuperuser
```
