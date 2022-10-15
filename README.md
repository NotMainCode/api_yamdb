# API of project "YaMDb".

## Description

The YaMDb project collects user feedback on creations (Title).
The creations are divided into categories: "Books", "Films", "Music", etc.
The list of categories can be expanded by the administrator.

In each category there is information about the creations.
The creations themselves are not stored in YaMDb;
you cannot watch a movie or listen to music here.

A creation can be assigned a genre from the preset list.
New genres can only be created by the administrator.

Users can leave text reviews for creations
and rate the creation in the range from one to ten (an integer);
from user ratings, an average rating of the creation is formed - rating (integer).
A user can leave only one review per creation.

###
Full API documentation is available at endpoint:
>redoc/

## Examples of requests

- user registration *(POST)*
>api/v1/auth/signup/ 
>```
>{
>    "username": "my_username",
>    "email": "my_email"
>}
>```

- getting access JWT-token *(POST)*
>api/v1/auth/token/ 
>```
>{
>    "username": "my_username",
>    "comfirmation_code": "my_ecomfirmation_code"
>}
>```

## Technology

Python 3.7

Django 2.2.16

Django REST framework 3.2.14

## For launch

Create and activate virtual environment
```
py -3.7 -m venv venv

source venv/Scripts/activate
```

Install dependencies from requirements.txt file
```
pip install -r requirements.txt
```

Perform migrations
```
py manage.py migrate
```

Load test data (if you need)
```
py manage.py load_test_data
```

Run project
```
py manage.py runserver 8008
```

## Authors

https://github.com/NotMainCode

https://github.com/Vas1l1y

https://github.com/SerMikh1981

###
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
