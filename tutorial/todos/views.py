from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello_world(request):
    return HttpResponse("Hello World!")

def hello_python(request):
    return HttpResponse("Hello Python!")

def hello_html_view(request):
    return render(request, 'hello.html')

def hello_name(request, name):
    return HttpResponse(f"Hello {name}!")
