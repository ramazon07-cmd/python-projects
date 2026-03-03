from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from .forms import PersonForm

# Create your views here.

def hello_world(request):
    return HttpResponse("Hello World!")

def hello_python(request):
    return HttpResponse("Hello Python!")

def hello_html_view(request):
    return render(request, 'hello.html')

def hello_name(request, name):
    return HttpResponse(f"Hello {name}!")

def hello_query(request):
    name = request.GET.get('q')
    return HttpResponse(f"Hello {name}!")

def special_view(request):
    # do some staff
    return redirect('hello_html_view')

def post_example(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            return HttpResponse(f"Hello {name}, you are {age} years old!")
    else:
        return HttpResponseNotAllowed(['POST'])

def submit_example(request):
    return render(request, 'submit.html')

def submit_djangoform(request):
    form = PersonForm()
    return render(request, 'submit_djangoform.html', {'form': form})

def template_view(request):
    context = {
        'name': 'John',
        'age': 30,
        'hobbies': ['Reading', 'Traveling', 'Cooking']
    }
    return render(request, 'template_demo.html', context)











