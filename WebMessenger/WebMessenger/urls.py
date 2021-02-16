from django.contrib import admin
from django.urls import path, include
from registration.urls import perfiles_patterns
from messenger.urls import messenger_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('perfiles/', include(perfiles_patterns)),
    # Path de Auth
    path('cuentas/', include('django.contrib.auth.urls')),
    path('cuentas/', include('registration.urls')),
    path('messenger/', include(messenger_patterns)),
]

# Configuracion por defecto si se quiere procesar archivos media (imagenes, etc) en la etapa de desarrollo
from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)