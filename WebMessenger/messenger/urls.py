from django.urls import path
from .views import ChatListView, ChatDetailView, add_message, start_thread

messenger_patterns = ([
    path('', ChatListView.as_view(), name='list'),
    path('chat/<int:pk>/', ChatDetailView.as_view(), name='detail'),
    path('chat/<int:pk>/add/', add_message, name='add'),
    path('chat/start/<username>/', start_thread, name='start'),
], 'messenger')