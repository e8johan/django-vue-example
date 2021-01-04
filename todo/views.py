import json

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Todo

def item_to_dict(item):
    return {
            'id': item.pk,
            'text': item.text,
            'done': item.is_done,
        }

@ensure_csrf_cookie
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
    """
        End-point for /api/todo/
        
        # GET
        
        Returns a list of todo item dicts with the following keys:
        
        - `id` - integer, unique id of task
        - `text` - text string, human readable description of task
        - `done` - boolean, indicating if the task is done
        
        # POST
        
        Expects a json body containing the following keys:
        
        - `text`, text string, human readable description of task
        
        Returns a single item dict as described in the GET section
    """
    if request.method == 'GET':
        items = Todo.objects.all()
        itemlist = []
        for item in items:
            itemlist.append(item_to_dict(item))
            
        return HttpResponse(json.dumps(itemlist, ensure_ascii = False))
    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode("UTF-8"))
        except ValueError:
            return HttpResponseBadRequest()
        
        if 'text' not in data:
            return HttpResponseBadRequest()
        
        item = Todo(text=str(data['text']).strip())
        item.save()
        
        return HttpResponse(json.dumps(item_to_dict(item), ensure_ascii=False))
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

    return HttpResponse("Hello list")

def api_todo_details(request, todo_id):
    """
        API end point for /api/todo/<todo_id>/
        
        # PATCH
        
        Updates the todo item information. Expects a body with a json struct with the following parameter:
        
        - `done`, boolean, indicating if the task is done
        
        Returns a single item dict as described in the /api/todo/ GET section.
        
        # DELETE
        
        Deletes the item.
        
        Returns an empty dict.
    """
    if request.method == 'PATCH':
        item = get_object_or_404(Todo, pk = todo_id)
        
        try:
            data = json.loads(request.body.decode("UTF-8"))
        except ValueError:
            return HttpResponseBadRequest()

        if 'done' not in data:
            return HttpResponseBadRequest()

        item.is_done = data['done']
        item.save()
        
        return HttpResponse(json.dumps(item_to_dict(item), ensure_ascii = False))
    elif request.method == 'DELETE':
        item = get_object_or_404(Todo, pk = todo_id)
        item.delete()
        return HttpResponse(json.dumps({}))
    else:
        return HttpResponseNotAllowed(['PATCH', 'DELETE'])
