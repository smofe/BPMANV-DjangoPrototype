# BPMANV-DjangoPrototype

### Properly installing the project

After cloning the project, run 
```shell
pip install -r requirements.txt
```
then 
```shell
cd backend  
python manage.py makemigrations  
python manage.py migrate
python manage.py createsuperuser
```
we usually use "admin" as id and "password123" as password   
there is no need to add an email adress (just press enter)  
then
```shell
python manage.py runserver
```

you can find the admin view by adding admin/ to the given URL
