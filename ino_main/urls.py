from django.urls import path

from .views import AboutView, CookieView, PrivacyView

app_name = 'ino_main'

urlpatterns = [

    path('', AboutView.as_view(), name='about'),
    path('cookie/', CookieView.as_view(), name='cookie'),
    path('privacy_policy/', PrivacyView.as_view(), name='privacy_policy'),



]
