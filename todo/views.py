from django.http import HttpResponse
from django.shortcuts import render

from .models import Todo

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

def api_todo_list(request):
    return HttpResponse("Hello list")

def api_todo_details(request, todo_id):
    return HttpResponse("Hello details")
