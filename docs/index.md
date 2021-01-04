# Introductiin

This guide will talk you through setting up a Django and Vue application. The intention is to establish best practices in some respect, but also for me to learn how to do this. Explaining something is the best way to learn.

# The Goal

The goal is to create a Django application with a Vue based user interface, creating a progressive web app. The goal is also to deploy as little as possible to the production environment, i.e. all bundling of assets and such is to happen in the development environment.

# Reference Documentation

Make sure that you are familiar with the following documents:

* The Django First Steps Tutorial, found [here](https://docs.djangoproject.com/en/3.1/).

# The Guide

## Basic Setup

We start by setting up a Python virtual environment:

```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

Then we install Django, start a Django project and create a Django app. Notice that we change the directory after having created the Django project. The rest of this document will treat that directory as the project root.

```
pip install django
django-admin startproject djangovue
cd djangovue
django-admin startapp todo
```

And now we make some preparations before creating our initial commit:

Freeze all Python dependencies:

```
pip freeze > requirements.txt
```

Ensure that we don't commit our virtual environment, or any of Python's cached files:

```
echo "venv/" > .gitignore
echo "__pycache__/" >> .gitignore
```

Now we can create an initial commit:

```
git add manage.py requirements.txt djangovue todo
git commit -m "Initial commit"
```

## Separate Settings

Django is configured using the `settings.py` file. As this file contains both common and machine unique settings, I try to split it into a `local_settings.py` and the `settings.py`. This is done by having `settings.py` refer to `local_settings.py`.

At the bottom of `djangovue/settings.py`, add the following lines:

```
try:
    from .local_settings import *
except ImportError:
    pass
```

Then I move the lines `SECRET_KEY`, `DEBUG` and `ALLOWED_HOSTS` lines from `settings.py` to `local_settings.py`. Also, make sure to add `local_settings.py` to `.gitignore`:

```
echo "local_settings.py" >> .gitignore
```

I have a habit of creating a set of example `local_settings.py` in a directory called `example-configs/`. I call the `local_settings.py` from my development setup `example-configs/development-local_settings.py`. I usually also have a `production-local_settings.py`, acting as a template for production deployments, and a `test-local_settings.py`, acting as a template for an automated test environment. Make sure to remove the `SECRET_KEY` from these files, as they are to act as templates, not source files.