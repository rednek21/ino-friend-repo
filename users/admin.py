from django.contrib import admin

from users.models import User, EmailVerification, Hobby
from modeltranslation.admin import TranslationAdmin


@admin.register(Hobby)
class HobbyAdmin(TranslationAdmin):
    fields = ('title',)
    list_display = ('title',)


@admin.register(User)
class UserAdmin(TranslationAdmin):
    list_display = ('email', 'is_verified_email', 'url')


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created',)
