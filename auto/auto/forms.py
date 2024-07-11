from django import forms

class ContactForm(forms.Form):
    name=forms.CharField(max_length=100)
    contact=forms.CharField(max_length=30)
    birthday = forms.DateField(input_formats=['%m/%d/%Y'], widget=forms.DateInput(format='%m/%d/%Y'))



