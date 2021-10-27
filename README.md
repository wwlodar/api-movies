# api-movies [![wwlodar](https://circleci.com/gh/wwlodar/api-movies.svg?style=shield)](https://app.circleci.com/pipelines/github/wwlodar/api-movies?branch=main)
 API built with Django Rest Framework

### Demo
Here is a working live demo: https://pacific-refuge-57547.herokuapp.com/

### Technology
Python 3.9.7. 
djangorestframework 3.12.4

### Integartion 
In order to work correctly, application needs API Key from OMDB API.
You can obtain it here: 
http://www.omdbapi.com/apikey.aspx

### Installation

First clone the repository from Github and switch to the new directory:
```
$ git clone https://github.com/wwlodar/api-movies.git
$ cd api-movies
```
Activate the virtualenv for your project.

Install project dependencies:
```
$ pip install -r requirements.txt
```
Apply migrations: 
```
$ python manage.py migrate
```
You can now run the development server:
```
$ python manage.py runserver
```
