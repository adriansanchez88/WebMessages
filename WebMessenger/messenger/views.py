from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from .models import Chat, Mensaje
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

# Create your views here.
@method_decorator(login_required, name="dispatch")
class ChatListView(TemplateView):
    template_name = "messenger/chat_list.html"

@method_decorator(login_required, name="dispatch")
class ChatDetailView(DetailView):
    model = Chat

    def get_object(self):
        obj = super(ChatDetailView, self).get_object()
        if self.request.user not in obj.users.all():
            raise Http404()
        return obj

@login_required
def add_message(request, pk):    
    json_response = {'created':False}
    if request.user.is_authenticated:
        content = request.GET.get('content', None)
        if content:
            chat = get_object_or_404(Chat, pk=pk)
            message = Mensaje.objects.create(user=request.user, content=content)
            chat.messages.add(message)
            json_response['created'] = True
            if len(chat.messages.all()) is 1:
                json_response['first'] = True
    else:
        raise Http404("El usuario no esta identificado")
    return JsonResponse(json_response)

@login_required
def start_thread(request, username):
    user = get_object_or_404(User, username=username)
    chat = Chat.objects.find_or_create(user, request.user)
    return redirect(reverse_lazy('messenger:detail', args=[chat.pk]))