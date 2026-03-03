from django.urls import path
from .views import *

urlpatterns = [
    path('', hello_python, name="hello_python"),
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
