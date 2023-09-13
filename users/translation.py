from modeltranslation.translator import TranslationOptions, register
from .models import User, Hobby


@register(Hobby)
class HobbyTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('en',)


@register(User)
class UserTranslationOptions(TranslationOptions):
    fields = ('hobby', 'about_yourself')
    required_languages = ('en',)
