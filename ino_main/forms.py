from django import forms


class FeedBackForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mini-text', 'placeholder': 'Введите имя', 'type': 'mail', 'id': 'mail', 'rows': '5',
    }), required=False)

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control mini-text', 'placeholder': 'Введите почту', 'type': 'mail', 'rows': '5',
    }))

    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control mini-text', 'placeholder': 'Введите текст', 'rows': '5',
    }))

    class Meta:
        fields = ['name', 'email', 'message']
