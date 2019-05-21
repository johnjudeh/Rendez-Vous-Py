# RendezVousPy

## Description

Rendez Vous is an application that helps connect people in big cities. By using
the locations of you and your friends, it can find a fair place to meet close to
the middle. The application also allows users to register and update their
preferences of types of places to meet up. Search results will then match the
logged in user's preferences where possible.

The application is just a hobby for now and should be fun to use. It might even
help you see those 'other-side-of-the-city' friends that you never get the
chance to :wink:

Demo: https://rendezvous-py.herokuapp.com

## Developer Guide

Interested in getting this project on your local machine and playing around
with it? Check out the instructions below!

### Prerequisites

To run the application locally, make sure that you have the following installed:
* [Python](https://www.python.org/) and pip for the backend
* [NodeJS](https://nodejs.org/en/) and npm for the frontend

### Installing

If you are planning to pull the project from the Github website, click the
**Clone or download** button above. Alternatively, if you would like to pull it
from the command line, make sure you have [Git](https://git-scm.com/) installed
and type in the following command in your terminal.

```bash
cd <chosen folder>
git clone https://github.com/johnjudeh/Rendez-Vous-Py.git
```

Once the files have been downloaded, navigate into the applications root
directory and install the python and node dependencies needed.

```bash
cd Rendez-Vous-Py
pip install -r requirements.txt
npm install
```

### Setting Environment Variables

In order to ensure the highest level of security for the deployed version of the
application, some environment variables have been set to hide API keys and other
sensitive information.

In order to run the application, the following environment variables must be set
locally. The following variables are needed:

1. **MAPS_KEY** - a free Google Maps Javascript API key must be generated on the
[Google API Console](https://console.developers.google.com/apis/). Make sure to
read the terms and conditions on how the key is allowed to be used if you plan
to develop further
1. **SECRET_KEY** - this is not required for running the application locally
but strongly recommended when deploying the application

### Setup PostgreSQL

Install [postgresql](https://postgresapp.com/) and type the following commands
into your terminal:

```bash
createdb rvdb
psql -c "create user <your-name> with password 'cookiemonster'"
psql -c "grant all on database rvdb to <your-name>"
psql -c "alter user <your-name> superuser"
```

Make sure you also update the `DATABASES` variable in 
`rendezvous/settings/base.py` to use `<your-name>` like below:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rvdb',
        'USER': '<your-name>',
        ...
    }
}
``` 

Once you have setup the database, make sure to allow Django to set it up the 
application's models:

```bash
python manage.py migrate
``` 

### Frontend Build Process

While not required for running the application locally, there is a Gulp build
process setup for deploying the application. This build process minifies static
assets, optimises images and transpiles JavaScript using babel. Assuming you
installed the node dependencies, you can run the build process using:

```bash
gulp
```

### Running

To run the application, make sure you are in the application's root directory
and type the following command into the terminal:

```bash
python manage.py runserver
```

You should then be able to access the application at 
[127.0.0.1:8000](http://127.0.0.1:8000/). Enjoy!



## Built With

* [Django](https://www.djangoproject.com/) - Backend framework used
* [PostgreSQL](https://www.postgresql.org/) - Database employed
* [NodeJS](https://nodejs.org/en/) - Frontend build process created
* [SemanticUI](https://semantic-ui.com/) - Front-end library used

## Author

* [John Judeh](https://www.linkedin.com/in/hannajudeh/)

## Acknowledgements

A big thank you to all of the friends who have talked through this idea with me
and helped me flesh out how it should work. This project is for you guys!
