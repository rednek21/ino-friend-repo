from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordResetForm, \
    SetPasswordForm

from datetime import datetime, timedelta

from cities.models import Country

from .models import User, Hobby
from .selections import choice_fields
from users.tasks import send_email_verification

import json

universities_path = 'static/vendor/json/universities.json'
languages_path = 'static/vendor/json/languages.json'
cities_path = 'static/vendor/json/cities.json'


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control mail_entrance', 'placeholder': 'Введите email', 'autofocus': True, 'type': 'username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control pass_entrance', 'placeholder': 'Введите пароль', 'type': 'password'
    }))
    remember_me = forms.BooleanField(required=False, initial=True,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'autocomplete': 'current-password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'remember_me')


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control mail', 'placeholder': 'Введите email', 'autofocus': True, 'type': 'username'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control pass1', 'placeholder': 'Введите пароль', 'id': 'errorcolor',
        'data-bs-container': 'body', 'data-bs-toggle': 'popover', 'data-bs-placement': 'right',
        'data-bs-trigger': 'focus',
        'data-bs-content': 'Пароль должен состоять из букв латинского алфавита, содержать не менее 8 символов, включая заглавные буквы, цифры и знаки',
        'type': 'password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control pass2', 'placeholder': 'Повторите пароль', 'type': 'password'
    }))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        send_email_verification.delay(user.id)
        return user


class UserProfileEditForm(UserChangeForm):
    # 'onchange': 'this.form.submit()' - для поля image, чтобы изображение загружалось без подтверждения
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control mini-text', 'accept': 'image/*', 'onchange': 'this.form.submit()'
    }), required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mini-text', 'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mini-text', 'placeholder': 'Введите фамилию'
    }))
    url = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mini-text', 'placeholder': 'Введите ссылку'
    }))
    about_yourself = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control mini-text', 'placeholder': 'Напишите кратко о себе', 'rows': '5'
    }), required=False)

    class Meta:
        model = User
        # fields = ('image', 'cropping', 'first_name', 'last_name', 'url', 'about_yourself')
        fields = ('image', 'first_name', 'last_name', 'url', 'about_yourself')


class UserQuestionnaireForm(UserChangeForm):

    @staticmethod
    def get_universities():
        with open(universities_path, 'r', encoding='utf-8') as file:
            universities_data = json.load(file)

        university_names = []

        for university in universities_data:
            university_name = university.get('name')
            if university_name:
                university_names.append(university_name)

        universities = [(university_name, university_name) for university_name in university_names]

        universities = sorted(universities)

        universities.insert(0, (None, "Выберите университет"))

        return universities

    @staticmethod
    def get_languages():
        with open(languages_path, 'r', encoding='utf-8') as file:
            languages_data = json.load(file)

        languages_names = languages_data.get('languages')

        languages = [(language, language) for language in languages_names]

        languages = sorted(languages)

        languages.insert(0, (None, "Выберите язык"))

        return languages

    @staticmethod
    def get_cities():
        with open(cities_path, 'r', encoding='utf-8') as file:
            cities_data = json.load(file)

        cities_names = cities_data.get('cities')

        cities = [(city, city) for city in cities_names]

        cities = sorted(cities)

        cities.insert(0, (None, "Выберите город"))

        return cities

    birthdate = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={
        'class': 'form-control mini-text',
        'type': 'date',
        'min': (datetime.today() - timedelta(days=60 * 365)).strftime('%Y-%m-%d'),
        'max': (datetime.today() - timedelta(days=16 * 365)).strftime('%Y-%m-%d'),
    }))
    gender = forms.ChoiceField(choices=choice_fields.GENDER_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select mini-text', 'aria-label': 'Defaut selelct example',
    }))
    native_language = forms.ChoiceField(choices=get_languages(), widget=forms.Select(attrs={
        'class': 'form-select mini-text',
    }))
    preferred_language = forms.ChoiceField(choices=get_languages(), widget=forms.Select(attrs={
        'class': 'form-select mini-text',
    }))
    native_country = forms.ModelChoiceField(queryset=Country.objects.all().only('name').order_by('name'),
                                            empty_label='Выберите страну',
                                            widget=forms.Select(attrs={
                                                'class': 'form-select mini-text',
                                            }))
    residence_city = forms.ChoiceField(choices=get_cities(),
                                       widget=forms.Select(attrs={
                                           'class': 'form-select mini-text',
                                           'id': 'residence_city'
                                       }), required=False)
    university = forms.ChoiceField(choices=get_universities(), widget=forms.Select(attrs={
        'class': 'form-select mini-text', 'aria-label': "Default select example",
    }))
    specialty = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mini-text', 'placeholder': 'Введите специальность'
    }), required=False)

    class Meta:
        model = User
        fields = ('birthdate', 'gender', 'native_language', 'preferred_language',
                  'residence_city', 'native_country', 'university', 'specialty')


class PasswordRecoveryForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'id': 'mail', 'type': 'email', 'class': 'form-control login', 'placeholder': 'Введите email'
    }))

    class Meta:
        fields = ('email',)


class HobbyForm(forms.ModelForm):
    hobby = forms.ModelMultipleChoiceField(queryset=Hobby.objects.all().order_by('pk'),
                                           widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-btn'}),
                                           required=False)

    class Meta:
        model = Hobby
        fields = ('hobby',)


class NewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'errorcolor', 'data-bs-container': 'body', 'data-bs-toggle': 'popover',
        'data-bs-placement': 'right', 'data-bs-trigger': 'focus',
        'data-bs-content': 'Пароль должен состоять из букв латинского алфавита, содержать не менее 8 символов, включая заглавные буквы, цифры и знаки',
        'data-bs-custom-class': 'custom-popover', 'type': 'password', 'class': 'form-control pass1',
        'placeholder': 'Введите новый пароль'
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': 'password', 'class': 'form-control pass2', 'placeholder': 'Повторите новый пароль'
    }))

    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')


class UserSearchForm(forms.Form):
    hobby_choices = [(hobby.id, hobby.title_ru, hobby.title_en) for hobby in Hobby.objects.all()]
    # hobby_choices = []
    hobby = forms.MultipleChoiceField(choices=hobby_choices,
                                      required=False)
    # hobby = forms.ModelMultipleChoiceField(queryset=Hobby.objects.all(), required=False)
    preferred_language = forms.ChoiceField(choices=UserQuestionnaireForm.get_languages()[1:], widget=forms.Select(attrs={
        'class': 'form-select mini-text',
        'placeholder': 'Выберите изучаемый язык'
    }))
    gender = forms.ChoiceField(choices=choice_fields.GENDER_CHOICES[1:], required=False)
    residence_city = forms.ChoiceField(choices=UserQuestionnaireForm.get_cities()[1:],
                                       widget=forms.Select(attrs={
                                           'class': 'form-select mini-text',
                                           'placeholder': 'Выберите город',
                                           'id': 'residence_city',
                                       }), required=False)
    university = forms.ChoiceField(choices=UserQuestionnaireForm.get_universities()[1:], widget=forms.Select(attrs={
        'class': 'form-select mini-text', 'aria-label': "Default select example",
        'placeholder': 'Выберите ВУЗ'
    }), required=False)

    class Meta:
        fields = ('hobby', 'preferred_language', 'gender', 'residence_city', 'university')
