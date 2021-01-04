from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello world")

def api_todo_list(request):
    return HttpResponse("Hello list")

def api_todo_details(request, todo_id):
    return HttpResponse("Hello details")
