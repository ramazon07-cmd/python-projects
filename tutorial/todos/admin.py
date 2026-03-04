from django.contrib import admin
from .models import Todo, Person

# Register your models here.

admin.site.register(Person)

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'completed', 'owner')
    list_filter = ('completed', 'owner')
    search_fields = ('title', 'description')