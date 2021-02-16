from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Función para reescribir el avatar cargado por el usuario 
# y no se llene el servidor de imágenes que no se utilizan
def upload_to_modificado(instance, filename):
    old_instance = Perfil.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'registration/' + filename

# Modelo que representará el perfil de usuario
class Perfil(models.Model):
    # Campo que contendrá una referencia (Relación OneToOne) al usuario al que pertenece el modelo, 
    # utiliza on_delete=models.CASCADE para cuando se elimine el usuario se elimine también su perfil asociado
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Campo que contendrá una imagen, que se guardará en la carpeta definida en 'upload_to'
    # No será un campo obligatorio por lo que se permitirá que sea null y blank 
    avatar = models.ImageField(upload_to=upload_to_modificado, null=True, blank=True)
    # Campo que contendrá una breve biografía del usuario
    # No será un campo obligatorio por lo que se permitirá que sea null y blank 
    bio = models.TextField(null=True, blank=True)
    # Campo que contendrá un enlace
    # No será un campo obligatorio por lo que se permitirá que sea null y blank 
    link = models.URLField(max_length=200, null=True, blank=True)

    # Se definen algunas configuraciones del modelo en la class Meta
    class Meta:
        # El orden por defecto en que se mostrarán los perfiles, en este caso por el username del user
        # Como se usa un campo de otro modelo se llama con user__username (campoQueRepresentaAlModelo__campoDelModeloRepresentado)
        ordering = ['user__username']

# Señal que se llamará automaticamente luego de crearse un usuario (post_save), donde se creará un perfil asociado 
# a este aunque no acceda al sitio web luego de registrarse
@receiver(post_save, sender=User)
def crear_perfil_automaticamente(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Perfil.objects.get_or_create(user=instance)