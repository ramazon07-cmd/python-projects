from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from .forms import PersonForm, TodoForm
from .models import Todo
from .models import Person

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


def todos_view(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save()
            return HttpResponse(f"Todo '{todo.title}' created successfully!")
    else:
        form = TodoForm()
        todos = Todo.objects.all()
        return render(request, 'todos.html', {'todos': todos, 'form': form})


def person_details(request, person_id):
    person = Person.objects.filter(id=person_id).first()

    return render(request, 'person_details.html', {'person': person})

def delete_todo(request, todo_id):
    todo = Todo.objects.filter(id=todo_id).first()

    todo.delete()

    return HttpResponse("Todo deleted successfully!")


def toggle_todo_done(request, todo_id):
    todo = Todo.objects.filter(id=todo_id).first()

    todo.completed = not todo.completed
    todo.save()

    return HttpResponse("Todo toggled successfully!")


