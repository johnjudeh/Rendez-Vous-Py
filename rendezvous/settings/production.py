"""
Django production settings for RendezVous project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
from rendezvous.settings.base import *
import django_heroku


# General Settings

DEBUG = False


# Security Settings

ALLOWED_HOSTS = ['rendezvous-py.herokuapp.com']

SECURE_SSL_REDIRECT = True

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = 'DENY'


# Deployment to Heroku

django_heroku.settings(locals(), staticfiles=False, allowed_hosts=False)