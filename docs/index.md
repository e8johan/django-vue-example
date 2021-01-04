# Introduction

This guide will talk you through setting up a Django and Vue application. The intention is to establish best practices in some respect, but also for me to learn how to do this. Explaining something is the best way to learn.

# The Goal

The goal is to create a Django application with a Vue based user interface, creating a progressive web app. The goal is also to deploy as little as possible to the production environment, i.e. all bundling of assets and such is to happen in the development environment.

# Reference Documentation

Make sure that you are familiar with the following documents and tools:

* The Django First Steps Tutorial, found [here](https://docs.djangoproject.com/en/3.1/).
* The `django-compressor-parceljs` README, found [here](https://github.com/eadwinCode/django-compressor-parceljs).
* Some ParcelJS basics, found [here](https://parceljs.org/).

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

## The Example App

The example app will be a trivial todo application, showing a list of todo items. They can be checked and archived.

We begin with a simple model:

```
class Todo(models.Model):
    text = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
```

A migration is created from this model, and the project is migrated. The model is also added to the admin interface of Django. Please refer to the Django tutorial for details around this.

We will provide to views from the app, one entry-point for the Vue app, and one REST-like end-point for the dynamic part of the app. This is reflected in `todo/views.py`:

```
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello world")

def api_todo_list(request):
    return HttpResponse("Hello list")

def api_todo_details(request, todo_id):
    return HttpResponse("Hello details")
```

And in `todo/urls.py`:

```
from django.urls import path

from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.index, name='index'),
    
    path('api/todo', views.api_todo_list),
    path('api/todo/<int:todo_id>/', views.api_todo_details),
]
```

Notice the `app_name`, that provides a namespace to our url names.

## Delivering the Vue App

The next step is to deliver the Vue app. This will involve setting up the actual Vue infrastructure, including nodejs, `django-compressor-parceljs`, and their deps, as well as the ability to serve static files from the Django server in our development environment.

The general game plan is to deliver the app as a web page through the index call. The app will consist of an HTML entry point served as a Django template, and the app itself, served as static files.

### Install ParcelJS

```
npm init
npm install --save-dev parcel-bundler
```

Binaries end up in `node_modules/.bin`, so I create the following sourcable `source-to-set-path.sh` file:
 
```
PATH="$PATH:$(pwd)/node_modules/.bin/"
```

I source this file to initialize the environment just after having sources the Python virtual environment.

### Install django-compressor-parceljs

```
pip install django-compressor-parceljs
pip freeze > requirements.txt
```

Configure the app as detailed in the project documentation, i.e. alter the `INSTALLED_APPS` and `STATICFILES_FINDERS` in `settings.py`. Then add the following lines to your `development-local_settings.py` (and current `local_settings.py`).

```
COMPRESS_ENABLED = True
COMPRESS_REBUILD_TIMEOUT = 1
```

The first line enables the compressor, and the second makes sure that the cache is re-created every second, which is good for development (no need to restart the Django server).

Also, make sure that the Django server serves static files during development ([documentation](https://docs.djangoproject.com/en/3.1/howto/static-files/#serving-static-files-during-development)).


### Install Vue

```
npm install --save-dev vue-template-compiler @vue/component-compiler-utils
npm install vue
```

### Create the HTML, Javascript and Vue Files

These are the placeholder files to ensure that the setup is working. They represent the actual file structure, but contains no actual bindings or meaningful code.

#### todo/templates/todo/index.html

Note that the `index` function in `todo/views.py` is altered to serve this file using the `render` function.

```
{% load static %}
{% load compress %}

<html>
<head>

    <meta charset="UTF-8">

</head>
<body>

    <div id="app"></div>

{% compress parcel file todoapp %}
    <script src="{% static 'js/todoapp.js' %}"></script>
{% endcompress %}

</body>
</html>
```

#### todo/static/js/todoapp.js

```
import Vue from 'vue';
import TodoApp from '../components/TodoApp.vue';

new Vue(TodoApp).$mount("#app");
```

#### todo/static/components/TodoApp.vue

```
<template>
    <todo-list></todo-list>
</template>

<script>
import TodoList from './TodoList.vue'

export default {
    name: "todoapp",
    components: { TodoList },
    data: function() { 
        return {
        };
    },
    methods: {
    },
    mounted() {
    },
}
</script>
```

#### todo/static/components/TodoList.vue

```
<template>
    <todo-item></todo-item>
</template>

<script>
import TodoItem from './TodoItem.vue'

export default {
    name: "todo-list",
    components: { TodoItem },
    data: function() { 
        return {
        };
    },
    methods: {
    },
    mounted() {
    },
}
</script>
```

#### todo/static/components/TodoItem.vue

```
<template>
    <p>item!</p>
</template>

<script>
export default {
    name: "todo-item",
    components: {},
    data: function() { 
        return {
        };
    },
    methods: {
    },
    mounted() {
    },
}
</script>
```

### Running the Server

If everything is in place, you can run the local server using the following command:

```
NODE_ENV=development ./manage.py runserver
```

Make sure that you source the `source-to-set-path.sh` before running the server, otherwise it will complain about the `parcel` command not being found.

## Rendering the List Using Vue

The next step is to render the view using Vue. The idea is that we pass the data using the Django context, as usual when working with Django, but instead of rendering it in the template, we pick up the data from Vue and render it using Vue components.

Why do we do this? This is the first step on our path towards a reactive app using the REST-like API.

### Building the Context

In Django, we build the context using the following code.

```
def item_to_dict(item):
    return {
            'id': item.pk,
            'text': item.text,
            'done': item.is_done,
        }

def index(request):
    items = Todo.objects.all()
    itemlist = []
    for item in items:
        itemlist.append(item_to_dict(item))
    context = {
        'items': itemlist,
    }
    return render(request, 'todo/index.html', context = context)
```

The code above makes the context available to the Django template renderer. Using it we render a Javascript snippet exposing the context. This script is placed before the compressor is run.

```
<script>
const context_items = [
{% for item in items %}
    { 'id': {{ item.id }}, 'text': '{{ item.text }}', 'done': {% if item.done %}true{% else %}false{% endif %}    },
{% endfor %}
];
</script>
```

Notice that booleans need to be explicitly transformed to `true`/`false`. This is necessary as the Python booleans are called `True`/`False`.

### The Vue App

#### The Structure

Given two Todo items (created using the Django admin interface), the following Vue components are generated:

![](images/vue-structure.png&raw=true)

#### Getting the Context to Vue

The `VueApp`'s `mounted` function copies the context into the Vue state:

```
mounted() {
    this.items = context_items;
}
```

#### Listeners

When an `TodoItem` is clicked, it emits either `check` or `clear`. We want to catch these signals in the `TodoApp`, rather than in `TodoList`. To propagate it through, we use the `v-on="$listeners"` pattern in the `TodoList`.

##### TodoItem

```
<p>
    <span v-if="item.done" v-on:click="$emit('clear', item.id);">[x]</span>
    <span v-else="" v-on:click="$emit('check', item.id);">[&nbsp;]</span>
    {{ item.text }}
</p>
```

##### TodoList

```
<todo-item v-for="item in items" v-bind:item="item" v-on="$listeners"></todo-item>
```

##### TodoApp

First, the signals are caught in the template section:

```
<todo-list 
    v-bind:items="items"
    
    v-on:clear="on_clear"
    v-on:check="on_check"
></todo-list>
```

Then we catch the signals and arguments in the corresponding methods. Notice that event handler methods start with `on_` by convention.

```
methods: {
    /* Event handlers */
    
    'on_clear': function(id) {
        ...
    },
    'on_check': function(id) {
        ...
    },
}
```
