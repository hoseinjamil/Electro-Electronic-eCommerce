from django import forms
from .models import Newsletter


class NewsletterForm(forms.Form):
    email = forms.EmailField()
