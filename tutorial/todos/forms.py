from django import forms
from .models import Todo

class PersonForm(forms.Form):
    name = forms.CharField(max_length=100, required=False) # it means that it is not required to fill in the name field
    age = forms.IntegerField(min_value=0, label='Age (must be a positive integer)') 

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'completed', 'deadline', 'priority']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }