Commands to run project:-

1. create virtual env :-
    1) python3 -m venv rbac_env
    2) source rbac_env/bin/activate # Linux
    3) rbac_env\Scripts\activate
2. install requirements :-
    1) pip install -r requirements.txt
3. Initiate data in tables
    1) python manage.py create_roles
    2) python manage.py makemigrations
    3)  python manage.py migrate  
4. run project
    1) python manage.py runserver 
5. postman collection :-
    1) `rbac postman.postman_collection.json` file in repository

Contact :- rohitjadhav440@gmail.com
Phone no :- +91 9922979035
    