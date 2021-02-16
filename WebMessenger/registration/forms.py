from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil

# Formulario de creación y modificación de Perfil
class PerfilForm(forms.ModelForm):    
    # Se establecen en la clase Meta las configuraciones del formulario
    class Meta:
        # El modelo al cual va a representar el formulario
        model = Perfil
        # Los campos del modelo que se mostrarán en el formulario
        fields = ['avatar', 'bio', 'link']
        # Los componentes que representarán a cada campo
        # class: el estilo css que utilizará cada componente
        # placeholder: el texto fantasma que se mostrará en el componente antes de escribir en ellos        
        widgets = {
            'avatar': forms.ClearableFileInput(
                attrs={'class':'form-control-file mt-3'}),
            'bio': forms.Textarea(
                attrs={'class':'form-control mt-3', 'rows':3, 'placeholder':'Biografía'}),
            'link': forms.URLInput(
                attrs={'class':'form-control mt-3', 'placeholder':'Enlace'}),
        }

# Formulario UserCreationForm modificado para que se creee el usuario también con el campo 'email'
class UserCreationFormConEmail(UserCreationForm):
    # Campo email representado por un componente EmailField
    email = forms.EmailField(required=True, help_text='Requerido, 254 caracteres como máximo y debe ser válido')

    # Se establecen en la clase Meta las configuraciones del formulario
    class Meta:
        # El modelo al cual va a representar el formulario
        model = User
        # Los campos que se mostrarán en el formulario (username, password1 y password2 estan definidos en el UserCreationForm original)
        fields = ('username', 'email', 'password1', 'password2')
    
    # Se redefine la funcion clean_email (que se llama automáticamente al crear un usuario y comprueba si el email tiene el formato 
    # adecuado) y se le agrega la comprobación de que ese email no lo tenga ya registrado otro usuario
    def clean_email(self):
        # Obtenemos el email procesado (con formato adecuado)
        email = self.cleaned_data.get('email')
        # Comprobamos que no exista un usuario registrado ya con ese email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya esta registrado, prueba con otro')
        return email

# Formulario utilizado para modifiacr el email
class EmailForm(forms.ModelForm):
    # Campo email representado por un componente EmailField
    email = forms.EmailField(required=True, help_text='Requerido, 254 caracteres como máximo y debe ser válido')
    # Se establecen en la clase Meta las configuraciones del formulario
    class Meta:
        # El modelo al cual va a representar el formulario
        model = User
        # El campo que se mostrará en el formulario
        fields = ['email']

    # Se redefine la funcion clean_email (que se llama automáticamente al modificar el email y comprueba si el este tiene el 
    # formato adecuado) y se le agrega la comprobación de que no lo tenga ya registrado otro usuario
    def clean_email(self):
        # Obtenemos el email procesado (con formato adecuado)
        email = self.cleaned_data.get('email')
        # Comprobamos que se haya modificado el email, de lo contrario siempre mostraría que el email ya esta registrado
        # porque no se ha modificado
        if 'email' in self.changed_data:
            # Comprobamos que no exista un usuario registrado ya con ese email
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('El email ya esta registrado, prueba con otro')
        return email