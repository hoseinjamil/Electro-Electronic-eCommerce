from django import forms


class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=20,
                           widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'John'}))
    email = forms.EmailField()
    subject = forms.CharField(max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Cooperate'}))
    body = forms.CharField(max_length=300, widget=forms.Textarea(
        attrs={"class": "form-control", 'placeholder': 'how can i cooperate with you?'}))
