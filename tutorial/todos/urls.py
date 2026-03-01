from django.urls import path
from .views import *

urlpatterns = [
    path('', hello_python, name="hello_python"),
    path('htmlrender/', hello_html_view, name="hello_html_view"),
    path('hello/', hello_world, name='hello_world'),
    path('hello/<str:name>/', hello_name, name='hello_name'),
]
