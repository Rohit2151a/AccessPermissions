Commands to run project:-

1. create virtual env :-
    1) python3 -m venv rbac_env
    2) source rbac_env/bin/activate # Linux
    3) rbac_env\Scripts\activate
2. install requirements :-
    1) pip install -r requirements.txt
3. Update settings.py for database details update
4. create superuser and Initiate data in tables
    1) python manage.py createsuperuser
    Note : Please create superuser with username: "admin" and password: 123
         This will help in running API in postman collection easily
    2) python manage.py makemigrations
    3)  python manage.py migrate
    4) python manage.py create_roles
5. run project
    1) python manage.py runserver 
6. postman collection :-
    1) `rbac postman.postman_collection.json` file in repository you can import it.
    2) Use "Auth Token" API first and use the Token got in reponse for each API before using
    3) I have hosted API at URL :- https://rohitjadhav440.pythonanywhere.com you can update url in postman from localhost to this URL
      Note: we have used musql in hosted API for free plan issues

Contact :- rohitjadhav440@gmail.com
Phone no :- +91 9922979035
    