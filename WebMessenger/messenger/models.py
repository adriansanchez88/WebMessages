from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

# Create your models here.
class Mensaje(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

class ChatManager(models.Manager):
    def find(self, user1, user2):
        queryset = self.filter(users=user1).filter(users=user2)
        if len(queryset)>0:
            return queryset[0]
        return None
    
    def find_or_create(self, user1, user2):
        chat = self.find(user1, user2)
        if chat is None:
            chat = Chat.objects.create()
            chat.users.add(user1, user2)
        return chat

class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='chats')
    messages = models.ManyToManyField(Mensaje)
    updated = models.DateTimeField(auto_now=True)

    objects = ChatManager()

    class Meta:
        ordering = ['-updated']

def messages_changed(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    print(instance, action, pk_set)

    false_pk_set = set()
    if action is 'pre_add':
        for msg_pk in pk_set:
            msg = Mensaje.objects.get(pk=msg_pk)
            if msg.user not in instance.users.all():
                print("Ups, ({}) no forma parte de la conversación".format(msg.user))
                false_pk_set.add(msg_pk)
    
    # Buscar los mensajes de false_pk_set que estan en pk_set y borrarlos de pk_set
    pk_set.difference_update(false_pk_set)

    # Forzar la actualizacion haciendo un save
    instance.save()

m2m_changed.connect(messages_changed, sender=Chat.messages.through)