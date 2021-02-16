from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django import forms
from .models import Perfil
from .forms import UserCreationFormConEmail, PerfilForm, EmailForm
# Usamos las vistas genéricas para crear CBV
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
# Con los decoradores indicamos que para acceder a ciertas vistas 
# como modificar el perfil el usuario debe estar autenticado (login_required)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Vista que mostrará un listado de los perfiles
class PerfilListView(ListView):
    # Modelo al cual representará la vista
    model = Perfil
    # Indica el numero de perfiles que se mostrarán el la paginación
    paginate_by = 3

# Vista que mostrará los detalles de un perfil especificado (Mi Perfil)
class PerfilDetailView(DetailView):
    # Modelo al cual representará la vista
    model = Perfil
    
    # Redefinimos el método get_object() para que recupere el perfil del usuario
    def get_object(self):
        return get_object_or_404(Perfil, user__username=self.kwargs['username'])

# Vista que permitirá registrarse en el sitio con un nuevo usuario
class RegistrarseView(CreateView):
    # Formulario personalizado utilizado para registrarse
    form_class = UserCreationFormConEmail
    # Template que se mostrara cuando se llame a la vista
    template_name = 'registration/registro.html'

    # Función para redefinir a donde nos redireccionará luego de registrado satisfactoriamente el usuario pasándole un mensaje en GET
    def get_success_url(self):
        # En este caso a la página de autenticación de usuario (login) con un mensaje en el GET (?registrado)
        return reverse_lazy('login') + '?registrado'
    
    # Se redefine el metodo get_form() para modificar el formulario de registro de usuario
    def get_form(self, form_class=None):
        form = super(RegistrarseView, self).get_form()
        # Modificando el formulario en tiempo de ejecucion
        # Campo username
        form.fields['username'].widget = forms.TextInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Nombre de usuario'})
        # Campo email
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Dirección email'})
        # Campo password
        form.fields['password1'].widget = forms.PasswordInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Contraseña'})
        # Campo confirmación de password
        form.fields['password2'].widget = forms.PasswordInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Repetir contraseña'})
        return form

# Vista que permitirá modificar el perfil, solo en caso de estar autenticado (login_required)
@method_decorator(login_required, name='dispatch')
class ModificarPerfilView(UpdateView):
    # Formulario personalizado utilizado para modificar el perfil
    form_class = PerfilForm
    # Página a la que nos redireccionará una vez modificado el perfil
    success_url = reverse_lazy('mi_perfil')
    # Template que se mostrara cuando se llame a la vista
    template_name = 'registration/perfil_update_form.html'

    # Se redefine el metodo get_object() para recuperar el perfil
    def get_object(self):
        profile, created = Perfil.objects.get_or_create(user=self.request.user)
        return profile

# Vista que permitirá modificar el perfil, solo en caso de estar autenticado (login_required)
@method_decorator(login_required, name='dispatch')
class ModificarEmailView(UpdateView):
    # Formulario personalizado utilizado para modificar el email
    form_class = EmailForm
    # Página a la que nos redireccionará una vez modificado el perfil
    success_url = reverse_lazy('mi_perfil')
    # Template que se mostrara cuando se llame a la vista
    template_name = 'registration/perfil_update_email_form.html'
    
    # Se redefine el método get_object() para recuperar el usuario que se le modificará el email
    def get_object(self):
        return self.request.user

    # Se redefine el metodo get_form() para modificar el formulario de modificación de email
    def get_form(self, form_class=None):
        form = super(ModificarEmailView, self).get_form()
        # Modificando el formulario en tiempo de ejecucion
        # Campo email
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Dirección email'})
        return form