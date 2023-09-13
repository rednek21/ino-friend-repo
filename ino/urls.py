
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('chaining/', include('smart_selects.urls')),

] + i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('ino_main.urls', namespace='ino_main')),
    path('users/', include('users.urls', namespace='users')),
    prefix_default_language=False
)

handler400 = 'ino_main.views.error400'
handler404 = 'ino_main.views.error404'
handler500 = 'ino_main.views.error500'


if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
