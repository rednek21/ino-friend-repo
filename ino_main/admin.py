from django.contrib import admin

from .models import FeedBack


@admin.register(FeedBack)
class FeedbackEmailAdmin(admin.ModelAdmin):
    list_display = ('code', 'email', 'message')
    fields = ('code', 'email', 'message')
