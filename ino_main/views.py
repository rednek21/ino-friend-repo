import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from common.views import CommonContextMixin

from ino_main.forms import FeedBackForm
from ino_main.models import FeedBack


class AboutView(CommonContextMixin, FormView):
    template_name = 'ino_main/about.html'
    form_class = FeedBackForm
    title = 'INO - О нас'
    success_url = reverse_lazy('ino_main:about')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        feedback = FeedBack(code=uuid.uuid4(), name=name, email=email, message=message)
        feedback.save()

        # Отправка письма
        send_mail(
            subject='Feedback',
            message=f'Name: {name}\nEmail: {email}\nMessage: {message}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return super().form_valid(form)


class CookieView(CommonContextMixin, TemplateView):
    template_name = 'ino_main/cookies.html'
    title = 'INO - Cookie'


class PrivacyView(CommonContextMixin, TemplateView):
    template_name = 'ino_main/privacy.html'
    title = 'INO - Политика конфиденциальности'


def error400(request, exception):
    return render(request, 'ino_main/error400.html', {})


def error404(request, exception):
    return render(request, 'ino_main/error404.html', {})


def error500(request, exception=None):
    return render(request, 'ino_main/error500.html', {})


def technical_break(request, exception):
    return render(request, 'ino_main/technical_break.html', {})
