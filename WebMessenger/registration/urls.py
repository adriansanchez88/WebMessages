from django.urls import path
from .views import PerfilListView, PerfilDetailView, RegistrarseView, ModificarPerfilView, ModificarEmailView

# Establecemos una nueva variable 'perfiles_patterns' para llamar a los path de la forma 'perfiles:name_del_path'
# se tendrá que importar el urls.py de la app en el urls.py del proyecto e incluir la variable modelos_patterns
perfiles_patterns = ([
    path('', PerfilListView.as_view(), name='list'),
    path('<username>/', PerfilDetailView.as_view(), name='detail'),
], 'perfiles')
# También usaremos el urlpatterns para el resto de los path que no son de los perfiles
urlpatterns = [
    path('registro/', RegistrarseView.as_view(), name='registro'),
    path('mi_perfil/', ModificarPerfilView.as_view(), name='mi_perfil'),
    path('mi_perfil/modificar_email/', ModificarEmailView.as_view(), name='mi_perfil_update_email'),
]