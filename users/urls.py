from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (UserRegistrationView, UserLoginView, UserProfileEditView,
                    UserProfileView, EmailVerificationView, user_delete, delete_user_image,
                    ProfilesView, QuestionnaireView, SomeProfileView, UserPasswordReset, UserPasswordResetConfirm,)
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile_edit/<int:pk>/', UserProfileEditView.as_view(), name='profile_edit'),
    path('profile/<int:id>/', UserProfileView.as_view(), name='profile'),
    path('profile_view/<int:id>/', SomeProfileView.as_view(), name='profile_view'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('questionnaire_edit/<int:pk>/', QuestionnaireView.as_view(), name='questionnaire_edit'),

    path('profiles/', ProfilesView.as_view(), name='profiles'),

    path('delete_user/<int:id>/', user_delete, name='delete_user'),
    path('delete_user_image/<int:id>/', delete_user_image, name='delete_user_image'),

    path('password_reset/', UserPasswordReset.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', UserPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),

]
