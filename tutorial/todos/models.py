from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

class PriorityChoice(models.IntegerChoices):
    LOW = 0, 'Low'
    MEDIUM = 1, 'Medium'
    HIGH = 2, 'High'

class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(choices=PriorityChoice.choices, default=PriorityChoice.LOW, null=True, blank=True)

    owner = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='todos', blank=True, null=True)

    def __str__(self):
        return self.title