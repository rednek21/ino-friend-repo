from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings

from django.utils.timezone import now
from users.managers import CustomUserManager

from cities.models import Country

from datetime import date


class Hobby(models.Model):
    title = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name = 'hobby'
        verbose_name_plural = 'hobbies'

    def __str__(self):
        return f'{self.title}'


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=30, blank=True, null=True)
    first_name = models.CharField(verbose_name=_('first_name'), max_length=30, default='Имя')
    last_name = models.CharField(verbose_name=_('last_name'), max_length=30, default='Фамилия')
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(verbose_name=_('gender'), max_length=50, null=True, blank=True)
    password = models.CharField(max_length=100)
    native_language = models.CharField(verbose_name=_('native_language'), max_length=30, null=True, blank=True)
    preferred_language = models.CharField(verbose_name=_('preferred_language'), max_length=30, null=True, blank=True)
    residence_city = models.CharField(verbose_name=_('residence_city'), max_length=128, null=True, blank=True)
    native_country = models.ForeignKey(verbose_name=_('native_country'), to=Country, on_delete=models.SET_NULL,
                                       max_length=128, null=True, blank=True)
    university = models.CharField(verbose_name=_('university'), max_length=100, null=True, blank=True)
    specialty = models.CharField(verbose_name=_('specialty'), max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    hobby = models.ManyToManyField('Hobby')
    url = models.CharField(null=True, blank=True, max_length=64)
    about_yourself = models.TextField(verbose_name=_('about_yourself'), null=True, blank=True)
    remember_me = models.BooleanField(default=True)
    is_verified_email = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_user_age_ru(self):
        today = date.today()
        age = today.year - self.birthdate.year - (
                (today.month, today.day) < (self.birthdate.month, self.birthdate.day))

        if age % 10 == 1:
            return f'{age} год'
        elif age % 10 in (2, 3, 4):
            return f'{age} года'
        else:
            return f'{age} лет'

    def get_user_age_en(self):
        today = date.today()
        age = today.year - self.birthdate.year - (
                (today.month, today.day) < (self.birthdate.month, self.birthdate.day))

        if age % 10 == 1:
            return f'{age} year'
        elif age % 10 in (2, 3, 4, 5, 6, 7, 8, 9, 0):
            return f'{age} years'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_url(self):
        nickname = str(self.url)
        nickname = nickname.replace('@', '')
        url = f'https://t.me/{nickname}'
        return url

    def __str__(self):
        return f'Mail: {self.email}'
        # return f'Username: {self.username} | University: {self.university} | Mail: {self.email}'


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.email}'
        message = 'Для подтверждения учетной записи для {} перейдите по ссылке: {}'.format(
            self.user.email,
            verification_link,
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
