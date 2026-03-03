from django import forms

class PersonForm(forms.Form):
    name = forms.CharField(max_length=100, required=False) # it means that it is not required to fill in the name field
    age = forms.IntegerField(min_value=0, label='Age (must be a positive integer)') 
    