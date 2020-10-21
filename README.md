# BPMANV-DjangoPrototype

###Properly installing the project

After cloning the project, run 
```shell
pip install -r requirements.txt
```
then 
```shell
cd backend  
python manage.py createsuperuser
python manage.py makemigrations  
python manage.py migrate
python manage.py runserver
```

you can find the admin view by adding admin/ to the given URL
