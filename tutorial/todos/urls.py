from django.urls import path
from .views import *

urlpatterns = [
    path('', hello_python, name="hello_python"),
    path('todos/', todos_view, name='todos_view'),
    path('person/<int:person_id>/', person_details, name='person_details'),
    path('delete_todo/<int:todo_id>/', delete_todo, name='delete_todo'),
    path('toggle_todo_done/<int:todo_id>/', toggle_todo_done, name='toggle_todo_done'),
    path('htmlrender/', hello_html_view, name="hello_html_view"),
    path('template/', template_view, name="template_view"),
    path('special/', special_view, name="special_view"),
    path('hello/', hello_world, name='hello_world'),
    path('hello-query/', hello_query, name='hello_query'),
    path('hello/<str:name>/', hello_name, name='hello_name'),
    path('post-example/', post_example, name='post_example'),
    path('submit-example/', submit_example, name='submit_example'),
    path('submit-djangoform/', submit_djangoform, name='submit_djangoform'),
]
