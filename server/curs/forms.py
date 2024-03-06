from django import forms

class DateForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))