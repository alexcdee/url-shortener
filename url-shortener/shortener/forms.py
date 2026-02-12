from django import forms

class UrlForm(forms.Form):
    url = forms.URLField(label='Original URL', max_length=500)