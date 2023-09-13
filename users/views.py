from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect

from django.conf import settings

from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView

from django.views.generic.edit import CreateView, UpdateView
from django.contrib import auth, messages
from django.contrib.auth.views import TemplateView, LoginView, PasswordResetView, PasswordResetConfirmView
from .models import User, EmailVerification, Hobby
from common.views import CommonContextMixin
from .forms import (UserLoginForm, UserRegistrationForm, UserProfileEditForm, UserQuestionnaireForm,
                    PasswordRecoveryForm, HobbyForm, UserSearchForm, NewPasswordForm)


class UserRegistrationView(CommonContextMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    title = 'INO - Регистрация'
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Пользователь с таким email уже существует.\nUser with this email already exists.")
        return response


class UserLoginView(CommonContextMixin, LoginView):
    template_name = 'users/login.html'
    authentication_form = UserLoginForm
    title = 'INO - Авторизация'

    def get_success_url(self):
        return reverse_lazy('users:profile_edit', args=(self.request.user.id,))

    def form_invalid(self, form):
        # Добавляем своё сообщение об ошибке в случае неверного логина или пароля
        messages.error(self.request, 'Неверный логин или пароль.\nInvalid username or password.')
        return super().form_invalid(form)

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(settings.SESSION_COOKIE_AGE)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().get(request, *args, **kwargs)


class UserPasswordReset(PasswordResetView):
    template_name = 'users/password_reset.html'
    form_class = PasswordRecoveryForm
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset')
    from_email = settings.EMAIL_HOST_USER

    def form_valid(self, form):
        email = form.cleaned_data['email']

        try:
            user = User.objects.get(email=email)
        except:
            form.add_error('email', 'Пользователь с указанным email не найден.\nUser with this email was not found.')
            return self.form_invalid(form)

        form.save(
            subject_template_name=self.email_template_name,
            from_email=self.from_email,
            email_template_name=self.email_template_name,
            use_https=self.request.is_secure(),
            request=self.request,
        )

        messages.success(self.request, 'На указанный email было отправлено письмо для создания нового пароля.')
        return super().form_valid(form)


class UserPasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = NewPasswordForm
    success_url = reverse_lazy('users:login')


class ProfilesView(LoginRequiredMixin, CommonContextMixin, ListView):
    model = User
    template_name = 'users/all_profiles.html'
    context_object_name = 'users'
    title = 'INO - Анкеты'
    paginate_by = 8

    @staticmethod
    def user_check(request):
        user = request.user

        conditions_not_met = []

        if user.first_name == '' or user.first_name == 'Имя':
            conditions_not_met.append("имя")
        if user.last_name == '' or user.last_name == 'Фамилия':
            conditions_not_met.append("фамилия")
        if user.university == '':
            conditions_not_met.append("Университет")
        if user.preferred_language == '':
            conditions_not_met.append("Изучаемый язык")
        if user.hobby is None:
            conditions_not_met.append("Интересы")
        if user.birthdate is None:
            conditions_not_met.append("Дата рождения")
        if not user.is_verified_email:
            conditions_not_met.append("Почта")
        if user.url is None:
            conditions_not_met.append("Ссылка")

        return conditions_not_met

    def get_queryset(self):
        queryset = User.objects.exclude(
            Q(first_name='') |
            Q(first_name='Имя') |
            Q(last_name='') |
            Q(last_name='Фамилия') |
            Q(url__isnull=True) |
            Q(is_verified_email=False) |
            Q(university='') |
            Q(preferred_language='') |
            Q(birthdate__isnull=True) |
            Q(hobby__isnull=True)
        )

        hobby = self.request.GET.get('hobby')
        if hobby:
            queryset = queryset.filter(hobby__title=hobby)

        preferred_language = self.request.GET.get('preferred_language')
        if preferred_language:
            queryset = queryset.filter(preferred_language=preferred_language)

        gender = self.request.GET.get('gender')
        if gender:
            queryset = queryset.filter(gender=gender)

        university = self.request.GET.get('university')
        if university:
            queryset = queryset.filter(university=university)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserSearchForm(self.request.GET)
        context['conditions'] = self.user_check(self.request)
        return context


class UserProfileEditView(LoginRequiredMixin, CommonContextMixin, UpdateView):
    model = User
    form_class = UserProfileEditForm
    template_name = 'users/profile_edit.html'
    title = 'INO - Редактирование профиля'

    def get_success_url(self):
        return reverse_lazy('users:profile_edit', args=(self.request.user.id,))

    def form_valid(self, form):
        user = User.objects.get(id=self.request.user.id)

        image = self.request.FILES.get('image')
        if image:
            if image.size <= 5 * 1024 * 1024:
                user.image = image
                user.save()
            else:
                return self.form_invalid(form)
        else:
            user.save()
        return super().form_valid(form)


class QuestionnaireView(CommonContextMixin, LoginRequiredMixin, View):
    template_name = 'users/questionnaire_edit.html'
    title = 'INO - Редактирование анкеты'

    @classmethod
    def initial_form(cls, request):
        qf = UserQuestionnaireForm(initial={
            'birthdate': request.user.birthdate,
            'gender': request.user.gender,
            'native_language': request.user.native_language,
            'preferred_language': request.user.preferred_language,
            'residence_city': request.user.residence_city,
            'native_country': request.user.native_country,
            'university': request.user.university,
            'specialty': request.user.specialty,
        })

        hf = HobbyForm(initial={
            'hobby': request.user.hobby.all(),
        })

        form_dict = {'qf': qf, 'hf': hf, 'title': cls.title}
        return form_dict

    def get(self, request, *args, **kwargs):
        forms_dict = self.initial_form(request)

        hobbies = Hobby.objects.all()

        context = {
            'hf': forms_dict['hf'],
            'qf': forms_dict['qf'],
            'hobbies': hobbies,
            'title': self.title
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        qf = UserQuestionnaireForm(request.POST)
        hf = HobbyForm(request.POST)
        user = User.objects.get(id=request.user.id)

        if qf.is_valid():
            bd = qf.cleaned_data['birthdate']
            gender = qf.cleaned_data['gender']
            native_language = qf.cleaned_data['native_language']
            preferred_language = qf.cleaned_data['preferred_language']
            native_country = qf.cleaned_data['native_country']
            residence_city= qf.cleaned_data['residence_city']
            university = qf.cleaned_data['university']
            specialty = qf.cleaned_data['specialty']

            user.birthdate = bd
            user.gender = gender
            user.native_language = native_language
            user.preferred_language = preferred_language
            user.native_country = native_country
            user.residence_city= residence_city
            user.university = university
            user.specialty = specialty

            user.save()

            forms_dict = self.initial_form(request)
            context = {
                'hf': forms_dict['hf'],
                'qf': forms_dict['qf'],
                'hobbies': Hobby.objects.all(),
                'title': self.title,
            }
            return redirect(reverse_lazy('users:profile', args=(self.request.user.id,)))

        if hf.is_valid():
            hobby = hf.cleaned_data['hobby']
            user.hobby_ru.set(hobby)
            user.hobby_en.set(hobby)
            user.save()

            forms_dict = self.initial_form(request)
            context = {
                'hf': forms_dict['hf'],
                'qf': forms_dict['qf'],
                'hobbies': Hobby.objects.all(),
                'title': self.title,
            }

            return render(request, self.template_name, context)


class UserProfileView(LoginRequiredMixin, CommonContextMixin, TemplateView):
    model = User
    template_name = 'users/profile.html'
    title = 'INO - Профиль'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.id,))


class SomeProfileView(LoginRequiredMixin, CommonContextMixin, TemplateView):
    model = User
    template_name = 'users/profile_view.html'

    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        title = f'INO - {user.first_name} {user.last_name}'
        context = {'user': user, 'title': title}
        return render(request, self.template_name, context)


class EmailVerificationView(CommonContextMixin, UpdateView):
    template_name = 'users/profile_edit.html'
    form_class = UserProfileEditForm
    title = 'INO - Редактирование профиля'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            auth.login(request, user)
            return HttpResponseRedirect(self.get_success_url())
        return super(EmailVerificationView, self).get(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('users:profile_edit', args=(self.request.user.id,))


class ResetPasswordView(CommonContextMixin, PasswordResetView):
    template_name = 'users/password_reset.html',
    form_class = PasswordRecoveryForm,
    email_template_name = 'users/password_reset_email.html',
    success_url = reverse_lazy('users:login')
    title = 'INO - Восстановление пароля'


@login_required
def user_delete(request, id):
    user = User.objects.get(id=id)
    if request.user == user:
        auth.logout(request)
        user.delete()

        return HttpResponseRedirect(reverse('users:login'))
    else:
        return HttpResponse('У вас нет разрешения на удаление операций')


def delete_user_image(request, id):
    user = User.objects.get(id=id)
    if request.user == user:
        user.image.delete(save=True)

    return HttpResponseRedirect(reverse('users:profile_edit', args=(request.user.id,)))
